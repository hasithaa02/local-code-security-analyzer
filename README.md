# ai-codefix-assignment-hasit

**AI Code Remediation Microservice (LLM + Local Inference + Optional RAG)**

This repository implements a FastAPI microservice that runs a local open-source LLM to analyze and remediate vulnerable code snippets.
It includes:
- Local model inference (Qwen2.5-Coder-1.5B)
- FastAPI endpoint `/local_fix`
- Diff generation and explanation
- Token usage + latency logging
- Optional RAG (FAISS + SentenceTransformers)
- test_local.py to exercise the API
- Dockerfile for containerized runs

---

## How to run (CPU-only)

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Start the service:
```bash
uvicorn app.main:app --reload
```

3. Run tests (from another terminal):
```bash
python test_local.py
```

---

## Notes
- The original assignment PDF included by the recruiter is placed in the repository as `Assignment 1.0.pdf`.
- If FAISS or sentence-transformers are not available, the RAG module gracefully falls back to a simple message.
- Model selection and prompt format are described in the code and README.

