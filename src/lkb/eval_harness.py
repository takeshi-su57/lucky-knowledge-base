import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from lkb.models import AskResult
from lkb.pipeline import UNKNOWN_ANSWER, ask_question


@dataclass(frozen=True)
class GoldenQuestion:
    qid: str
    question: str
    expected_sources: list[str]
    expect_unknown: bool


def load_golden_questions(path: Path) -> list[GoldenQuestion]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    questions: list[GoldenQuestion] = []
    for idx, row in enumerate(data):
        qid = str(row.get("id", f"q{idx+1}"))
        question = str(row["question"])
        expected_sources = [str(source) for source in row.get("expected_sources", [])]
        expect_unknown = bool(row.get("expect_unknown", False))
        questions.append(
            GoldenQuestion(
                qid=qid,
                question=question,
                expected_sources=expected_sources,
                expect_unknown=expect_unknown,
            )
        )
    return questions


def ensure_minimum_coverage(questions: list[GoldenQuestion], min_coverage: int = 50) -> None:
    if len(questions) < min_coverage:
        raise ValueError(
            f"Golden question coverage is below requirement: {len(questions)} < {min_coverage}"
        )


def _compute_rank(retrieved_sources: list[str], expected_sources: list[str]) -> int | None:
    normalized_expected = {_normalize_path(source) for source in expected_sources}
    for i, source in enumerate(retrieved_sources, start=1):
        if _normalize_path(source) in normalized_expected:
            return i
    return None


def _normalize_path(value: str) -> str:
    return value.replace("\\", "/")


def _compute_regression(
    metrics: dict[str, float],
    baseline_report: dict | None,
) -> dict[str, float | None]:
    baseline_metrics = {}
    if baseline_report:
        baseline_metrics = baseline_report.get("metrics", {})
    deltas: dict[str, float | None] = {}
    for key in (
        "top1_accuracy",
        "top3_accuracy",
        "top5_accuracy",
        "mrr",
        "citation_accuracy",
        "unknown_answer_accuracy",
        "exact_term_query_success",
    ):
        baseline_value = baseline_metrics.get(key)
        deltas[f"{key}_delta"] = None if baseline_value is None else float(metrics[key] - baseline_value)
    return deltas


def evaluate_questions(
    questions: list[GoldenQuestion],
    index_dir: Path,
    ask_fn: Callable[..., AskResult] = ask_question,
    top_k: int = 5,
    threshold: float = 0.1,
    unknown_threshold: float = 0.8,
    baseline_report: dict | None = None,
    retrieval_strategy: str = "vector_only",
    exact_term_ids: set[str] | None = None,
) -> dict:
    answerable_total = 0
    top1_hits = 0
    top3_hits = 0
    top5_hits = 0
    mrr_total = 0.0
    citation_hits = 0
    unknown_total = 0
    unknown_correct = 0
    exact_term_total = 0
    exact_term_success = 0
    failed_examples: list[dict] = []

    for row in questions:
        use_threshold = unknown_threshold if row.expect_unknown else threshold
        try:
            result = ask_fn(
                row.question,
                index_dir,
                top_k=top_k,
                threshold=use_threshold,
                retrieval_strategy=retrieval_strategy,
            )
        except TypeError:
            result = ask_fn(row.question, index_dir, top_k=top_k, threshold=use_threshold)
        retrieved_sources = [scored.chunk.source_path for scored in result.top_chunks[:top_k]]
        failure_reasons: list[str] = []

        if row.expect_unknown:
            unknown_total += 1
            is_unknown_correct = result.answer.strip() == UNKNOWN_ANSWER
            if is_unknown_correct:
                unknown_correct += 1
            else:
                failure_reasons.append("unknown_answer_miss")
        else:
            answerable_total += 1
            rank = _compute_rank(retrieved_sources, row.expected_sources)
            if rank is not None:
                if rank <= 1:
                    top1_hits += 1
                if rank <= 3:
                    top3_hits += 1
                if rank <= 5:
                    top5_hits += 1
                mrr_total += 1.0 / rank
            else:
                failure_reasons.append("retrieval_miss")

            if exact_term_ids and row.qid in exact_term_ids:
                exact_term_total += 1
                if rank is not None:
                    exact_term_success += 1

            citation_match = any(
                _normalize_path(expected) in _normalize_path(citation)
                for expected in row.expected_sources
                for citation in result.citations
            )
            if citation_match:
                citation_hits += 1
            else:
                failure_reasons.append("citation_miss")

        if failure_reasons:
            failed_examples.append(
                {
                    "id": row.qid,
                    "question": row.question,
                    "failure_reasons": failure_reasons,
                    "expected_sources": row.expected_sources,
                    "retrieved_sources": retrieved_sources,
                    "citations": result.citations,
                    "answer_preview": result.answer[:200],
                }
            )

    metrics = {
        "top1_accuracy": (top1_hits / answerable_total) if answerable_total else 0.0,
        "top3_accuracy": (top3_hits / answerable_total) if answerable_total else 0.0,
        "top5_accuracy": (top5_hits / answerable_total) if answerable_total else 0.0,
        "mrr": (mrr_total / answerable_total) if answerable_total else 0.0,
        "citation_accuracy": (citation_hits / answerable_total) if answerable_total else 0.0,
        "unknown_answer_accuracy": (unknown_correct / unknown_total) if unknown_total else 1.0,
        "exact_term_query_success": (exact_term_success / exact_term_total) if exact_term_total else 1.0,
    }

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "eval_coverage": len(questions),
        "metrics": metrics,
        "regression_vs_baseline": _compute_regression(metrics, baseline_report),
        "failed_examples": failed_examples,
    }


def compare_retrieval_strategies(
    questions: list[GoldenQuestion],
    index_dir: Path,
    ask_fn: Callable[..., AskResult] = ask_question,
    top_k: int = 5,
    threshold: float = 0.1,
    unknown_threshold: float = 0.8,
    exact_term_ids: set[str] | None = None,
    baseline_report: dict | None = None,
) -> dict:
    vector_report = evaluate_questions(
        questions=questions,
        index_dir=index_dir,
        ask_fn=ask_fn,
        top_k=top_k,
        threshold=threshold,
        unknown_threshold=unknown_threshold,
        retrieval_strategy="vector_only",
        exact_term_ids=exact_term_ids,
    )
    hybrid_report = evaluate_questions(
        questions=questions,
        index_dir=index_dir,
        ask_fn=ask_fn,
        top_k=top_k,
        threshold=threshold,
        unknown_threshold=unknown_threshold,
        baseline_report=baseline_report,
        retrieval_strategy="hybrid",
        exact_term_ids=exact_term_ids,
    )
    top5_delta = hybrid_report["metrics"]["top5_accuracy"] - vector_report["metrics"]["top5_accuracy"]
    return {
        "generated_at": hybrid_report["generated_at"],
        "eval_coverage": hybrid_report["eval_coverage"],
        "top5_accuracy_delta": float(top5_delta),
        "vector_only": vector_report,
        "hybrid": hybrid_report,
    }


def format_markdown_report(report: dict) -> str:
    metrics = report["metrics"]
    deltas = report["regression_vs_baseline"]
    lines = [
        "# Retrieval Eval Report",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Eval coverage: `{report['eval_coverage']}` questions",
        "",
        "## Metrics",
        "",
        "| Metric | Value | Delta vs baseline |",
        "|---|---:|---:|",
    ]
    metric_keys = (
        "top1_accuracy",
        "top3_accuracy",
        "top5_accuracy",
        "mrr",
        "citation_accuracy",
        "unknown_answer_accuracy",
        "exact_term_query_success",
    )
    for key in metric_keys:
        value = f"{metrics[key]:.4f}"
        delta = deltas[f"{key}_delta"]
        delta_cell = "n/a" if delta is None else f"{delta:+.4f}"
        lines.append(f"| `{key}` | {value} | {delta_cell} |")

    lines.extend(["", "## Failed Examples", ""])
    if not report["failed_examples"]:
        lines.append("No failures detected.")
    else:
        for example in report["failed_examples"]:
            lines.extend(
                [
                    f"### {example['id']}: {example['question']}",
                    f"- reasons: `{', '.join(example['failure_reasons'])}`",
                    f"- expected_sources: `{example['expected_sources']}`",
                    f"- retrieved_sources: `{example['retrieved_sources']}`",
                    f"- citations: `{example['citations']}`",
                    f"- answer_preview: `{example['answer_preview']}`",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def load_report(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_reports(report: dict, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(format_markdown_report(report), encoding="utf-8")
