import unittest

from lkb.web_ui_helpers import citation_panel_render_success, format_chunk_rows


class WebUiSmokeTests(unittest.TestCase):
    def test_format_chunk_rows_includes_source_heading_and_score(self):
        rows = format_chunk_rows(
            [
                {
                    "source_path": "kb/topic-01.md",
                    "heading_path": ["Topic 1", "Overview"],
                    "score": 0.91,
                    "text": "Topic 1 summary text",
                }
            ]
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source"], "kb/topic-01.md")
        self.assertEqual(rows[0]["heading"], "Topic 1 > Overview")
        self.assertEqual(rows[0]["score"], "0.9100")

    def test_citation_panel_render_success_is_true_when_citations_exist(self):
        metric = citation_panel_render_success(
            [{"answer": "A", "citations": ["kb/topic-01.md#Topic 1 (score=0.9100)"]}]
        )
        self.assertEqual(metric, 1.0)

    def test_citation_panel_render_success_is_zero_when_missing(self):
        metric = citation_panel_render_success(
            [{"answer": "A", "citations": []}, {"answer": "B", "citations": []}]
        )
        self.assertEqual(metric, 0.0)


if __name__ == "__main__":
    unittest.main()

