import json
import tempfile
import unittest
from pathlib import Path

from lkb.models import AskResult, Chunk, ScoredChunk
from lkb.pipeline import UNKNOWN_ANSWER, index_markdown_dir


def _make_result(paths: list[str], answer: str | None = None, citations: list[str] | None = None) -> AskResult:
    scored = [
        ScoredChunk(
            chunk=Chunk(source_path=path, heading_path=["H"], text=f"text for {path}", chunk_id=i + 1, embedding={}),
            score=1.0 - (i * 0.1),
        )
        for i, path in enumerate(paths)
    ]
    if answer is None:
        answer = UNKNOWN_ANSWER if not paths else scored[0].chunk.text
    if citations is None:
        citations = [f"{row.chunk.source_path} :: {row.chunk.chunk_id}" for row in scored]
    return AskResult(answer=answer, citations=citations, top_chunks=scored)


class EvalHarnessUnitTests(unittest.TestCase):
    def test_metrics_topk_mrr_citation_unknown(self):
        from lkb.eval_harness import GoldenQuestion, evaluate_questions

        questions = [
            GoldenQuestion(
                qid="q1",
                question="q1",
                expected_sources=["kb/a.md"],
                expect_unknown=False,
            ),
            GoldenQuestion(
                qid="q2",
                question="q2",
                expected_sources=["kb/b.md"],
                expect_unknown=False,
            ),
            GoldenQuestion(
                qid="q3",
                question="q3",
                expected_sources=["kb/miss.md"],
                expect_unknown=False,
            ),
            GoldenQuestion(
                qid="q4",
                question="q4",
                expected_sources=[],
                expect_unknown=True,
            ),
        ]

        answers = {
            "q1": _make_result(paths=["kb/a.md", "kb/x.md"]),
            "q2": _make_result(paths=["kb/x.md", "kb/b.md"]),
            "q3": _make_result(paths=["kb/x.md", "kb/y.md"], citations=["kb/z.md :: 3"]),
            "q4": _make_result(paths=[], answer=UNKNOWN_ANSWER, citations=[]),
        }

        def fake_ask(question: str, _index_dir: Path, top_k: int = 5, threshold: float = 0.2) -> AskResult:
            del top_k, threshold
            return answers[question]

        report = evaluate_questions(
            questions=questions,
            index_dir=Path("."),
            ask_fn=fake_ask,
            top_k=5,
            threshold=0.2,
        )

        self.assertEqual(report["eval_coverage"], 4)
        metrics = report["metrics"]
        self.assertAlmostEqual(metrics["top1_accuracy"], 1 / 3, places=6)
        self.assertAlmostEqual(metrics["top3_accuracy"], 2 / 3, places=6)
        self.assertAlmostEqual(metrics["top5_accuracy"], 2 / 3, places=6)
        self.assertAlmostEqual(metrics["mrr"], 0.5, places=6)
        self.assertAlmostEqual(metrics["citation_accuracy"], 2 / 3, places=6)
        self.assertAlmostEqual(metrics["unknown_answer_accuracy"], 1.0, places=6)
        self.assertEqual(len(report["failed_examples"]), 1)

    def test_metrics_normalize_path_separators(self):
        from lkb.eval_harness import GoldenQuestion, evaluate_questions

        report = evaluate_questions(
            questions=[
                GoldenQuestion(
                    qid="q1",
                    question="q1",
                    expected_sources=["kb/topic-01.md"],
                    expect_unknown=False,
                )
            ],
            index_dir=Path("."),
            ask_fn=lambda *_args, **_kwargs: _make_result(paths=["kb\\topic-01.md"]),
            top_k=5,
            threshold=0.2,
        )

        self.assertAlmostEqual(report["metrics"]["top1_accuracy"], 1.0, places=6)
        self.assertAlmostEqual(report["metrics"]["citation_accuracy"], 1.0, places=6)

    def test_report_schema_contract_stability(self):
        from lkb.eval_harness import GoldenQuestion, evaluate_questions, format_markdown_report

        questions = [
            GoldenQuestion(
                qid="q1",
                question="q1",
                expected_sources=["kb/a.md"],
                expect_unknown=False,
            )
        ]

        report = evaluate_questions(
            questions=questions,
            index_dir=Path("."),
            ask_fn=lambda *_args, **_kwargs: _make_result(paths=["kb/a.md"]),
            top_k=5,
            threshold=0.2,
        )

        expected_top_keys = {
            "generated_at",
            "eval_coverage",
            "metrics",
            "regression_vs_baseline",
            "failed_examples",
        }
        self.assertEqual(set(report.keys()), expected_top_keys)
        self.assertEqual(
            set(report["metrics"].keys()),
            {
                "top1_accuracy",
                "top3_accuracy",
                "top5_accuracy",
                "mrr",
                "citation_accuracy",
                "unknown_answer_accuracy",
            },
        )
        self.assertEqual(
            set(report["regression_vs_baseline"].keys()),
            {
                "top1_accuracy_delta",
                "top3_accuracy_delta",
                "top5_accuracy_delta",
                "mrr_delta",
                "citation_accuracy_delta",
                "unknown_answer_accuracy_delta",
            },
        )
        md = format_markdown_report(report)
        self.assertIn("## Metrics", md)
        self.assertIn("## Failed Examples", md)

    def test_coverage_guard_requires_at_least_50_questions(self):
        from lkb.eval_harness import GoldenQuestion, ensure_minimum_coverage

        questions = [
            GoldenQuestion(
                qid="q1",
                question="q1",
                expected_sources=["kb/a.md"],
                expect_unknown=False,
            )
        ]

        with self.assertRaises(ValueError):
            ensure_minimum_coverage(questions, min_coverage=50)


class EvalHarnessIntegrationTests(unittest.TestCase):
    def test_eval_runner_on_seeded_mini_corpus(self):
        from lkb.eval_harness import evaluate_questions, load_golden_questions

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kb = root / "kb"
            kb.mkdir(parents=True, exist_ok=True)
            (kb / "python.md").write_text("# Python\n## Basics\nPython uses indentation.\n", encoding="utf-8")
            (kb / "git.md").write_text("# Git\n## Branches\nA branch is a line of development.\n", encoding="utf-8")

            index_dir = root / ".index"
            index_dir.mkdir(parents=True, exist_ok=True)
            index_markdown_dir(kb, index_dir)

            dataset_path = root / "questions.yaml"
            dataset_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "k1",
                            "question": "What uses indentation?",
                            "expected_sources": ["kb/python.md"],
                            "expect_unknown": False,
                        },
                        {
                            "id": "k2",
                            "question": "What is a branch?",
                            "expected_sources": ["kb/git.md"],
                            "expect_unknown": False,
                        },
                        {
                            "id": "u1",
                            "question": "What is the capital of Mars colony one?",
                            "expected_sources": [],
                            "expect_unknown": True,
                        },
                    ]
                ),
                encoding="utf-8",
            )

            questions = load_golden_questions(dataset_path)
            report = evaluate_questions(questions=questions, index_dir=index_dir, top_k=5, threshold=0.8)

            self.assertEqual(report["eval_coverage"], 3)
            self.assertIn("top5_accuracy", report["metrics"])
            self.assertGreaterEqual(report["metrics"]["unknown_answer_accuracy"], 0.0)


if __name__ == "__main__":
    unittest.main()
