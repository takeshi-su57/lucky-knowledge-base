import tempfile
import unittest
from pathlib import Path

from lkb.markdown import load_markdown_documents
from lkb.chunking import chunk_markdown_document


class MarkdownChunkingTests(unittest.TestCase):
    def test_loader_reads_only_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("# A\nhello", encoding="utf-8")
            (root / "b.txt").write_text("ignore", encoding="utf-8")
            docs = load_markdown_documents(root)
            self.assertEqual(len(docs), 1)
            self.assertEqual(docs[0].source_path.name, "a.md")

    def test_chunker_preserves_heading_path_and_overlap(self):
        text = "# Top\n## Child\n" + "word " * 80
        chunks = chunk_markdown_document(
            source_path=Path("kb/test.md"),
            content=text,
            chunk_size=30,
            overlap=5,
        )

        self.assertGreaterEqual(len(chunks), 2)
        self.assertEqual(chunks[0].heading_path, ["Top", "Child"])
        self.assertEqual(chunks[1].text.split()[:5], chunks[0].text.split()[-5:])


if __name__ == "__main__":
    unittest.main()
