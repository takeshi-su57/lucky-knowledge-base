import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Avoid shadowing stdlib inspect by scripts/inspect.py when run as a script.
script_dir = str(Path(__file__).parent.resolve())
sys.path = [p for p in sys.path if str(Path(p).resolve()) != script_dir]

from lkb.eval_harness import (
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
    parser.add_argument("--update-baseline", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    index_markdown_dir(args.kb_dir, args.index_dir)
    questions = load_golden_questions(args.questions)
    ensure_minimum_coverage(questions, min_coverage=50)
    baseline_report = load_report(args.baseline)

    report = evaluate_questions(
        questions=questions,
        index_dir=args.index_dir,
        top_k=args.top_k,
        threshold=args.threshold,
        unknown_threshold=args.unknown_threshold,
        baseline_report=baseline_report,
    )

    args.report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    latest_json = args.report_dir / "latest.json"
    latest_md = args.report_dir / "latest.md"
    stamped_json = args.report_dir / f"eval-report-{stamp}.json"
    stamped_md = args.report_dir / f"eval-report-{stamp}.md"

    write_reports(report, latest_json, latest_md)
    write_reports(report, stamped_json, stamped_md)

    if args.update_baseline:
        args.baseline.parent.mkdir(parents=True, exist_ok=True)
        write_reports(report, args.baseline, args.baseline.with_suffix(".md"))

    print(f"eval_coverage={report['eval_coverage']}")
    for key, value in report["metrics"].items():
        print(f"{key}={value:.4f}")

    deltas = report["regression_vs_baseline"]
    print("regression_deltas:")
    for key, value in deltas.items():
        if value is None:
            print(f"  {key}=n/a")
        else:
            print(f"  {key}={value:+.4f}")

    print(f"failed_examples={len(report['failed_examples'])}")
    if report["failed_examples"]:
        print("failed_example_inspector:")
        for row in report["failed_examples"][: max(args.failed_limit, 0)]:
            print(
                f"  id={row['id']} reasons={','.join(row['failure_reasons'])} "
                f"expected={row['expected_sources']} retrieved={row['retrieved_sources']}"
            )

    print(f"report_json={latest_json}")
    print(f"report_markdown={latest_md}")
    print(f"stamped_json={stamped_json}")
    print(f"stamped_markdown={stamped_md}")
    if args.update_baseline:
        print(f"baseline_json={args.baseline}")
        print(f"baseline_markdown={args.baseline.with_suffix('.md')}")


if __name__ == "__main__":
    main()
