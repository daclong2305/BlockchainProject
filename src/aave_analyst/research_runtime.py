"""Transparent scheduling/usage ledger for authorized research calls."""
import json,time
from pathlib import Path
from botocore.exceptions import ClientError, EndpointConnectionError, ConnectionClosedError, SSLError


class ResearchRunBlocked(BaseException):
    """Stop scheduling cases on infrastructure failure; preserve checkpoints."""

class MeteredLLM:
    def __init__(self,inner,path,pace=6.,cap=5.):
        self.inner=inner;self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
        self.pace=pace;self.cap=cap;self.last=0.;self.calls=inner.calls
        # Conservative standard cross-region estimate, not account billing.
        self.estimate=0.
        if self.path.exists():
            self.estimate=sum(r.get('estimated_usd',0) for r in map(json.loads,self.path.read_text(encoding='utf-8').splitlines()))
    def config(self):return self.inner.config()
    def complete(self,role,payload,timeout=60.):
        deadline=time.monotonic()+timeout
        for attempt in range(1,4):
            try:
                return self._attempt(role,payload,deadline-time.monotonic(),attempt)
            except SSLError as exc:
                raise ResearchRunBlocked('SSL verification failed; checkpoint retained') from exc
            except (ClientError,EndpointConnectionError,ConnectionClosedError) as exc:
                retryable=not isinstance(exc,ClientError) or exc.response.get('Error',{}).get('Code') in {'ThrottlingException','TooManyRequestsException','ServiceUnavailableException','InternalServerException'}
                if not retryable:raise
                delay=8*2**(attempt-1)
                if attempt==3 or time.monotonic()+delay+1>=deadline:
                    raise ResearchRunBlocked('Transport retries exhausted; checkpoint retained') from exc
                time.sleep(delay)

    def _attempt(self,role,payload,timeout,attempt):
        # Reserve a conservative maximum for the serialized input and two outputs.
        reserve=(len(json.dumps(payload,ensure_ascii=False).encode())+20000)*1.1/1e6+8192*5.5/1e6
        if self.estimate+reserve>self.cap:raise ResearchRunBlocked('Research cost guard reached; retain partial results')
        wait=max(0,self.last+self.pace-time.monotonic())
        if wait>=timeout:raise TimeoutError('Rate-limit queue exceeds remaining deadline')
        if wait:time.sleep(wait)
        before=len(self.calls);started=time.monotonic();self.last=started
        try:return self.inner.complete(role,payload,timeout=timeout-wait)
        finally:
            for call in self.calls[before:]:
                unknown=bool(call.get('error')) and not (call.get('input_tokens') or call.get('output_tokens'))
                cost=reserve if unknown else (call.get('input_tokens',0)*1.1+call.get('output_tokens',0)*5.5)/1e6
                call.update(queue_seconds=wait,estimated_usd=cost,usage_unknown=unknown,transport_attempt=attempt)
                self.estimate+=cost
                with self.path.open('a',encoding='utf-8') as f:f.write(json.dumps(call,ensure_ascii=False)+'\n')
