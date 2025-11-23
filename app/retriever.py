import os
import numpy as np

# Simple embedding generator using hashing (no GPU, no external models)
def embed_text(text: str) -> np.ndarray:
    tokens = text.lower().split()
    vec = np.zeros(256)
    for tok in tokens:
        vec[hash(tok) % 256] += 1
    return vec / (np.linalg.norm(vec) + 1e-6)

# Load and embed all recipes once
def load_recipes(recipe_dir="recipes"):
    store = []
    for fname in os.listdir(recipe_dir):
        if fname.endswith(".txt"):
            path = os.path.join(recipe_dir, fname)
            with open(path, "r", encoding="utf-8") as f:
                txt = f.read()
            emb = embed_text(txt)
            store.append((fname, txt, emb))
    return store

RECIPES = load_recipes()

# Return the top-1 most similar recipe
def retrieve(query: str):
    if not RECIPES:
        return None

    q_emb = embed_text(query)
    sims = [(fname, txt, float(np.dot(q_emb, emb))) for fname, txt, emb in RECIPES]
    sims.sort(key=lambda x: x[2], reverse=True)
    top = sims[0]
    return {"filename": top[0], "content": top[1], "score": top[2]}
