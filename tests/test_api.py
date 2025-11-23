from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_local_fix_endpoint():
    payload = {
        "language": "python",
        "cwe": "CWE-89",
        "code": "cursor.execute('SELECT * FROM users WHERE id=' + user_input)"
    }
    res = client.post("/local_fix", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert "fixed_code" in data
    assert "explanation" in data
    assert "diff" in data
    assert "model_used" in data
