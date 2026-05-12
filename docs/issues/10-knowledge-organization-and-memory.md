# Issue 10 - Knowledge Organization and Memory

## Goal
Evolve from retrieval-only system to topic-level memory and cross-document intelligence.

## Scope
- In: document summaries, entities, tags, topic browsing, cross-source summarization.
- Out: full graph database (optional future extension).

## Deliverables
- Summary generation pipeline (short + long)
- Entity extraction and linking model
- Topic browser/query path using summary/entity layers

## Implementation Tasks
1. Generate and store document summaries post-ingestion.
2. Extract entities and relations into structured tables.
3. Link entities to source documents/chunks.
4. Add topic-level retrieval path.
5. Expose topic browsing in API/UI.

## Tests
- Unit: summary schema validation.
- Unit: entity extraction normalization.
- Integration: multi-document topic query accuracy checks.

## Definition of Done
- System answers topic questions across multiple sources.
- Entity links reveal related docs.
- Summaries stored separately from raw chunks.

## Success Metrics
- `multi_source_topic_answer_success >= 0.80`.
- `entity_link_precision >= 0.85` on labeled sample.

## Deployment
- Release tag: `v0.10.0-knowledge-memory`
- Summary generation is asynchronous and retryable.
