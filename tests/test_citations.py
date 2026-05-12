import unittest

from lkb.citations import format_citation


class CitationTests(unittest.TestCase):
    def test_markdown_citation_format(self):
        citation = format_citation("kb/topic.md", ["A", "B"], 0.91)
        self.assertIn("kb/topic.md", citation)
        self.assertIn("A > B", citation)
        self.assertIn("0.91", citation)


if __name__ == "__main__":
    unittest.main()
