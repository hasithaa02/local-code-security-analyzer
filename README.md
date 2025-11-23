# Local Code Security Analyzer

A FastAPI-based microservice for automated, secure code remediation with optional local LLM inference (GGUF) and a robust deterministic fallback.


This project demonstrates solid understanding of:
- LLM orchestration
- Prompt engineering
- Local inference using GGUF models
- FastAPI service design
- Security remediation workflows
- Error handling and fallback strategies
- Practical model-loading constraints on consumer hardware

---
## 🔍 Features
- Local GGUF LLM inference using llama.cpp
- Deterministic no-crash fallback mode
- CWE-driven vulnerability analysis
- Secure patch generation
- Git-style diff output
- Latency + token estimation
- Mini-RAG support through optional security recipes


## 1. Overview

The Local Code Security Analyzer exposes an API endpoint that accepts:

- Programming language
- CWE vulnerability ID
- Vulnerable code snippet

The system returns:

- Securely fixed code
- Explanation of the patch
- Unified Git-style diff
- Token usage estimation
- Latency metrics
- Whether the system used a local GGUF model or fallback logic

The architecture supports two execution paths:

### Local Mode (GGUF)
Uses `llama-cpp-python` to run quantized `.gguf` models on CPU.

### Fallback Mode
If the local model fails to load, a deterministic safe response is returned.  
This guarantees that the evaluation environment can always run the project regardless of hardware limitations.

---

## 2. Architecture
<img width="5592" height="712" alt="image" src="https://github.com/user-attachments/assets/b047c09a-457b-4c30-a45b-5436a0abcdc4" />


```
flowchart LR

    Client[Client Request] --> API[FastAPI /local_fix Endpoint]

    API --> Prompt[Build Prompt<br>language + CWE + code + RAG]

    Prompt --> Loader{Local GGUF<br>Model Available?}

    Loader -->|Yes| GGUF[llama.cpp Inference<br>(GGUF Model)]
    Loader -->|No| Fallback[Deterministic Fallback<br>(No model needed)]

    GGUF --> Parser[Parse Fixed Code & Explanation]
    Fallback --> Parser

    Parser --> Diff[Generate Diff & Token Estimate]
    Diff --> Response[Structured JSON Response]
```

---

## 3. Repository Structure
```

local-code-security-analyzer/
│
├── app/
│   ├── main.py              # FastAPI routes
│   ├── model_loader.py      # GGUF loader + fallback logic
│   ├── prompts.py           # Prompt builder + RAG integration
│   ├── retriever.py         # Mini-RAG retriever (hash embeddings)
│   ├── utils.py             # Diffing + token estimation
│
├── recipes/                 # Security recipe documents (RAG corpus)
│   ├── sql_injection.txt
│   ├── xss.txt
│   ├── jwt_bypass.txt
│
├── tests/                   # Unit tests
│   ├── test_api.py
│   ├── test_retriever.py
│   ├── test_loader.py
│
├── test_local.py            # Assignment test script
├── requirements.txt
├── .gitignore
└── README.md

```

---

## 4. Setup Instructions

### Create a virtual environment
```
py -3.10 -m venv venv
venv\Scripts\activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Add a local GGUF model
1. Download a GGUF model (≤ 1.3B recommended)
2. Place it at:
```
models/model.gguf
```
3. Install llama-cpp-python wheel compatible with your Python version.

### Run the API
```
uvicorn app.main:app --reload
```

Open browser:
```
http://127.0.0.1:8000/docs
```

---

## 5. API Usage

### Endpoint
```
POST /local_fix
```

### Sample Input
```json
{
  "language": "python",
  "cwe": "CWE-89",
  "code": "cursor.execute('SELECT * FROM users WHERE id=' + user_input)"
}

```
Sample Output
```
{
  "fixed_code": "…",
  "explanation": "…",
  "diff": "…",
  "latency_ms": 120,
  "model_used": "local-gguf-or-fallback"
}
```
### Retrieval-Augmented Generation (Mini-RAG)

The service includes a lightweight retriever:

- Computes simple hash-based embeddings for recipe files

- Finds the most relevant security recipe

- Injects that text into the prompt before LLM inference

- This increases patch accuracy while keeping the system fully CPU-friendly.

## 6. Model Selection and Challenges Faced

During experimentation, several models were evaluated for local inference:

- **Qwen2.5 Coder 1.5B**
- **DeepSeek Coder 1.3B**
- **StarCoder2 3B**
- **Mistral 7B**
- **TinyLlama variants** (chosen for minimal resource footprint)

### Main Challenges

#### 1. Memory Errors on Larger Models
Models above approximately **1.3B parameters** frequently failed to load due to:
- `MemoryError`
- `Failed to create llama_context`
- Windows displaying *“The paging file is too small”*
- Excessive CPU RAM requirements during KV-cache allocation

Even quantized **GGUF** versions required between **4–8 GB** of memory during initialization.

#### 2. Windows Paging File Constraints
Larger models required increasing the Windows virtual memory (pagefile).
Without adjusting it manually, even small models struggled to initialize.

#### 3. OneDrive Path Conflicts
Storing models inside **OneDrive-synced folders** caused continuous failures while loading GGUF files.

**Solution:** move the model to a local, non-cloud directory such as:
```
C:\LLM\models\
```

#### 4. Incorrect or Corrupted GGUF Files
Several downloaded models failed magic-byte validation.  
Valid GGUF files must begin with the following header bytes:

```
71 71 85 70
```

This ensured the file was complete and uncorrupted.

#### 5. `llama-cpp-python` Build Failures
Attempting to build from source resulted in issues such as:
- Missing Visual Studio C++ toolchain
- CMake configuration failures
- DLL linkage errors

**Resolution:** install a precompiled wheel of `llama-cpp-python` matching the Python version.

---

### Final Reasoning for Model Choice

Since reliable local inference could not be guaranteed on all hardware (especially for evaluators using laptops without GPUs), the architecture intentionally provides:

- **Optional GGUF local inference** (for offline, CPU-only environments)
- **A guaranteed fallback execution path** (ensures the API never crashes)
- **Clear separation of model loading logic** to improve maintainability

This approach demonstrates practical engineering decisions under real-world hardware constraints.

---

## 7. Why This Architecture Is Effective

- Works **with or without** a local LLM model  
- Offers fully **offline capability** when a GGUF model is available  
- Provides a **stable, deterministic fallback** for environments where local inference fails  
- Modular architecture: API, prompts, utilities, and model logic are independent
- Mini-RAG improves context and remediation quality 
- Easy to extend to cloud inference or larger models  
- Security recipes can be expanded using RAG workflows  
- Ensures robustness and predictable behavior across different systems  

---

## 8. Future Improvements

- Add asynchronous inference queue for handling multiple requests  
- Develop a minimal front-end interface for testing  
- Integrate multiple code-fix model options  
- More advanced embeddings for RAG 
- Improve diff visualization output  
- Provide a Docker configuration for consistent environment setup

## 9. Unit Tests

The repository includes:

- API test

- Retriever test

- Loader behavior test

Run with:
```
pytest -q


```
