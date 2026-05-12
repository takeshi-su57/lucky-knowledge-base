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
