import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Avoid shadowing stdlib inspect by scripts/inspect.py when run as a script.
script_dir = str(Path(__file__).parent.resolve())
sys.path = [p for p in sys.path if str(Path(p).resolve()) != script_dir]

from lkb.eval_harness import (
    compare_retrieval_strategies,
    ensure_minimum_coverage,
    evaluate_questions,
    load_golden_questions,
    load_report,
    write_reports,
)
from lkb.pipeline import index_markdown_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run retrieval evaluation harness.")
    parser.add_argument("--kb-dir", type=Path, default=Path("kb"))
    parser.add_argument("--index-dir", type=Path, default=Path(".index"))
    parser.add_argument("--questions", type=Path, default=Path("evals/test_questions.yaml"))
    parser.add_argument("--report-dir", type=Path, default=Path("evals/reports"))
    parser.add_argument("--baseline", type=Path, default=Path("evals/baseline_report.json"))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--threshold", type=float, default=0.1)
    parser.add_argument("--unknown-threshold", type=float, default=0.8)
    parser.add_argument("--failed-limit", type=int, default=10)
    parser.add_argument("--retrieval-strategy", choices=["vector_only", "hybrid"], default="hybrid")
    parser.add_argument("--compare-strategies", action="store_true")
    parser.add_argument("--exact-term-ids", nargs="*", default=[])
    parser.add_argument("--update-baseline", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    index_markdown_dir(args.kb_dir, args.index_dir)
    questions = load_golden_questions(args.questions)
    ensure_minimum_coverage(questions, min_coverage=50)
    baseline_report = load_report(args.baseline)

    exact_term_ids = {str(qid) for qid in args.exact_term_ids}
    report: dict
    if args.compare_strategies:
        report = compare_retrieval_strategies(
            questions=questions,
            index_dir=args.index_dir,
            top_k=args.top_k,
            threshold=args.threshold,
            unknown_threshold=args.unknown_threshold,
            exact_term_ids=exact_term_ids if exact_term_ids else None,
            baseline_report=baseline_report,
        )
        # For file compatibility, store hybrid report shape in latest files.
        write_target = report["hybrid"]
    else:
        report = evaluate_questions(
            questions=questions,
            index_dir=args.index_dir,
            top_k=args.top_k,
            threshold=args.threshold,
            unknown_threshold=args.unknown_threshold,
            baseline_report=baseline_report,
            retrieval_strategy=args.retrieval_strategy,
            exact_term_ids=exact_term_ids if exact_term_ids else None,
        )
        write_target = report

    args.report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    latest_json = args.report_dir / "latest.json"
    latest_md = args.report_dir / "latest.md"
    stamped_json = args.report_dir / f"eval-report-{stamp}.json"
    stamped_md = args.report_dir / f"eval-report-{stamp}.md"

    write_reports(write_target, latest_json, latest_md)
    write_reports(write_target, stamped_json, stamped_md)

    if args.update_baseline:
        args.baseline.parent.mkdir(parents=True, exist_ok=True)
        write_reports(write_target, args.baseline, args.baseline.with_suffix(".md"))

    print(f"eval_coverage={report['eval_coverage']}")
    if args.compare_strategies:
        vector_metrics = report["vector_only"]["metrics"]
        hybrid_metrics = report["hybrid"]["metrics"]
        print("vector_only_metrics:")
        for key, value in vector_metrics.items():
            print(f"  {key}={value:.4f}")
        print("hybrid_metrics:")
        for key, value in hybrid_metrics.items():
            print(f"  {key}={value:.4f}")
        print(f"top5_accuracy_delta={report['top5_accuracy_delta']:+.4f}")
        deltas = report["hybrid"]["regression_vs_baseline"]
        print("hybrid_regression_deltas:")
        for key, value in deltas.items():
            if value is None:
                print(f"  {key}=n/a")
            else:
                print(f"  {key}={value:+.4f}")
        failed_examples = report["hybrid"]["failed_examples"]
    else:
        for key, value in report["metrics"].items():
            print(f"{key}={value:.4f}")
        deltas = report["regression_vs_baseline"]
        print("regression_deltas:")
        for key, value in deltas.items():
            if value is None:
                print(f"  {key}=n/a")
            else:
                print(f"  {key}={value:+.4f}")
        failed_examples = report["failed_examples"]

    print(f"failed_examples={len(failed_examples)}")
    if failed_examples:
        print("failed_example_inspector:")
        for row in failed_examples[: max(args.failed_limit, 0)]:
            print(
                f"  id={row['id']} reasons={','.join(row['failure_reasons'])} "
                f"expected={row['expected_sources']} retrieved={row['retrieved_sources']}"
            )

    if args.compare_strategies:
        print(f"strategy_comparison=true")
        print(f"report_json={latest_json}")
        print(f"report_markdown={latest_md}")
        print(f"stamped_json={stamped_json}")
        print(f"stamped_markdown={stamped_md}")
        if args.update_baseline:
            print(f"baseline_json={args.baseline}")
            print(f"baseline_markdown={args.baseline.with_suffix('.md')}")
        return

    print(f"report_json={latest_json}")
    print(f"report_markdown={latest_md}")
    print(f"stamped_json={stamped_json}")
    print(f"stamped_markdown={stamped_md}")
    if args.update_baseline:
        print(f"baseline_json={args.baseline}")
        print(f"baseline_markdown={args.baseline.with_suffix('.md')}")


if __name__ == "__main__":
    main()
