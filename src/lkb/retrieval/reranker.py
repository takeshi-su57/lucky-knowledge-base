from lkb.models import ScoredChunk
from lkb.retrieval.keyword_retriever import _tokenize_normalized


def _lexical_relevance(query: str, text: str) -> float:
    query_tokens = set(_tokenize_normalized(query))
    chunk_tokens = set(_tokenize_normalized(text))
    if not query_tokens or not chunk_tokens:
        return 0.0

    overlap = len(query_tokens.intersection(chunk_tokens))
    overlap_ratio = overlap / len(query_tokens)
    phrase_boost = 0.15 if query.lower() in text.lower() else 0.0
    return overlap_ratio + phrase_boost


def rerank_candidates(
    query: str,
    candidates: list[ScoredChunk],
    top_k: int = 5,
    semantic_weight: float = 0.65,
) -> list[ScoredChunk]:
    reranked: list[ScoredChunk] = []
    for row in candidates:
        lexical_score = _lexical_relevance(query, row.chunk.text)
        blended_score = (semantic_weight * row.score) + ((1.0 - semantic_weight) * lexical_score)
        reranked.append(ScoredChunk(chunk=row.chunk, score=blended_score))
    reranked.sort(key=lambda item: item.score, reverse=True)
    return reranked[:top_k]
