import unittest

from lkb.embeddings import embed_text
from lkb.models import Chunk, ScoredChunk


def _chunk(source_path: str, text: str, chunk_id: int) -> Chunk:
    return Chunk(
        source_path=source_path,
        heading_path=["H"],
        text=text,
        chunk_id=chunk_id,
        embedding=dict(embed_text(text)),
    )


class KeywordRetrieverTests(unittest.TestCase):
    def test_keyword_retriever_prefers_exact_topic_id_with_zero_padded_query(self):
        from lkb.retrieval.keyword_retriever import keyword_retrieve

        chunks = [
            _chunk("kb/topic-01.md", "Topic 1 describes concept 1 and practical usage.", 1),
            _chunk("kb/topic-06.md", "Topic 6 describes concept 6 and practical usage.", 2),
        ]

        scored = keyword_retrieve("What does topic 06 describe?", chunks, top_k=2)

        self.assertEqual(scored[0].chunk.source_path, "kb/topic-06.md")


class HybridRetrieverTests(unittest.TestCase):
    def test_merge_and_dedupe_prefers_better_duplicate_score(self):
        from lkb.retrieval.hybrid_retriever import merge_and_dedupe_candidates

        shared = _chunk("kb/topic-06.md", "Topic 6 describes concept 6.", 6)
        other = _chunk("kb/topic-02.md", "Topic 2 describes concept 2.", 2)

        dense = [
            ScoredChunk(chunk=shared, score=0.35),
            ScoredChunk(chunk=other, score=0.30),
        ]
        keyword = [
            ScoredChunk(chunk=shared, score=0.85),
        ]

        merged = merge_and_dedupe_candidates(dense, keyword, top_k=5)

        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0].chunk.source_path, "kb/topic-06.md")
        self.assertGreaterEqual(merged[0].score, 0.85)

    def test_hybrid_retriever_applies_source_path_filter(self):
        from lkb.retrieval.hybrid_retriever import hybrid_retrieve

        chunks = [
            _chunk("kb/topic-01.md", "Topic 1 describes concept 1 and practical usage.", 1),
            _chunk("kb/topic-06.md", "Topic 6 describes concept 6 and practical usage.", 6),
        ]

        scored = hybrid_retrieve(
            "What does topic 06 describe?",
            chunks,
            top_k=5,
            metadata_filters={"source_paths": ["kb/topic-06.md"]},
        )

        self.assertEqual(len(scored), 1)
        self.assertEqual(scored[0].chunk.source_path, "kb/topic-06.md")


class RerankerTests(unittest.TestCase):
    def test_reranker_prioritizes_exact_numeric_match(self):
        from lkb.retrieval.reranker import rerank_candidates

        candidates = [
            ScoredChunk(
                chunk=_chunk("kb/topic-01.md", "Topic 1 describes concept 1 and practical usage.", 1),
                score=0.40,
            ),
            ScoredChunk(
                chunk=_chunk("kb/topic-06.md", "Topic 6 describes concept 6 and practical usage.", 6),
                score=0.35,
            ),
        ]

        reranked = rerank_candidates("What does topic 06 describe?", candidates, top_k=2)
        self.assertEqual(reranked[0].chunk.source_path, "kb/topic-06.md")


if __name__ == "__main__":
    unittest.main()
