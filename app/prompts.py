def build_prompt(language, cwe, code, context):
    return f"""You are a security code remediation AI.

### CWE
{cwe}

### SECURITY CONTEXT
{context}

### ORIGINAL CODE ({language})
{code}

### TASK
Fix the vulnerability, improve security, and return strictly in this format:

### FIXED CODE
<secure code>

### EXPLANATION
<why the fix works + what vulnerability existed>
""".format(language=language, cwe=cwe, code=code, context=context)
