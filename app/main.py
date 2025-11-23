from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.model_loader import fix_code_with_model, is_model_available
from app.prompts import build_prompt
from app.utils import generate_diff, count_tokens_estimate
import time

app = FastAPI(title="Local Code Security Analyzer")

class FixRequest(BaseModel):
    language: str
    cwe: str
    code: str

@app.post("/local_fix")
def local_fix(req: FixRequest):
    start = time.time()
    prompt = build_prompt(req.language, req.cwe, req.code)
    input_tokens = count_tokens_estimate(prompt)

    try:
        if is_model_available():
            fixed, explanation = fix_code_with_model(prompt)
        else:
            fixed = "// REMOTE FALLBACK: Model not available locally\n" + req.code
            explanation = "Local model unavailable. Returned safe fallback response."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    output_tokens = count_tokens_estimate(fixed)
    diff = generate_diff(req.code, fixed)
    latency_ms = int((time.time() - start) * 1000)

    return {
        "fixed_code": fixed,
        "diff": diff,
        "explanation": explanation,
        "model_used": "local-gguf-or-remote-fallback",
        "token_usage": {"input_tokens": input_tokens, "output_tokens": output_tokens},
        "latency_ms": latency_ms
    }
