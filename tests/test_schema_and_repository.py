import tempfile
import unittest
from pathlib import Path

from lkb.incremental import compute_content_hash, should_reindex
from lkb.store import (
    ensure_schema,
    get_sqlite_db_path,
    insert_or_update_document,
    replace_document_chunks,
    load_index,
    load_lineage,
)


class HashingTests(unittest.TestCase):
    def test_hash_changes_when_content_changes(self):
        h1 = compute_content_hash("hello")
        h2 = compute_content_hash("hello world")
        self.assertNotEqual(h1, h2)

    def test_should_reindex_logic(self):
        current = compute_content_hash("same")
        self.assertFalse(should_reindex(current, current))
        self.assertTrue(should_reindex(None, current))
        self.assertTrue(should_reindex("abc", current))


class RepositoryCrudTests(unittest.TestCase):
    def test_document_chunk_embedding_crud_and_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            index_dir = Path(tmp) / ".index"
            index_dir.mkdir(parents=True, exist_ok=True)

            ensure_schema(index_dir)
            doc = insert_or_update_document(
                index_dir=index_dir,
                source_path="kb/test.md",
                content_hash="hash-1",
                content="# Test\nBody",
            )
            replace_document_chunks(
                index_dir=index_dir,
                document_id=doc.id,
                chunks=[
                    {
                        "chunk_index": 0,
                        "heading_path": ["Test"],
                        "text": "Body text one",
                        "embedding": {"body": 1, "text": 1, "one": 1},
                    },
                    {
                        "chunk_index": 1,
                        "heading_path": ["Test"],
                        "text": "Body text two",
                        "embedding": {"body": 1, "text": 1, "two": 1},
                    },
                ],
            )

            chunks = load_index(index_dir)
            lineage = load_lineage(index_dir, source_path="kb/test.md")

            self.assertEqual(len(chunks), 2)
            self.assertEqual(len(lineage), 2)
            self.assertTrue(get_sqlite_db_path(index_dir).exists())
            self.assertTrue(all(row.embedding_id > 0 for row in lineage))


if __name__ == "__main__":
    unittest.main()
