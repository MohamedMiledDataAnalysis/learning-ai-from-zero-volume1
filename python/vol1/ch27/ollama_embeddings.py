"""Chapter 27 — search the prospectus with a pretrained embedding model (nomic-embed-text in Ollama).

    python python/vol1/ch27/ollama_embeddings.py --mode replay   print the recorded ranking
    python python/vol1/ch27/ollama_embeddings.py --mode record   needs: ollama pull nomic-embed-text

The recording keeps the top 3 passages and their similarity scores (not the vectors themselves).
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part45_common import PENDING, REPO, parse_mode  # noqa: E402
from tar_agent.tools.prospectus import chunks  # noqa: E402

QUERY = "Which loans were eligible?"
WANTED = "Each loan met the following criteria"
EMBED_MODEL = "nomic-embed-text"
RECORDING = REPO / "python" / "recordings" / "vol1-ch27-ollama-embeddings.json"

mode = parse_mode()
docs = chunks()
if mode == "replay":
    if not RECORDING.exists():
        print(PENDING)
        raise SystemExit(0)
    top = json.loads(RECORDING.read_text(encoding="utf-8"))["top"]
else:
    import ollama
    # nomic-embed-text expects a task prefix: 'search_document:' for passages, 'search_query:' for questions.
    doc_vecs = np.array(ollama.embed(model=EMBED_MODEL,
                                     input=[f"search_document: {d['text']}" for d in docs])["embeddings"])
    q = np.array(ollama.embed(model=EMBED_MODEL, input=[f"search_query: {QUERY}"])["embeddings"][0])
    sims = doc_vecs @ q / (np.linalg.norm(doc_vecs, axis=1) * np.linalg.norm(q))
    order = np.argsort(-sims, kind="stable")[:3]
    top = [{"chunk": int(i), "page": docs[i]["page"], "score": round(float(sims[i]), 4)} for i in order]
    if mode == "record":
        RECORDING.parent.mkdir(parents=True, exist_ok=True)
        RECORDING.write_text(json.dumps({"model": EMBED_MODEL, "query": QUERY, "top": top}, indent=2))

found = any(WANTED in docs[t["chunk"]]["text"] for t in top)
print(f"Pretrained embeddings ({EMBED_MODEL}): {'FOUND' if found else 'missed'}")
for rank, t in enumerate(top, start=1):
    print(f"  {rank}. page {t['page']}  similarity {t['score']:.3f}  {docs[t['chunk']]['text'][:58]}...")
