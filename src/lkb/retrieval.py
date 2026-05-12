from lkb.embeddings import cosine_like, embed_text
from lkb.models import Chunk, ScoredChunk


def retrieve(query: str, chunks: list[Chunk], top_k: int = 5) -> list[ScoredChunk]:
    qv = embed_text(query)
    scored = [
        ScoredChunk(
            chunk=c,
            score=cosine_like(qv, c.embedding if c.embedding is not None else embed_text(c.text)),
        )
        for c in chunks
    ]
    scored.sort(key=lambda row: row.score, reverse=True)
    return scored[:top_k]
