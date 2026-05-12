# Issue 04 - Hybrid Search and Reranking

## Goal
Improve relevance by combining vector retrieval, keyword retrieval, and reranking.

## Scope
- In: BM25/FTS keyword retriever, merge/dedupe, metadata filters, reranker, retrieval strategy switch.
- Out: web UI changes.

## Deliverables
- `retrieval/keyword_retriever.py`
- `retrieval/hybrid_retriever.py`
- `retrieval/reranker.py`
- Config flags for `vector_only` vs `hybrid`

## Implementation Tasks
1. Implement keyword search index.
2. Merge dense + sparse candidates with dedupe.
3. Apply metadata filters consistently.
4. Add reranking on merged candidates.
5. Wire strategy selection and comparison.

## Tests
- Unit: merge/dedupe ordering behavior.
- Unit: metadata filters.
- Integration: exact-term queries with IDs/acronyms.
- Eval: compare vector-only vs hybrid on golden set.

## Definition of Done
- Hybrid beats vector-only on retrieval metrics.
- Exact-term queries improve materially.
- Reranking improves top-k source relevance.

## Success Metrics
- `top5_accuracy_delta >= +0.08` vs vector-only baseline.
- `exact_term_query_success >= 0.90` on targeted suite.

## Deployment
- Release tag: `v0.4.0-hybrid-rerank`
- Safe fallback toggle to vector-only retained.

---

## Implementation Status
Completed on branch `issue-04-hybrid-search-reranking-dev`.

## What Shipped
- Added retrieval package modules:
  - `src/lkb/retrieval/keyword_retriever.py`
  - `src/lkb/retrieval/hybrid_retriever.py`
  - `src/lkb/retrieval/reranker.py`
  - `src/lkb/retrieval/vector_retriever.py`
  - `src/lkb/retrieval/filters.py`
  - `src/lkb/retrieval/__init__.py`
- Converted legacy `src/lkb/retrieval.py` into package-based retrieval implementation.
- Added retrieval strategy switch in pipeline and CLI:
  - `src/lkb/pipeline.py`
  - `scripts/ask.py`
- Added strategy comparison + exact-term metric support in eval harness:
  - `src/lkb/eval_harness.py`
  - `scripts/run_eval.py`
- Added and updated tests:
  - `tests/test_hybrid_retrieval.py`
  - `tests/test_integration_rag.py`
  - `tests/test_eval_harness.py`

## Code Review Findings and Resolution
1. **Finding:** metadata filters were not applied consistently in vector strategy path in `ask_question`.
   - **Resolution:** switched vector path to `vector_retrieve(..., metadata_filters=...)` so filtering semantics are consistent across `vector_only` and `hybrid`.
2. **Finding:** compare-strategy eval path did not apply baseline deltas in hybrid report.
   - **Resolution:** added `baseline_report` plumbing through `compare_retrieval_strategies` and `scripts/run_eval.py`.

## Verification Evidence

### Unit + Integration Tests
Command:
```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests -v
```

Result:
- `Ran 21 tests in 14.556s`
- `OK`

### Eval Comparison (Vector vs Hybrid)
Command:
```powershell
$env:PYTHONPATH='src'; python scripts/run_eval.py --compare-strategies --exact-term-ids k6 k7 k8 k9 k26 k27 k28 k29 k46 k47 k48 k49 --top-k 5 --threshold 0.1 --unknown-threshold 0.8
```

Result:
- `vector_only top5_accuracy=0.7600`
- `hybrid top5_accuracy=1.0000`
- `top5_accuracy_delta=+0.2400`
- `vector_only exact_term_query_success=0.0000`
- `hybrid exact_term_query_success=1.0000`
- `failed_examples=0`
- report artifacts:
  - `evals/reports/latest.json`
  - `evals/reports/latest.md`
  - `evals/reports/eval-report-20260512-220315.json`
  - `evals/reports/eval-report-20260512-220315.md`

## Success Metrics
- `top5_accuracy_delta >= +0.08` vs vector-only baseline:
  - **Actual:** `+0.2400` ✅
- `exact_term_query_success >= 0.90` on targeted suite:
  - **Actual:** `1.0000` ✅

## Release Notes
- Added hybrid retrieval strategy (`hybrid`) that merges dense + keyword candidates and applies reranking.
- Added metadata filtering helper shared by retrieval paths.
- Added eval support for strategy comparison and exact-term query success tracking.
- Preserved existing safe fallback behavior with `vector_only` strategy.

## Migration / Config Changes
- New CLI flag on `scripts/ask.py`:
  - `--retrieval-strategy {vector_only,hybrid}` (default: `vector_only`)
- New eval CLI flags on `scripts/run_eval.py`:
  - `--retrieval-strategy {vector_only,hybrid}` (default: `hybrid`)
  - `--compare-strategies`
  - `--exact-term-ids <id...>`

## Rollback Path
1. Run questions with `--retrieval-strategy vector_only` for immediate operational fallback.
2. Revert commit(s) that introduce `src/lkb/retrieval/` package and strategy/eval wiring.
3. Re-run:
   - `python -m unittest discover -s tests -v`
   - `python scripts/run_eval.py --retrieval-strategy vector_only`
