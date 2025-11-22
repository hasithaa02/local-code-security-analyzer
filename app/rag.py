import os
try:
    import faiss
    from sentence_transformers import SentenceTransformer
except Exception:
    # Minimal fallback if packages are not installed in the environment running tests.
    faiss = None
    SentenceTransformer = None

MODEL = None
index = None
texts = []
RECIPE_DIR = os.path.join(os.path.dirname(__file__), "..", "recipes")

if SentenceTransformer is not None and faiss is not None:
    MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    texts = []
    for file in sorted(os.listdir(RECIPE_DIR)):
        path = os.path.join(RECIPE_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            texts.append(f.read())
    if texts:
        embs = MODEL.encode(texts)
        index = faiss.IndexFlatL2(embs.shape[1])
        index.add(embs)

def retrieve_context(cwe):
    if index is None or MODEL is None or not texts:
        return "Refer to secure coding best practices for the specified CWE."
    q_emb = MODEL.encode([cwe])
    _, idx = index.search(q_emb, 1)
    return texts[idx[0][0]]
