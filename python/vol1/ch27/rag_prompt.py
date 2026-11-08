"""Chapter 27 — build a retrieval-augmented prompt and (optionally) ask the model.

    python python/vol1/ch27/rag_prompt.py show            print the prompt built from one search
    python python/vol1/ch27/rag_prompt.py split           print the passages found with two searches
    python python/vol1/ch27/rag_prompt.py ask --mode replay   ask the model with the two-search prompt
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part45_common import ask_model, parse_mode  # noqa: E402
from tar_agent.tools.prospectus import search_prospectus  # noqa: E402

QUESTION = "What is the limit for the 90+ day arrears ratio, and what happens if it is exceeded?"

SYSTEM = ("You answer questions about the Thames Auto Receivables 2026-1 prospectus. "
          "Use only the passages provided. After each statement, cite the page in brackets, e.g. (page 9). "
          "If the passages do not contain the answer, say: 'The passages provided do not answer this.'")


SUB_QUESTIONS = ["What is the limit for the 90+ day arrears ratio?",
                 "What happens after a trigger event occurs?"]


def retrieve(queries, top_k):
    """Search once per query and keep each passage once, in the order found."""
    found, seen = [], set()
    for q in queries:
        for r in search_prospectus(q, top_k=top_k)["results"]:
            if r["text"] not in seen:
                seen.add(r["text"])
                found.append(r)
    return found


def build_messages(question, queries=None, top_k=3):
    results = retrieve(queries or [question], top_k)
    passages = "\n\n".join(f"[Passage {i}, page {r['page']}, {r['section']}]\n{r['text']}"
                           for i, r in enumerate(results, start=1))
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Passages:\n{passages}\n\nQuestion: {question}"}]


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "show"
    if action == "show":
        for m in build_messages(QUESTION):
            print(f"[{m['role']}]\n{m['content']}\n")
    elif action == "split":
        for q in SUB_QUESTIONS:
            print(f"Search: {q}")
        for i, r in enumerate(retrieve(SUB_QUESTIONS, top_k=2), start=1):
            print(f"  Passage {i}, page {r['page']}: {r['text'][:70]}...")
        found = any("principal is paid sequentially" in r["text"] for r in retrieve(SUB_QUESTIONS, top_k=2))
        print(f"Consequence passage included: {'yes' if found else 'no'}")
    else:
        messages = build_messages(QUESTION, SUB_QUESTIONS, top_k=2)
        reply = ask_model(messages, "vol1-ch27-rag-answer", parse_mode())
        if reply is not None:
            print(reply.strip())
