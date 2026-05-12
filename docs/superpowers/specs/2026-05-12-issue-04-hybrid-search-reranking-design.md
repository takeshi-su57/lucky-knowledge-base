# Issue 04 Hybrid Search and Reranking Design

## Goal
Improve retrieval relevance by combining dense retrieval with keyword retrieval, then reranking the merged set, while preserving a safe `vector_only` fallback.

## Scope Alignment
- In scope:
  - keyword retriever (BM25-style term scoring over chunks)
  - hybrid merge/dedupe
  - metadata filtering support across retrievers
  - reranker over merged candidates
  - retrieval strategy switch (`vector_only` vs `hybrid`)
- Out of scope:
  - web UI changes

## Proposed Architecture
1. Keep existing dense retrieval behavior as the baseline path.
2. Add a keyword retriever module that scores chunks by term overlap/IDF-like weighting.
3. Add a hybrid retriever module that:
   - fetches dense candidates
   - fetches keyword candidates
   - applies consistent metadata filters
   - merges and dedupes by chunk identity
4. Add a reranker module to refine merged candidate ordering with lexical + semantic signals.
5. Wire strategy selection in `pipeline.ask_question` and evaluation CLI so we can compare `vector_only` vs `hybrid`.

## Data Flow
1. Query enters `ask_question`.
2. Strategy decides retrieval mode:
   - `vector_only`: existing dense retrieval
   - `hybrid`: dense + keyword -> merge/dedupe -> rerank
3. Top chunks flow to answer and citation formatting unchanged.
4. Eval harness runs both strategies and computes:
   - `top5_accuracy_delta` (`hybrid - vector_only`)
   - exact-term query success on targeted query set.

## Error Handling and Compatibility
- Unknown strategy should raise a clear `ValueError`.
- If keyword retrieval yields no results, hybrid should still return dense path outputs.
- Existing `ask_question` call sites should continue working without code changes (`vector_only` default retained where needed).

## Test Strategy
- Unit:
  - keyword scoring behavior (exact terms/acronyms)
  - hybrid merge/dedupe ordering behavior
  - metadata filters
  - reranker prioritization behavior
- Integration:
  - end-to-end exact-term query retrieval behavior
- Eval:
  - compare `vector_only` vs `hybrid`
  - validate issue success metrics

## Success Metrics
- `top5_accuracy_delta >= +0.08` vs vector-only baseline
- `exact_term_query_success >= 0.90` on targeted suite

## Tradeoff Decision
Use deterministic, lightweight term scoring and reranking (no extra external dependencies) to keep deployment simple and reproducible for this phase.
