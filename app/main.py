import time
from fastapi import FastAPI
from pydantic import BaseModel
from app.model_loader import run_model
from app.prompts import build_prompt
from app.utils import generate_diff, count_tokens
from app.rag import retrieve_context

app = FastAPI(title="AI Code Remediation Microservice")

class FixRequest(BaseModel):
    language: str
    cwe: str
    code: str

@app.post("/local_fix")
def fix_code(data: FixRequest):
    start = time.time()

    context = retrieve_context(data.cwe)
    prompt = build_prompt(data.language, data.cwe, data.code, context)

    input_tokens = count_tokens(prompt)
    output = run_model(prompt)

    # Best-effort parsing of expected sections
    fixed_code = output
    explanation = ""
    try:
        if "### FIXED CODE" in output:
            fixed_code = output.split("### FIXED CODE",1)[1]
            if "### EXPLANATION" in fixed_code:
                fixed_code, explanation = fixed_code.split("### EXPLANATION",1)
                fixed_code = fixed_code.strip()
                explanation = explanation.strip()
    except Exception:
        # keep defaults if parsing fails
        pass

    diff = generate_diff(data.code, fixed_code)

    latency = int((time.time() - start) * 1000)

    return {
        "fixed_code": fixed_code,
        "diff": diff,
        "explanation": explanation,
        "model_used": "Qwen2.5-Coder-1.5B",
        "token_usage": {
            "input_tokens": input_tokens,
            "output_tokens": count_tokens(output)
        },
        "latency_ms": latency
    }
