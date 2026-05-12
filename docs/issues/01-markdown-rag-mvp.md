# Issue 01 - Markdown RAG MVP

## Goal
Ship a local CLI that answers questions over Markdown notes with citations.

## Scope
- In: Markdown ingestion, chunking, embeddings, vector retrieval, answer generation, CLI commands (`index`, `ask`, `inspect`).
- Out: Web UI, PDF/audio/video, background workers.

## Deliverables
- `scripts/index.py`, `scripts/ask.py`, `scripts/inspect.py`
- Local vector store + metadata for source file and heading path
- Prompt template enforcing grounded answers + unknown behavior

## Implementation Tasks
1. Add Markdown loader for `kb/*.md`.
2. Add heading-aware chunker with overlap.
3. Add embedding + vector persistence.
4. Build CLI query flow and citation rendering.
5. Build retrieval inspection output (top-k chunks + scores).

## Tests
- Unit: chunker boundaries, metadata correctness.
- Unit: citation formatter for markdown sources.
- Integration: index sample notes then ask seeded questions.
- Integration: unknown question returns explicit unknown response.

## Definition of Done
- 20+ Markdown files indexed.
- 30 manual eval questions documented.
- Top-5 contains expected source >= 80%.
- Answers include source citations.
- Unknown answers do not hallucinate.

## Success Metrics
- `retrieval_top5_accuracy >= 0.80`
- `unknown_answer_accuracy >= 0.90`
- `p95_query_latency <= 6s` on local dataset

## Deployment
- Local release tag: `v0.1.0-markdown-rag`
- Rollback: restore prior index snapshot directory.
