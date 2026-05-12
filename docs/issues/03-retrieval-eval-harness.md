# Issue 03 - Retrieval Evaluation Harness

## Goal
Make retrieval quality measurable and regressions visible.

## Scope
- In: golden questions dataset, eval runner, retrieval and answer metrics report.
- Out: production observability stack.

## Deliverables
Implemented:
- `evals/test_questions.yaml` (55 golden questions: 50 answerable + 5 unknown)
- `scripts/run_eval.py`
- `src/lkb/eval_harness.py`
- `evals/baseline_report.json`
- `evals/baseline_report.md`
- `evals/reports/latest.json`
- `evals/reports/latest.md`
- `tests/test_eval_harness.py`

## Implementation Tasks
Completed:
1. Added 55 golden questions in `evals/test_questions.yaml` to satisfy `eval_coverage >= 50`.
2. Implemented retrieval metrics `top1_accuracy`, `top3_accuracy`, `top5_accuracy`, and `mrr`.
3. Added `citation_accuracy` and `unknown_answer_accuracy` checks.
4. Added baseline regression deltas for all key metrics against `evals/baseline_report.json`.
5. Added failed-example inspector output in JSON/Markdown reports and CLI output.

Additional implementation details:
- Added path normalization for `\` vs `/` so retrieval/citation scoring is stable across Windows path formatting.
- Added minimum coverage guard that raises an error if fewer than 50 golden questions are supplied.
- Added question-type thresholding (`threshold` for answerable, `unknown_threshold` for unknown prompts).

## Tests
- Unit: metric calculations and path normalization (`tests/test_eval_harness.py::EvalHarnessUnitTests`).
- Integration: eval harness run on seeded mini corpus (`tests/test_eval_harness.py::EvalHarnessIntegrationTests::test_eval_runner_on_seeded_mini_corpus`).
- Contract: report schema stability (`tests/test_eval_harness.py::EvalHarnessUnitTests::test_report_schema_contract_stability`).
- Contract: coverage guard (`tests/test_eval_harness.py::EvalHarnessUnitTests::test_coverage_guard_requires_at_least_50_questions`).
- Backward compatibility: full existing test suite remains green.

### Verification Commands and Outputs
- Command: `PYTHONPATH=src python -m unittest discover -s tests -v`
  - Result: `Ran 15 tests ... OK`
- Command: `PYTHONPATH=src python scripts/run_eval.py`
  - Result:
    - `eval_coverage=55`
    - `top1_accuracy=0.5200`
    - `top3_accuracy=0.6400`
    - `top5_accuracy=0.7600`
    - `mrr=0.5970`
    - `citation_accuracy=0.7600`
    - `unknown_answer_accuracy=1.0000`
    - Regression deltas present for all key metrics (`*_delta`)
    - `failed_examples=12` with inspector lines printed

## Definition of Done
Status:
- Eval command prints and stores all core metrics: achieved (`scripts/run_eval.py` writes JSON + Markdown reports and prints metrics).
- Bad retrieval examples are explorable: achieved (`failed_examples` in reports + CLI failed-example inspector output).
- Any retrieval/prompt change can be compared to baseline: achieved (baseline load + metric deltas).

## Success Metrics
Measured:
- `eval_coverage >= 50`: achieved (`55`).
- Report generation pass rate `100%` in local check: achieved (`python scripts/run_eval.py` exited 0 and produced reports).
- Baseline comparison includes deltas for all key metrics: achieved (`top1/top3/top5/mrr/citation/unknown` delta keys present).

## Code Review Findings (Step 5/6)
Findings captured and resolved during implementation:
1. Important: source-path separator mismatch (`/` vs `\`) caused false retrieval misses in metrics.
   - Resolution: normalized paths in rank and citation matching logic.
   - Guard: `test_metrics_normalize_path_separators`.
2. Important: eval harness did not enforce Issue 03 minimum coverage requirement.
   - Resolution: added `ensure_minimum_coverage(..., min_coverage=50)` and wired it into runner.
   - Guard: `test_coverage_guard_requires_at_least_50_questions`.
3. Important: script import path collision (`scripts/inspect.py` shadowed stdlib `inspect`) when running `scripts/run_eval.py`.
   - Resolution: mirrored existing script pattern to remove script directory from `sys.path` before imports.

## Deployment
- Release tag: `v0.3.0-eval-harness`
- Baseline report committed for future diffing: `evals/baseline_report.json`.

## Release Notes
### What shipped
- New eval harness module with golden dataset loader, metric computations, baseline comparisons, and report rendering.
- New CLI runner for repeatable retrieval evaluation.
- Golden question dataset with 55 prompts.
- Baseline and latest reports in JSON + Markdown.
- Tests covering metrics, contract schema, integration flow, and coverage guard.

### Migration/config changes
- New command:
  - `PYTHONPATH=src python scripts/run_eval.py`
- Optional CLI flags:
  - `--questions`, `--report-dir`, `--baseline`
  - `--threshold`, `--unknown-threshold`
  - `--update-baseline`
- New eval artifact directories:
  - `evals/`
  - `evals/reports/`

### Rollback path
- Remove eval harness additions:
  - `scripts/run_eval.py`
  - `src/lkb/eval_harness.py`
  - `tests/test_eval_harness.py`
  - `evals/`
- Restore previous commit state of `docs/issues/03-retrieval-eval-harness.md`.
