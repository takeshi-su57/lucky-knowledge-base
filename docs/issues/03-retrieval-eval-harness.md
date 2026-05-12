# Issue 03 - Retrieval Evaluation Harness

## Goal
Make retrieval quality measurable and regressions visible.

## Scope
- In: golden questions dataset, eval runner, retrieval and answer metrics report.
- Out: production observability stack.

## Deliverables
- `evals/test_questions.yaml`
- `scripts/run_eval.py`
- Machine-readable + markdown eval reports

## Implementation Tasks
1. Add at least 50 golden questions.
2. Implement top-1/top-3/top-5 and MRR metrics.
3. Add citation and unknown-answer accuracy checks.
4. Add regression comparison against previous baseline report.
5. Add failed-example inspector output.

## Tests
- Unit: metric calculations.
- Integration: eval runner on seeded mini corpus.
- Contract: report schema stability test.

## Definition of Done
- Eval command prints and stores all core metrics.
- Bad retrieval examples are explorable.
- Any retrieval/prompt change can be compared to baseline.

## Success Metrics
- `eval_coverage >= 50` questions.
- Report generation pass rate `100%` in CI/local check.
- Baseline comparison includes deltas for all key metrics.

## Deployment
- Release tag: `v0.3.0-eval-harness`
- Baseline report committed for future diffing.
