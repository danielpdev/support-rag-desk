"""Small transparent lexical/dense/hybrid rankers, with explicit model loading."""

import re
from functools import lru_cache


def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - {
        "a",
        "the",
        "is",
        "to",
        "i",
        "do",
        "how",
        "of",
        "in",
        "and",
        "my",
        "for",
        "are",
        "when",
    }


def lexical(query, docs):
    q = {w[:-1] if w.endswith("s") and len(w) > 4 else w for w in tokens(query)}
    scored = [
        (
            d,
            len(q & {w[:-1] if w.endswith("s") and len(w) > 4 else w for w in tokens(d["text"])})
            / max(1, len(q)),
        )
        for d in docs
    ]
    return sorted(scored, key=lambda x: (-x[1], x[0]["id"]))


@lru_cache
def encoder():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")


def rank(query, docs, method="lexical"):
    if method == "lexical":
        return lexical(query, docs)
    if method not in {"dense", "hybrid"}:
        raise ValueError("unknown retrieval method")
    if not docs:
        return []
    model = encoder()
    matrix = model.encode([query] + [d["text"] for d in docs], normalize_embeddings=True)
    dense = sorted(
        [(d, float(matrix[0] @ matrix[i + 1])) for i, d in enumerate(docs)], key=lambda x: (-x[1], x[0]["id"])
    )
    if method == "dense":
        return dense
    ranks = {d["id"]: 1 / (60 + i) for i, (d, _) in enumerate(dense, 1)}
    for i, (d, _) in enumerate(lexical(query, docs), 1):
        ranks[d["id"]] += 1 / (60 + i)
    return sorted([(d, ranks[d["id"]]) for d in docs], key=lambda x: (-x[1], x[0]["id"]))
