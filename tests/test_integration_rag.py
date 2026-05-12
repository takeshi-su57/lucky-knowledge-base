import tempfile
import unittest
from pathlib import Path

from lkb.pipeline import index_markdown_dir, ask_question


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.kb = self.root / "kb"
        self.kb.mkdir(parents=True, exist_ok=True)

        (self.kb / "python.md").write_text(
            "# Python\n## Basics\nPython uses indentation to define blocks.\n",
            encoding="utf-8",
        )
        (self.kb / "git.md").write_text(
            "# Git\n## Branches\nA branch is an independent line of development.\n",
            encoding="utf-8",
        )
        (self.kb / "topic-06.md").write_text(
            "# Topic 6\n## Key Point\nTopic 6 describes concept 6 and practical usage.\n",
            encoding="utf-8",
        )

        self.index_dir = self.root / "index"
        self.index_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_index_then_ask_returns_citations(self):
        index_markdown_dir(self.kb, self.index_dir)
        result = ask_question(
            "What is a branch?",
            self.index_dir,
            top_k=5,
            threshold=0.1,
        )
        self.assertNotEqual(result.answer, "I don't know based on the indexed notes.")
        self.assertGreaterEqual(len(result.citations), 1)

    def test_unknown_question_returns_explicit_unknown(self):
        index_markdown_dir(self.kb, self.index_dir)
        result = ask_question(
            "What is quantum chromodynamics color confinement?",
            self.index_dir,
            top_k=5,
            threshold=0.8,
        )
        self.assertEqual(result.answer, "I don't know based on the indexed notes.")

    def test_hybrid_strategy_improves_exact_term_query(self):
        index_markdown_dir(self.kb, self.index_dir)
        result = ask_question(
            "What does topic 06 describe?",
            self.index_dir,
            top_k=5,
            threshold=0.1,
            retrieval_strategy="hybrid",
        )
        self.assertTrue(result.top_chunks[0].chunk.source_path.endswith("kb\\topic-06.md"))


if __name__ == "__main__":
    unittest.main()
