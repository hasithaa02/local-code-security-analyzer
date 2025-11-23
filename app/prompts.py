def build_prompt(language, cwe, code, context="") -> str:
    return f"""You are a security code remediation assistant.

### CWE
{cwe}

### ORIGINAL CODE ({language})
{code}

### TASK
Provide a secure corrected version. Output strictly using:

### FIXED CODE
<code>

### EXPLANATION
<explanation>
"""
