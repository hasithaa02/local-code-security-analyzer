from app.retriever import retrieve

def test_retriever_returns_top1():
    result = retrieve("SELECT * FROM users")
    assert result is not None
    assert "content" in result
    assert isinstance(result["content"], str)
