# Issue 09 - Capture Workflows and Auto-Sync

## Goal
Reduce ingestion friction by automating common knowledge capture paths.

## Scope
- In: local folder sync, manual upload, web clipping, Obsidian-compatible markdown sync.
- Out: full cloud integrations (Notion/Drive/GitHub APIs).

## Deliverables
- Source adapters for local sync and web clipping
- Duplicate detection and ingestion dedupe
- Metadata normalization template for captured content

## Implementation Tasks
1. Add filesystem watcher / scheduled sync.
2. Add manual upload normalization.
3. Add web clip import format.
4. Add duplicate detection using hash + canonical URI.
5. Add filters by tag/date/source.

## Tests
- Unit: dedupe logic.
- Integration: repeated sync does not duplicate records.
- Integration: captured metadata filters work in retrieval.

## Definition of Done
- New knowledge can be captured in under 2 minutes.
- New/updated files auto-index.
- Duplicates are suppressed.
- Search supports tag/date/source filters.

## Success Metrics
- `duplicate_ingestion_rate <= 1%`.
- `sync_to_search_latency_p95 <= 180s` for local files.

## Deployment
- Release tag: `v0.9.0-capture-workflows`
- Sync jobs include dry-run mode.
