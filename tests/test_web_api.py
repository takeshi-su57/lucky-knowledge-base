import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from lkb.api import create_app
from lkb.store import list_bad_answer_logs, list_feedback_events


class WebApiIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.kb = self.root / "kb"
        self.index_dir = self.root / "index"
        self.kb.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        (self.kb / "python.md").write_text(
            "# Python\n## Basics\nPython uses indentation to define blocks.\n",
            encoding="utf-8",
        )

        app = create_app(self.kb, self.index_dir)
        self.client = TestClient(app)

    def tearDown(self):
        self.tmp.cleanup()

    def test_chat_returns_answer_citations_and_retrieved_chunks(self):
        self.client.post("/reindex")
        response = self.client.post(
            "/chat",
            json={
                "question": "How does Python define blocks?",
                "top_k": 5,
                "threshold": 0.1,
                "retrieval_strategy": "hybrid",
            },
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("answer", payload)
        self.assertIn("citations", payload)
        self.assertIn("retrieved_chunks", payload)
        self.assertGreaterEqual(len(payload["citations"]), 1)
        self.assertGreaterEqual(len(payload["retrieved_chunks"]), 1)
        self.assertIsInstance(payload["query_id"], int)
        self.assertIsInstance(payload["answer_id"], int)

    def test_upload_reindex_then_ask_has_citation(self):
        upload = self.client.post(
            "/upload",
            files={"file": ("topic-99.md", b"# Topic 99\n## Key Point\nTopic 99 explains upload flow.\n", "text/markdown")},
        )
        self.assertEqual(upload.status_code, 200)

        reindex = self.client.post("/reindex")
        self.assertEqual(reindex.status_code, 200)
        self.assertGreaterEqual(reindex.json()["total_chunks"], 1)

        response = self.client.post(
            "/chat",
            json={
                "question": "What does topic 99 explain?",
                "top_k": 5,
                "threshold": 0.1,
                "retrieval_strategy": "hybrid",
            },
        )
        self.assertEqual(response.status_code, 200)
        citations = response.json()["citations"]
        self.assertTrue(any("topic-99.md" in c for c in citations))

    def test_feedback_persists_event_and_bad_answer_trace(self):
        self.client.post("/reindex")
        response = self.client.post(
            "/chat",
            json={
                "question": "How does Python define blocks?",
                "top_k": 5,
                "threshold": 0.1,
                "retrieval_strategy": "hybrid",
            },
        )
        payload = response.json()

        feedback = self.client.post(
            "/feedback",
            json={
                "answer_id": payload["answer_id"],
                "rating": -1,
                "comment": "This answer missed details.",
                "question": "How does Python define blocks?",
                "retrieved_chunks": payload["retrieved_chunks"],
                "answer": payload["answer"],
            },
        )
        self.assertEqual(feedback.status_code, 200)

        events = list_feedback_events(self.index_dir)
        bad_logs = list_bad_answer_logs(self.index_dir)
        self.assertGreaterEqual(len(events), 1)
        self.assertEqual(events[-1]["rating"], -1)
        self.assertGreaterEqual(len(bad_logs), 1)
        self.assertEqual(bad_logs[-1]["answer_id"], payload["answer_id"])


if __name__ == "__main__":
    unittest.main()

