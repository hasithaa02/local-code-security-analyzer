from app.model_loader import load_local_model

def test_model_loader_fallback():
    model = load_local_model()
    assert model is not None
