from lkb.models import Chunk, ScoredChunk
from lkb.retrieval.keyword_retriever import keyword_retrieve
from lkb.retrieval.reranker import rerank_candidates
from lkb.retrieval.vector_retriever import vector_retrieve


def _chunk_key(chunk: Chunk) -> tuple:
    return (chunk.chunk_id, chunk.source_path, tuple(chunk.heading_path), chunk.text)


def merge_and_dedupe_candidates(
    dense_candidates: list[ScoredChunk],
    keyword_candidates: list[ScoredChunk],
    top_k: int,
    dense_weight: float = 1.0,
    keyword_weight: float = 1.0,
) -> list[ScoredChunk]:
    merged: dict[tuple, ScoredChunk] = {}
    for row in dense_candidates:
        key = _chunk_key(row.chunk)
        weighted = ScoredChunk(chunk=row.chunk, score=row.score * dense_weight)
        current = merged.get(key)
        if current is None or weighted.score > current.score:
            merged[key] = weighted

    for row in keyword_candidates:
        key = _chunk_key(row.chunk)
        weighted = ScoredChunk(chunk=row.chunk, score=row.score * keyword_weight)
        current = merged.get(key)
        if current is None or weighted.score > current.score:
            merged[key] = weighted

    ranked = sorted(merged.values(), key=lambda item: item.score, reverse=True)
    return ranked[:top_k]


def hybrid_retrieve(
    query: str,
    chunks: list[Chunk],
    top_k: int = 5,
    metadata_filters: dict | None = None,
    dense_candidate_k: int = 20,
    keyword_candidate_k: int = 20,
) -> list[ScoredChunk]:
    candidate_k = max(top_k, dense_candidate_k, keyword_candidate_k)
    dense = vector_retrieve(query, chunks, top_k=candidate_k, metadata_filters=metadata_filters)
    keyword = keyword_retrieve(query, chunks, top_k=candidate_k, metadata_filters=metadata_filters)
    merged = merge_and_dedupe_candidates(
        dense_candidates=dense,
        keyword_candidates=keyword,
        top_k=candidate_k,
        dense_weight=0.8,
        keyword_weight=1.0,
    )
    return rerank_candidates(query=query, candidates=merged, top_k=top_k)
