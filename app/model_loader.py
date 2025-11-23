from pathlib import Path

# Model should be placed at: ./models/model.gguf
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model.gguf"


def is_model_available():
    """
    Returns True only if:
    - llama_cpp is installed
    - model.gguf exists
    """
    try:
        from llama_cpp import Llama  # type: ignore
        return MODEL_PATH.exists()
    except Exception:
        return False


def fix_code_with_model(prompt: str):
    """
    Run the local GGUF model (llama.cpp backend).
    """
    from llama_cpp import Llama  # type: ignore

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"GGUF model not found at {MODEL_PATH}")

    llm = Llama(
        model_path=str(MODEL_PATH),
        n_ctx=512,
        n_threads=4,
        n_batch=16,
        n_gpu_layers=0
    )

    out = llm(prompt, max_tokens=256, temperature=0.0)
    text = out.get("choices", [{}])[0].get("text", "")

    fixed = text
    explanation = ""

    if "### FIXED CODE" in text:
        try:
            fixed = text.split("### FIXED CODE", 1)[1]
            if "### EXPLANATION" in fixed:
                fixed, explanation = fixed.split("### EXPLANATION", 1)
                fixed = fixed.strip()
                explanation = explanation.strip()
        except Exception:
            pass

    return fixed, explanation
