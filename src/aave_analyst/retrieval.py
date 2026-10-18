from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,time
import requests
from bs4 import BeautifulSoup
from rank_bm25 import BM25Okapi

SOURCES={"SUPPLY":"https://aave.com/help/supplying/supply-tokens","BORROW":"https://aave.com/help/borrowing/borrow-tokens","LIQ":"https://aave.com/help/borrowing/liquidations"}


def tokenize(text):return re.findall(r"[\w]+",text.lower())


def collect_documents(root):
    folder=Path(root)/"data/documents";folder.mkdir(parents=True,exist_ok=True)
    chunks=[]
    for key,url in SOURCES.items():
        response=requests.get(url,timeout=45,headers={"User-Agent":"AaveCourseResearch/0.1"});response.raise_for_status()
        html=response.content.decode("utf-8")
        soup=BeautifulSoup(html,"html.parser")
        for element in soup(["script","style","nav","footer","header"]):element.decompose()
        main=soup.find("main") or soup.find("article") or soup.body
        text=main.get_text(" ",strip=True)
        if len(text)<300:raise ValueError(f"Insufficient extracted content from {url}")
        stamp=datetime.now(timezone.utc).isoformat()
        (folder/f"{key}.html").write_text(html,encoding="utf-8")
        words=text.split()
        for start in range(0,len(words),340):
            block=" ".join(words[start:start+400]);index=start//340
            chunks.append({"id":f"DOC_{key}_{index:03d}","title":soup.title.get_text() if soup.title else key,"url":url,"collected_at":stamp,"source_sha256":hashlib.sha256(response.content).hexdigest(),"text":block})
    (folder/"chunks.json").write_text(json.dumps(chunks,indent=2,ensure_ascii=False),encoding="utf-8")
    return chunks


class Retriever:
    def __init__(self,chunks):
        self.chunks=chunks
        self.calls=[]
        self.index=BM25Okapi([tokenize(c["title"]+" "+c["text"]) for c in chunks]) if chunks else None

    @classmethod
    def load(cls,path):return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    def search(self,query,k=5):
        started=time.perf_counter()
        if not self.index:result=[]
        else:
            scores=self.index.get_scores(tokenize(query))
            ids=sorted(range(len(scores)),key=lambda i:scores[i],reverse=True)[:k]
            result=[dict(self.chunks[i],score=float(scores[i])) for i in ids]
        self.calls.append({'tool':'retrieve','query':query,'document_ids':[d['id'] for d in result],'started':started,'elapsed':time.perf_counter()-started})
        return result
