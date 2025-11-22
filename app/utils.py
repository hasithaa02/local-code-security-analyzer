import difflib
from transformers import AutoTokenizer

# Tokenizer model name used for approximate token counting
TOKENIZER_MODEL = "Qwen/Qwen2.5-Coder-1.5B"
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_MODEL)

def count_tokens(text):
    return len(tokenizer(text).input_ids)

def generate_diff(old, new):
    diff = difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        lineterm=""
    )
    return "\n".join(list(diff))
