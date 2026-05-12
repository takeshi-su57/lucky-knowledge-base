# Issue 08 - Video Ingestion, OCR, and Visual Indexing

## Goal
Index video content across transcript and on-screen text for grounded retrieval.

## Scope
- In: audio extraction, transcription, frame sampling, OCR, optional visual descriptions, timestamp linking.
- Out: external cloud capture connectors.

## Deliverables
- Video pipeline producing transcript + frame OCR chunks
- Retrieval over multiple video chunk types
- Timestamp jump metadata in results

## Implementation Tasks
1. Add video audio extraction stage.
2. Add frame sampling + OCR stage.
3. Link transcript and frame chunks to timestamps.
4. Distinguish chunk types in storage and retrieval.
5. Add timestamp jump link in result payload.

## Tests
- Unit: chunk-type serialization and indexing.
- Integration: sample video pipeline end-to-end.
- Integration: OCR-specific query retrieval.

## Definition of Done
- Video transcripts are searchable.
- On-screen text is retrievable.
- Answers cite valid video timestamps.
- Users can jump back to source timestamp.

## Success Metrics
- `video_transcript_retrieval_accuracy >= 0.75`.
- `ocr_query_success_rate >= 0.80` on labeled cases.

## Deployment
- Release tag: `v0.8.0-video-ingestion`
- Feature flag available to disable OCR stage if needed.
