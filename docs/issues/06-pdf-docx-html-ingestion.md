# Issue 06 - PDF, DOCX, and HTML Ingestion

## Goal
Add robust ingestion for common document formats with traceable citations.

## Scope
- In: `.pdf`, `.docx`, `.html`, `.txt`; extraction preview; page metadata.
- Out: audio/video ingestion.

## Deliverables
- Format detection and parser routing
- Extraction normalization to markdown-like text
- Page/section/table metadata persistence

## Implementation Tasks
1. Add parser abstraction by file type.
2. Implement PDF extraction with digital/scanned detection.
3. Implement DOCX/HTML extractors.
4. Add extraction preview before indexing.
5. Preserve page-level citation metadata.

## Tests
- Unit: parser routing by extension/mime.
- Integration: PDF with known page citations.
- Integration: DOCX/HTML extraction fidelity checks.
- Regression: malformed/unreadable file handling.

## Definition of Done
- At least 20 PDFs indexed successfully.
- Answers can cite pages for PDF sources.
- Tables are searchable when extracted.
- Scanned PDFs are OCRed or flagged unsupported.

## Success Metrics
- `pdf_parse_success_rate >= 0.90` on test corpus.
- `page_citation_accuracy >= 0.90` on labeled queries.

## Deployment
- Release tag: `v0.6.0-doc-ingestion`
- Unsupported file reporting enabled.
