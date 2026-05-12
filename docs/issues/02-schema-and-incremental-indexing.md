# Issue 02 - Schema and Incremental Indexing

## Goal
Introduce durable document/chunk/query schema and re-index only changed files.

## Scope
- In: SQLite tables for docs/chunks/embeddings/queries/results/answers/feedback, content-hash incremental indexing.
- Out: Hybrid search and reranker.

## Deliverables
Implemented:
- `src/lkb/sql/001_issue02_schema_up.sql`
- `src/lkb/sql/001_issue02_schema_down.sql`
- `src/lkb/incremental.py`
- `src/lkb/store.py`
- `src/lkb/pipeline.py`
- `src/lkb/models.py`
- `src/lkb/retrieval.py`
- `src/lkb/citations.py`
- `scripts/index.py`
- `scripts/rebuild.py`
- `scripts/lineage.py`
- `scripts/eval_issue02.py`
- `tests/test_schema_and_repository.py`
- `tests/test_incremental_indexing.py`

## Implementation Tasks
Completed:
1. Added normalized SQLite schema + repository methods for docs/chunks/embeddings/queries/results/answers/feedback.
2. Added SHA-256 content hashing and stored hashes per source document.
3. Implemented incremental indexing that only re-processes changed docs and skips unchanged docs.
4. Added `scripts/rebuild.py` for full clean rebuild.
5. Added `scripts/lineage.py` to inspect document->chunk->embedding lineage.

## Tests
- Unit: hash change detection logic (`tests/test_schema_and_repository.py::HashingTests`).
- Unit: repository CRUD for core tables (`tests/test_schema_and_repository.py::RepositoryCrudTests`).
- Integration: modify one file and verify only affected chunks re-embedded (`tests/test_incremental_indexing.py::test_incremental_indexing_only_reembeds_changed_document`).
- Integration: full rebuild recreates valid state (`tests/test_incremental_indexing.py::test_rebuild_index_recreates_valid_state`).
- Backward compatibility checks: existing Issue 01 tests remain green (`tests/test_integration_rag.py`, `tests/test_markdown_chunking.py`, `tests/test_citations.py`).

### Verification Commands and Outputs
- Command: `PYTHONPATH=src python -m unittest discover -s tests -v`
  - Result: `Ran 10 tests ... OK`
- Command: `PYTHONPATH=src python scripts/eval_issue02.py`
  - Result:
    - `full_rebuild_runtime=8.857979s`
    - `incremental_runtime=0.059950s`
    - `incremental_runtime_reduction=99.32%`
    - `lineage_lookup_success_rate=1.00`

## Definition of Done
- Index can be deleted and rebuilt cleanly: achieved (`scripts/rebuild.py` + integration test coverage).
- Incremental run only processes changed files: achieved (index report tracks `indexed_documents` vs `skipped_documents`, integration test validates single-file re-index).
- Answers can show exact chunk IDs and source pointers: achieved (citations include `chunk_id=...` and source path/heading).
- Document lineage is queryable by CLI: achieved (`scripts/lineage.py` + `inspect_lineage` pipeline API).

## Success Metrics
- Incremental index run time reduced >= 60% vs full rebuild on same corpus: achieved (`99.32%` reduction).
- `lineage_lookup_success_rate = 100%` on test dataset: achieved (`1.00`).

## Release Notes
### What shipped
- SQLite-backed durable schema and migration scripts.
- Content-hash incremental indexing with changed-only re-embedding.
- Full rebuild CLI and lineage inspection CLI.
- Query/result/answer/feedback persistence for ask flows.

### Migration/config changes
- Index persistence switched from JSON-only to SQLite at `.index/index.sqlite`.
- Legacy JSON index loading remains as fallback for compatibility.
- New commands:
  - `PYTHONPATH=src python scripts/rebuild.py`
  - `PYTHONPATH=src python scripts/lineage.py --index-dir .index`

### Rollback path
- Use rollback script `src/lkb/sql/001_issue02_schema_down.sql` against `.index/index.sqlite`.
- Remove `.index/` and rerun Issue 01 indexing flow if full rollback is needed.

## Deployment
- Release tag: `v0.2.0-schema-incremental`
- Migration rollback script provided: `src/lkb/sql/001_issue02_schema_down.sql`.
