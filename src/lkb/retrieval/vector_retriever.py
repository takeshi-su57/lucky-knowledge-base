from lkb.embeddings import cosine_like, embed_text
from lkb.models import Chunk, ScoredChunk
from lkb.retrieval.filters import apply_metadata_filters


def vector_retrieve(
    query: str,
    chunks: list[Chunk],
    top_k: int = 5,
    metadata_filters: dict | None = None,
) -> list[ScoredChunk]:
    filtered_chunks = apply_metadata_filters(chunks, metadata_filters=metadata_filters)
    qv = embed_text(query)
    scored = [
        ScoredChunk(
            chunk=chunk,
            score=cosine_like(
                qv,
                chunk.embedding if chunk.embedding is not None else embed_text(chunk.text),
            ),
        )
        for chunk in filtered_chunks
    ]
    scored.sort(key=lambda row: row.score, reverse=True)
    return scored[:top_k]


def retrieve(query: str, chunks: list[Chunk], top_k: int = 5) -> list[ScoredChunk]:
    return vector_retrieve(query=query, chunks=chunks, top_k=top_k, metadata_filters=None)
