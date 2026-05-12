from lkb.models import ScoredChunk, Chunk
from lkb.embeddings import embed_text, cosine_like


def retrieve(query: str, chunks: list[Chunk], top_k: int = 5) -> list[ScoredChunk]:
    qv = embed_text(query)
    scored = [ScoredChunk(chunk=c, score=cosine_like(qv, embed_text(c.text))) for c in chunks]
    scored.sort(key=lambda row: row.score, reverse=True)
    return scored[:top_k]
