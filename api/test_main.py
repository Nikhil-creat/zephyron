from fastapi.testclient import TestClient
from main import app
c = TestClient(app)
def test_health(): assert c.get("/health").json() == {"ok": True}
def test_rag(): assert "hits" in c.post("/rag", json={"question": "guardrails"}).json()
