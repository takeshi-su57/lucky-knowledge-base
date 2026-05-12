# Issue 02 - Schema and Incremental Indexing

## Goal
Introduce durable document/chunk/query schema and re-index only changed files.

## Scope
- In: SQLite tables for docs/chunks/embeddings/queries/results/answers/feedback, content-hash incremental indexing.
- Out: Hybrid search and reranker.

## Deliverables
- DB schema migration scripts
- Content hash detection in indexing pipeline
- CLI command to inspect document->chunk->embedding lineage

## Implementation Tasks
1. Add normalized schema + repositories.
2. Compute and persist file content hash.
3. Skip unchanged documents during indexing.
4. Add full rebuild command.
5. Add lineage inspection command.

## Tests
- Unit: hash change detection logic.
- Unit: repository CRUD for core tables.
- Integration: modify one file and verify only affected chunks re-embedded.
- Integration: full rebuild recreates valid state.

## Definition of Done
- Index can be deleted and rebuilt cleanly.
- Incremental run only processes changed files.
- Answers can show exact chunk IDs and source pointers.
- Document lineage is queryable by CLI.

## Success Metrics
- Incremental index run time reduced >= 60% vs full rebuild on same corpus.
- `lineage_lookup_success_rate = 100%` on test dataset.

## Deployment
- Release tag: `v0.2.0-schema-incremental`
- Migration rollback script provided.
