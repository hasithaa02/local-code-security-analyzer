import difflib

def count_tokens_estimate(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // 4)

def generate_diff(old: str, new: str) -> str:
    return "\n".join(
        difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="")
    )
