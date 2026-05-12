import tempfile
import unittest
from pathlib import Path

from lkb.pipeline import index_markdown_dir, rebuild_index
from lkb.store import get_sqlite_db_path, load_lineage


class IncrementalIndexingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.kb = self.root / "kb"
        self.kb.mkdir(parents=True, exist_ok=True)
        self.index_dir = self.root / "index"
        self.index_dir.mkdir(parents=True, exist_ok=True)

        (self.kb / "python.md").write_text(
            "# Python\n## Basics\nPython uses indentation to define blocks.\n",
            encoding="utf-8",
        )
        (self.kb / "git.md").write_text(
            "# Git\n## Branches\nA branch is an independent line of development.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_incremental_indexing_only_reembeds_changed_document(self):
        first = index_markdown_dir(self.kb, self.index_dir)
        second = index_markdown_dir(self.kb, self.index_dir)

        self.assertGreater(first.reembedded_chunks, 0)
        self.assertEqual(second.reembedded_chunks, 0)
        self.assertEqual(second.indexed_documents, 0)
        self.assertEqual(second.skipped_documents, 2)

        (self.kb / "git.md").write_text(
            "# Git\n## Branches\nA branch is a movable pointer to a commit.\n",
            encoding="utf-8",
        )
        third = index_markdown_dir(self.kb, self.index_dir)
        self.assertEqual(third.indexed_documents, 1)
        self.assertEqual(third.skipped_documents, 1)
        self.assertGreater(third.reembedded_chunks, 0)

    def test_rebuild_index_recreates_valid_state(self):
        initial = index_markdown_dir(self.kb, self.index_dir)
        rebuilt = rebuild_index(self.kb, self.index_dir)
        lineage = load_lineage(self.index_dir)

        self.assertGreater(initial.total_chunks, 0)
        self.assertEqual(rebuilt.skipped_documents, 0)
        self.assertEqual(rebuilt.indexed_documents, 2)
        self.assertGreaterEqual(len(lineage), rebuilt.total_chunks)
        self.assertTrue(get_sqlite_db_path(self.index_dir).exists())


if __name__ == "__main__":
    unittest.main()
