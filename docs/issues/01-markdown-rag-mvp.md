# Issue 01 - Markdown RAG MVP

## Goal
Ship a local CLI that answers questions over Markdown notes with citations.

## Scope
- In: Markdown ingestion, chunking, embeddings, vector retrieval, answer generation, CLI commands (`index`, `ask`, `inspect`).
- Out: Web UI, PDF/audio/video, background workers.

## Deliverables
Implemented:
- `scripts/index.py`
- `scripts/ask.py`
- `scripts/inspect.py`
- `scripts/eval_issue01.py`
- `src/lkb/markdown.py`
- `src/lkb/chunking.py`
- `src/lkb/embeddings.py`
- `src/lkb/store.py`
- `src/lkb/retrieval.py`
- `src/lkb/citations.py`
- `src/lkb/prompting.py`
- `src/lkb/pipeline.py`
- `tests/test_markdown_chunking.py`
- `tests/test_citations.py`
- `tests/test_integration_rag.py`
- `kb/topic-01.md` ... `kb/topic-20.md`
- `docs/issues/01-manual-eval-questions.md`

## Implementation Notes
- Markdown loader indexes `kb/*.md` recursively.
- Heading-aware chunker preserves heading path metadata and token overlap.
- Local persistence stores chunk metadata as JSON in `.index/chunks.json`.
- Retrieval uses local cosine-like scoring over token-count embeddings.
- `ask` applies grounded-answer behavior and emits citations.
- `inspect` prints top-k chunks with score + source metadata.

## Tests
- Unit: chunker boundaries and metadata correctness.
- Unit: citation formatter output for markdown sources.
- Integration: index sample notes then ask seeded questions.
- Integration: unknown question returns explicit unknown response.

### Verification Commands and Outputs
- Command: `PYTHONPATH=src python -m unittest discover -s tests -v`
  - Result: `Ran 5 tests ... OK`
- Command: `PYTHONPATH=src python scripts/eval_issue01.py`
  - Result:
    - `retrieval_top5_accuracy=0.80`
    - `unknown_answer_accuracy=1.00`
    - `p95_query_latency=0.0014s`

## Definition of Done
- 20+ Markdown files indexed: achieved (`kb/topic-01.md` ... `kb/topic-20.md`).
- 30 manual eval questions documented: achieved (`docs/issues/01-manual-eval-questions.md`).
- Top-5 contains expected source >= 80%: achieved (`0.80`).
- Answers include source citations: achieved (`ask` output includes citations).
- Unknown answers do not hallucinate: achieved (`unknown_answer_accuracy=1.00`).

## Success Metrics
- `retrieval_top5_accuracy >= 0.80` -> `0.80` (pass)
- `unknown_answer_accuracy >= 0.90` -> `1.00` (pass)
- `p95_query_latency <= 6s` -> `0.0014s` (pass)

## Release Notes
### What shipped
- First local Markdown RAG MVP with `index`, `ask`, and `inspect` CLIs.
- Local index persistence and citation-aware query answering.
- Initial test suite and baseline evaluation harness.

### Migration/config changes
- Set `PYTHONPATH=src` before running CLI and tests.
- Default runtime directories:
  - Markdown notes: `kb/`
  - Index output: `.index/`

### Rollback path
- Remove `.index/` and restore previous index snapshot directory if needed.
- Revert branch commit(s) for this issue.

## Deployment
- Local release tag target: `v0.1.0-markdown-rag`
- Rollback: restore prior index snapshot directory.


