from app.retriever import retrieve

def build_prompt(language, cwe, code, context=""):
    rag = retrieve(code)
    rag_text = rag["content"] if rag else ""

    return f"""
You are a security code remediation assistant.

### CWE
{cwe}

### ORIGINAL CODE ({language})
{code}

### CONTEXT FROM SECURITY RECIPE
{rag_text}

### TASK
Provide a secure corrected version. Use:

### FIXED CODE
<code>

### EXPLANATION
<explanation>
"""
