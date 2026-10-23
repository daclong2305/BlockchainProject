from dataclasses import dataclass,asdict
from copy import deepcopy
import time
from .models import Draft,QuerySpec,RunResult,Issue
from .planning import planning_context,analysis_errors,runtime_dictionary
from .verification import semantic_rules,response_issues,verify_claims,evidence_payload,coverage_rules,sql_review_payload


@dataclass(frozen=True)
class Mode:
    sql_check:bool=False
    evidence_check:bool=False
    repair:bool=False
    generic_review:bool=False


MODES={"B0":Mode(),"B1":Mode(repair=True,generic_review=True),"P":Mode(True,True,True),"P-SQL":Mode(False,True,True),"P-Evidence":Mode(True,False,True),"P-Repair":Mode(True,True,False)}


class Analyst:
    def __init__(self,db,retriever,llm,deadline=120.):self.db=db;self.retriever=retriever;self.llm=llm;self.deadline=deadline

    @staticmethod
    def remaining(end):
        remaining=end-time.perf_counter()
        if remaining<=0:raise TimeoutError("Question deadline exceeded")
        return remaining

    def _call(self,role,payload,end):
        value=self.llm.complete(role,payload,timeout=self.remaining(end))
        self.remaining(end)
        return value

    def _answer(self,draft,end):
        value=self._call("answer",evidence_payload(draft),end)
        draft.answer=str(value.get("answer",""));draft.claims=value.get("claims",[]);draft.refused=bool(value.get("refused",False))
        if not draft.answer or not isinstance(draft.claims,list):raise ValueError("Malformed answer response")

    def make_draft(self,question):
        start=time.perf_counter();end=start+self.deadline;usage_start=len(self.llm.calls)
        sql_start=len(self.db.calls);retrieval_start=len(self.retriever.calls)
        draft=Draft(question=question,spec=QuerySpec())
        try:
            context=planning_context(self.db,self.retriever,question,lambda:self.remaining(end))
            requirements=self._call("plan",context,end)
            spec=QuerySpec(**{k:v for k,v in requirements.items() if k in QuerySpec.__dataclass_fields__})
            draft.planning={'initial':asdict(spec),'availability':context['availability']}
            reasons=analysis_errors(spec)
            if spec.clarification:reasons.append('Check whether clarification is genuinely needed instead of refusing an answerable question')
            if spec.kind=='unanswerable':reasons.append('Check available document evidence and data before declaring the question unsupported')
            if reasons:
                reviewed=self._call('plan_review',dict(context,proposed_requirements=asdict(spec),review_reasons=reasons),end)
                spec=QuerySpec(**{k:v for k,v in reviewed.items() if k in QuerySpec.__dataclass_fields__})
                draft.planning.update(review_reasons=reasons,revised=asdict(spec))
            errors=analysis_errors(spec)
            if errors:raise ValueError('Invalid analysis: '+'; '.join(errors))
            draft.spec=spec
            if spec.clarification:
                draft.answer=spec.clarification;draft.refused=True
            else:
                if spec.kind in {"docs","mixed"}:draft.documents=self.retriever.search(spec.retrieval_query or question)
                if spec.kind in {"data","mixed"}:
                    draft.sql=self._call("sql",{"question":question,"requirements":asdict(spec),"schema":self.db.schema(),"dictionary":runtime_dictionary()},end)["sql"]
                    try:draft.query_result=self.db.query(draft.sql,timeout=min(15,self.remaining(end)))
                    except Exception as exc:draft.issues=[Issue("sql_execution",str(exc),"sql")]
                draft.tools=deepcopy(self.db.calls[sql_start:]+self.retriever.calls[retrieval_start:])
                self._answer(draft,end)
        except Exception as exc:
            draft.error=f"{type(exc).__name__}: {exc}"
        finally:
            draft.elapsed=time.perf_counter()-start;draft.usage=deepcopy(self.llm.calls[usage_start:])
            draft.tools=deepcopy(self.db.calls[sql_start:]+self.retriever.calls[retrieval_start:])
        return draft

    def continue_draft(self,shared_draft,mode):
        flags=MODES[mode];draft=deepcopy(shared_draft);start=time.perf_counter();end=start+max(0,self.deadline-draft.elapsed)
        usage_start=len(self.llm.calls);trace=[];repairs=0;issues=[];status="unchecked";error=""
        sql_start=len(self.db.calls);retrieval_start=len(self.retriever.calls)
        try:
            self.remaining(end)
            if draft.error:raise RuntimeError(draft.error)
            if mode!="B0" and not draft.spec.clarification:
                while True:
                    self.remaining(end)
                    issues=list(draft.issues)
                    if flags.generic_review:
                        issues.extend(response_issues(self._call("generic_review",evidence_payload(draft),end)))
                    else:
                        if flags.sql_check and draft.sql:
                            issues.extend(semantic_rules(draft.sql,asdict(draft.spec)))
                            issues.extend(coverage_rules(self.db,draft.spec,timeout=min(15,self.remaining(end))))
                            payload=sql_review_payload(draft)
                            issues.extend(response_issues(self._call("sql_review",payload,end)))
                        # Do not spend calls reviewing prose based on known-invalid SQL.
                        if flags.evidence_check and not any(i.action in {"sql","stop"} for i in issues):
                            issues.extend(verify_claims(draft,self.llm,timeout=self.remaining(end)))
                    trace.append({"event":"verification","repair":repairs,"issues":[asdict(i) for i in issues],"sql":draft.sql,"answer":draft.answer})
                    if not issues:status="checks_passed";break
                    status="unverified"
                    if not flags.repair or repairs>=2 or any(i.action=="stop" for i in issues):break
                    before=(draft.sql,draft.answer,tuple(d["id"] for d in draft.documents))
                    fix=self._call("repair",dict(evidence_payload(draft),issues=[asdict(i) for i in issues],schema=self.db.schema()),end)
                    repairs+=1
                    new_sql=fix.get("sql","")
                    if new_sql and new_sql!=draft.sql:
                        draft.sql=new_sql;draft.query_result=None;draft.issues=[];draft.claims=[];draft.answer=""
                        # First SQL call of this repair; one optional auxiliary call remains.
                        try:draft.query_result=self.db.query(new_sql,timeout=min(15,self.remaining(end)))
                        except Exception as exc:draft.issues=[Issue("sql_execution",str(exc),"sql")]
                    query=fix.get("retrieval_query","")
                    if query:
                        draft.documents=self.retriever.search(query)
                        draft.tools.append(deepcopy(self.retriever.calls[-1]))
                    # A repeated unchanged SQL-only fix cannot improve the query.
                    if before[0]==draft.sql and not query and all(i.action=="sql" for i in issues):
                        trace.append({"event":"unchanged_repair_stop"});break
                    self._answer(draft,end)
                    after=(draft.sql,draft.answer,tuple(d["id"] for d in draft.documents))
                    trace.append({"event":"repair","repair":repairs,"sql":draft.sql,"answer":draft.answer})
                    if after==before:trace.append({"event":"unchanged_repair_stop"});break
                self.remaining(end)
        except Exception as exc:
            status="error";error=f"{type(exc).__name__}: {exc}"
            trace.append({"event":"error","message":error})
        if status=="unverified":
            draft.answer += "\n\nChưa thể xác minh đầy đủ: " + "; ".join(i.message for i in issues)
        tools=deepcopy(shared_draft.tools)+deepcopy(self.db.calls[sql_start:]+self.retriever.calls[retrieval_start:])
        return RunResult(mode,draft,status,repairs,issues,trace,draft.elapsed+time.perf_counter()-start,deepcopy(draft.usage)+deepcopy(self.llm.calls[usage_start:]),error,tools)

    def answer(self,question,mode="P"):
        return self.continue_draft(self.make_draft(question),mode)
