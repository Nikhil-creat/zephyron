import os, httpx
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI(title="Zephyron API")
KB = ["Guardrails block injection and redact PII.", "RAG grounds answers in retrieved chunks.", "Human approval gates high-impact actions."]
class Q(BaseModel):
    question: str
@app.get("/health")
def health(): return {"ok": True}
@app.post("/chat")
async def chat(q: Q):
    ctx = "\n".join(c for c in KB if any(w in c.lower() for w in q.question.lower().split()))
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": f"Context:\n{ctx}\n\nQ: {q.question}"}]})
    return {"answer": r.json()["choices"][0]["message"]["content"], "context": ctx}

@app.post("/rag")
def rag(q: Q):
    hits = [c for c in KB if any(w in c.lower() for w in q.question.lower().split())]
    return {"hits": hits}
