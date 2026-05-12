import math
from collections import Counter

from lkb.embeddings import tokenize
from lkb.models import Chunk, ScoredChunk
from lkb.retrieval.filters import apply_metadata_filters


def _normalize_keyword_token(token: str) -> str:
    token = token.lower()
    if token.isdigit():
        return token.lstrip("0") or "0"
    return token


def _tokenize_normalized(text: str) -> list[str]:
    return [_normalize_keyword_token(token) for token in tokenize(text)]


def _compute_idf(chunks: list[Chunk]) -> dict[str, float]:
    total_docs = len(chunks)
    doc_freq: Counter[str] = Counter()
    for chunk in chunks:
        doc_freq.update(set(_tokenize_normalized(chunk.text)))
    return {token: math.log((1.0 + total_docs) / (1.0 + df)) + 1.0 for token, df in doc_freq.items()}


def keyword_retrieve(
    query: str,
    chunks: list[Chunk],
    top_k: int = 5,
    metadata_filters: dict | None = None,
) -> list[ScoredChunk]:
    filtered_chunks = apply_metadata_filters(chunks, metadata_filters=metadata_filters)
    if not filtered_chunks:
        return []

    query_tokens = _tokenize_normalized(query)
    if not query_tokens:
        return []

    query_token_set = set(query_tokens)
    idf = _compute_idf(filtered_chunks)
    scored: list[ScoredChunk] = []

    for chunk in filtered_chunks:
        chunk_tokens = _tokenize_normalized(chunk.text)
        counts = Counter(chunk_tokens)
        score = 0.0
        overlap = 0
        for token in query_token_set:
            tf = counts.get(token, 0)
            if tf <= 0:
                continue
            overlap += 1
            score += (1.0 + math.log(1.0 + tf)) * idf.get(token, 0.0)
        if score <= 0:
            continue

        overlap_ratio = overlap / max(len(query_token_set), 1)
        score += overlap_ratio
        scored.append(ScoredChunk(chunk=chunk, score=score))

    scored.sort(key=lambda row: row.score, reverse=True)
    return scored[:top_k]
