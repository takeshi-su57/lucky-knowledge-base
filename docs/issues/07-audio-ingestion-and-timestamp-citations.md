# Issue 07 - Audio Ingestion and Timestamp Citations

## Goal
Make audio recordings searchable and citable by time range.

## Scope
- In: audio upload, transcription, optional diarization, timestamp chunking, timestamp citations.
- Out: video frames/OCR.

## Deliverables
- Audio ingestion pipeline
- Transcript storage with start/end timestamps
- Timestamp-aware retrieval and citation formatter

## Implementation Tasks
1. Add audio file loader and transcription integration.
2. Segment transcript by topic/time.
3. Store transcript chunks with timestamp metadata.
4. Add timestamp citation rendering in answers.
5. Add transcript quality inspection command.

## Tests
- Unit: timestamp parser/formatter.
- Integration: sample audio -> transcript -> query -> timestamp citation.
- Evaluation: targeted audio-memory question set.

## Definition of Done
- Audio files are uploadable and indexed.
- Transcript chunks are semantically searchable.
- Answers cite valid timestamps.
- Transcript quality review workflow exists.

## Success Metrics
- `audio_query_source_accuracy >= 0.80`.
- `timestamp_citation_validity = 100%` on test fixtures.

## Deployment
- Release tag: `v0.7.0-audio-ingestion`
- Transcription provider config documented.
