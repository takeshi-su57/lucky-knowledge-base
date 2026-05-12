# Personal Knowledge Base AI System Roadmap

> A practical, production-oriented roadmap for building a personal knowledge-base AI system, starting from simple Markdown RAG and evolving into a production-ready multimodal knowledge system.

---

## Table of Contents

1. [Goal](#goal)
2. [Core Mental Model](#core-mental-model)
3. [North-Star Architecture](#north-star-architecture)
4. [Recommended Technology Stack](#recommended-technology-stack)
5. [Roadmap Overview](#roadmap-overview)
6. [Phase 0: Define the Product](#phase-0-define-the-product)
7. [Phase 1: Local Markdown Knowledge Base](#phase-1-local-markdown-knowledge-base)
8. [Phase 2: Real Document and Chunk Schema](#phase-2-real-document-and-chunk-schema)
9. [Phase 3: Retrieval Debugging and Evaluation](#phase-3-retrieval-debugging-and-evaluation)
10. [Phase 4: Hybrid Retrieval and Reranking](#phase-4-hybrid-retrieval-and-reranking)
11. [Phase 5: Simple Web UI](#phase-5-simple-web-ui)
12. [Phase 6: PDF and Office Document Ingestion](#phase-6-pdf-and-office-document-ingestion)
13. [Phase 7: Audio Knowledge Ingestion](#phase-7-audio-knowledge-ingestion)
14. [Phase 8: Video Knowledge Ingestion](#phase-8-video-knowledge-ingestion)
15. [Phase 9: Personal Capture Workflows](#phase-9-personal-capture-workflows)
16. [Phase 10: Knowledge Organization and Memory](#phase-10-knowledge-organization-and-memory)
17. [Phase 11: Production Backend](#phase-11-production-backend)
18. [Phase 12: Guardrails and Reliability](#phase-12-guardrails-and-reliability)
19. [Phase 13: Advanced Query Intelligence](#phase-13-advanced-query-intelligence)
20. [Phase 14: Agent Layer](#phase-14-agent-layer)
21. [Phase 15: Production-Ready Checklist](#phase-15-production-ready-checklist)
22. [Suggested Repository Structure](#suggested-repository-structure)
23. [Core Data Models](#core-data-models)
24. [Prompt Templates](#prompt-templates)
25. [Evaluation Plan](#evaluation-plan)
26. [Implementation Tickets](#implementation-tickets)
27. [References](#references)

---

## Goal

Build a personal AI knowledge-base system that can ingest, index, search, and reason over your own information.

The system should evolve from:

```text
Simple local Markdown files
```

into:

```text
Production-ready multimodal personal knowledge infrastructure
```

The final system should support:

- Markdown notes
- PDFs
- Word documents
- PowerPoint slides
- HTML/web pages
- audio files
- video files
- images/screenshots
- transcripts
- source citations
- semantic search
- keyword search
- hybrid retrieval
- reranking
- evaluation
- background ingestion jobs
- backups
- observability
- optional agent tools

---

## Core Mental Model

Every source format eventually becomes:

```text
content + metadata + source pointer
```

Examples:

```text
Markdown → text + heading + file path
PDF      → text + page number + file path
Audio    → transcript + timestamp + speaker
Video    → transcript + timestamp + frame OCR + visual description
Web page → cleaned text + URL + capture date
Image    → OCR text + image description + file path
```

The main pipeline is:

```text
capture → parse → clean → chunk → embed → retrieve → rerank → generate → cite → evaluate
```

This is the heart of a knowledge-base AI system.

---

## North-Star Architecture

```text
Personal data sources
  ├── Markdown notes
  ├── PDFs
  ├── Word / PowerPoint / HTML
  ├── web pages
  ├── audio
  ├── video
  ├── screenshots / images
  └── APIs / databases

        ↓

Ingestion pipeline
  ├── detect file type
  ├── extract text / tables / images / timestamps
  ├── clean content
  ├── split into chunks
  ├── attach metadata
  ├── create embeddings
  └── store raw file + processed chunks

        ↓

Indexes
  ├── vector index for semantic search
  ├── keyword index for exact search
  ├── metadata database
  ├── optional knowledge graph
  └── object storage for original files

        ↓

Retrieval pipeline
  ├── understand user query
  ├── search vector DB
  ├── search keyword index
  ├── apply metadata filters
  ├── rerank results
  ├── build context
  └── send context to LLM

        ↓

AI assistant
  ├── answer with citations
  ├── show source chunks
  ├── say “I do not know” when evidence is missing
  ├── summarize documents
  ├── compare sources
  ├── create new notes
  └── call tools / agents later

        ↓

Production layer
  ├── evaluation
  ├── monitoring
  ├── backups
  ├── permissions
  ├── sync jobs
  ├── cost tracking
  └── versioning
```

---

## Recommended Technology Stack

### Version 1: Learning / Local Prototype

```text
Language: Python
Interface: CLI
Metadata DB: SQLite
Vector DB: Chroma or FAISS
Embeddings: OpenAI embeddings or SentenceTransformers
Generation model: OpenAI / Anthropic / local LLM
Input format: Markdown only
```

### Version 2: Serious Local App

```text
Backend: FastAPI
Frontend: Streamlit or Next.js
Metadata DB: Postgres
Vector DB: Qdrant or pgvector
Queue: Redis
Workers: Celery, RQ, or Dramatiq
File storage: local disk
Input formats: Markdown, PDF, DOCX, HTML, audio
```

### Version 3: Production-Style System

```text
Backend: FastAPI
Frontend: Next.js
Metadata DB: Postgres
Vector DB: Qdrant / Weaviate / Pinecone / pgvector
Object storage: S3-compatible storage
Queue: Redis
Workers: Celery
Observability: structured logs + metrics + traces
Evaluation: golden dataset + automated regression tests
Input formats: text, docs, PDFs, audio, video, images
```

---

## Roadmap Overview

```text
Level 1: Markdown CLI RAG
  Build a local ask-over-notes system.

Level 2: Real document/chunk schema
  Add metadata, hashes, SQLite/Postgres schema.

Level 3: Retrieval debugging
  Add inspect tool, top-k analysis, test questions.

Level 4: Hybrid retrieval
  Add keyword search + vector search + reranking.

Level 5: Web UI
  Add chat, upload, sources, feedback.

Level 6: PDF/Office ingestion
  Add PDF, DOCX, PPTX, HTML parsing and page citations.

Level 7: Audio ingestion
  Add transcription, speaker/timestamp chunks.

Level 8: Video ingestion
  Add audio extraction, transcript, OCR, frame descriptions.

Level 9: Personal capture
  Add folder sync, web clipper, Obsidian/Notion exports.

Level 10: Evaluation
  Add golden questions, retrieval metrics, answer metrics.

Level 11: Production backend
  Add workers, queue, Postgres, object storage, backups.

Level 12: Agent layer
  Add tools for search, read, summarize, and create notes.

Level 13: Knowledge intelligence
  Add summaries, entities, tags, optional graph.

Level 14: Production hardening
  Add monitoring, permissions, cost tracking, prompt/model versioning.
```

---

## Phase 0: Define the Product

### Objective

Define the first useful version of the product before writing complex code.

Your first version should answer this question:

> Can I ask questions over my own notes and get grounded answers with source citations?

### Scope

Start with:

```text
User = you
Data = local Markdown files
Goal = ask questions and get source-backed answers
```

Do not start with:

- PDFs
- audio
- video
- agents
- multi-agent systems
- complex UI
- cloud sync

### Success Criteria

The first system is successful when it can:

- read Markdown files from a folder
- split files into chunks
- embed the chunks
- store them in a local vector DB
- retrieve relevant chunks for a user question
- answer using only those chunks
- show source file names
- say “I do not know” when evidence is missing

---

## Phase 1: Local Markdown Knowledge Base

### Objective

Build the simplest possible working RAG system over local Markdown files.

### Example Data Layout

```text
kb/
  ai-notes.md
  rag-study.md
  project-ideas.md
  books.md
  personal-principles.md
```

### First Scripts

Create three scripts:

```text
index.py
ask.py
inspect.py
```

### `index.py`

Responsibilities:

- read all `.md` files
- split by Markdown headings
- create chunks
- create embeddings
- store chunk text, metadata, and vector

Pseudo-flow:

```text
for file in kb/*.md:
    text = read(file)
    sections = split_by_markdown_headings(text)
    chunks = chunk_sections(sections)
    for chunk in chunks:
        embedding = embed(chunk.text)
        store(chunk, embedding)
```

### `ask.py`

Responsibilities:

- take user question
- embed the question
- retrieve top 5 chunks
- send chunks + question to LLM
- print answer + sources

Pseudo-flow:

```text
question = input()
query_embedding = embed(question)
chunks = vector_search(query_embedding, top_k=5)
answer = generate_answer(question, chunks)
print(answer)
print_sources(chunks)
```

### `inspect.py`

Responsibilities:

- show retrieved chunks
- show scores
- show source file names
- help debug bad retrieval

This is important because many RAG failures are retrieval failures, not generation failures.

### Initial Chunking Rule

```text
Chunk by Markdown heading
Max chunk size: 500–1,000 tokens
Overlap: 50–100 tokens
Store heading path as metadata
```

### Example Chunk Metadata

```json
{
  "source": "rag-study.md",
  "heading": "Vector Search",
  "chunk_index": 12,
  "content_type": "markdown",
  "created_at": "2026-05-12"
}
```

### Acceptance Criteria

Move to Phase 2 when:

- [ ] at least 20 Markdown files are indexed
- [ ] at least 30 manual test questions exist
- [ ] correct source appears in top 5 for at least 80% of test questions
- [ ] answer cites the correct file
- [ ] system says “I do not know” when answer is not in notes

---

## Phase 2: Real Document and Chunk Schema

### Objective

Move from a simple script to a real internal data model.

### Core Entities

```text
Document
Chunk
Embedding
Source
IngestionJob
Query
RetrievalResult
Answer
Feedback
```

### Minimal Tables

```sql
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    source_uri TEXT NOT NULL,
    title TEXT,
    file_type TEXT,
    content_hash TEXT,
    created_at TEXT,
    updated_at TEXT,
    indexed_at TEXT,
    status TEXT
);

CREATE TABLE chunks (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    token_count INTEGER,
    heading TEXT,
    page_number INTEGER,
    start_time TEXT,
    end_time TEXT,
    metadata_json TEXT,
    FOREIGN KEY (document_id) REFERENCES documents(id)
);

CREATE TABLE embeddings (
    chunk_id TEXT PRIMARY KEY,
    embedding_model TEXT NOT NULL,
    vector_id TEXT NOT NULL,
    vector_dimension INTEGER,
    FOREIGN KEY (chunk_id) REFERENCES chunks(id)
);

CREATE TABLE queries (
    id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    created_at TEXT
);

CREATE TABLE retrieval_results (
    query_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    rank INTEGER,
    score REAL,
    retriever_type TEXT,
    FOREIGN KEY (query_id) REFERENCES queries(id),
    FOREIGN KEY (chunk_id) REFERENCES chunks(id)
);

CREATE TABLE answers (
    id TEXT PRIMARY KEY,
    query_id TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    model TEXT,
    created_at TEXT,
    FOREIGN KEY (query_id) REFERENCES queries(id)
);

CREATE TABLE feedback (
    id TEXT PRIMARY KEY,
    answer_id TEXT NOT NULL,
    rating INTEGER,
    notes TEXT,
    created_at TEXT,
    FOREIGN KEY (answer_id) REFERENCES answers(id)
);
```

### Why This Matters

You need to know:

- where each chunk came from
- which file version produced it
- which model embedded it
- which query retrieved it
- which chunks were used in an answer
- whether the answer was good

Without this, debugging production RAG becomes painful.

### Acceptance Criteria

Move to Phase 3 when:

- [ ] index can be deleted and rebuilt
- [ ] only changed files are re-indexed using content hashes
- [ ] each answer shows exact chunks used
- [ ] document → chunks → embeddings can be inspected

---

## Phase 3: Retrieval Debugging and Evaluation

### Objective

Make retrieval measurable and debuggable.

### Add a Golden Test Set

Create:

```text
evals/test_questions.yaml
```

Example:

```yaml
- id: q001
  question: "What is my preferred chunking strategy for Markdown?"
  expected_sources:
    - "rag-study.md"
  expected_answer_contains:
    - "heading"
    - "overlap"

- id: q002
  question: "What did I write about vector databases?"
  expected_sources:
    - "vector-db-notes.md"
  expected_answer_contains:
    - "embedding"
    - "semantic search"
```

### Retrieval Metrics

Track:

```text
retrieval_top_1_accuracy
retrieval_top_3_accuracy
retrieval_top_5_accuracy
mean_reciprocal_rank
citation_accuracy
unknown_answer_accuracy
latency
cost_per_query
```

### Debugging Workflow

For every bad answer, inspect:

```text
1. Was the document parsed correctly?
2. Was the chunk too small or too large?
3. Was the right chunk retrieved?
4. Did the reranker reorder results badly?
5. Did the LLM ignore the source?
6. Was the question ambiguous?
7. Was the expected knowledge missing?
```

### Acceptance Criteria

Move to Phase 4 when:

- [ ] at least 50 test questions exist
- [ ] eval script reports top-1, top-3, and top-5 retrieval accuracy
- [ ] bad retrieval examples can be inspected
- [ ] every prompt or retrieval change can be evaluated

---

## Phase 4: Hybrid Retrieval and Reranking

### Objective

Improve retrieval using vector search, keyword search, metadata filtering, and reranking.

### Retrieval Versions

Build retrieval in this order:

```text
V1: vector search only
V2: vector search + metadata filters
V3: vector search + keyword search
V4: hybrid search
V5: hybrid search + reranking
```

### Why Hybrid Search Matters

Vector search is good for meaning.

Keyword search is good for exact strings.

Example:

```text
Question: What does note AI-2025-11 say about HNSW?
```

Exact terms matter:

```text
AI-2025-11
HNSW
```

Pure vector search may miss exact IDs or rare terms. Keyword search helps.

### Production Retrieval Flow

```text
User question
  ↓
Optional query rewrite
  ↓
Dense vector search: top 30
  ↓
Keyword/BM25 search: top 30
  ↓
Merge results
  ↓
Remove duplicates
  ↓
Apply metadata filters
  ↓
Rerank top 30
  ↓
Select top 5–10 chunks
  ↓
Build LLM context
```

### Reranking

A reranker takes candidate chunks and sorts them by relevance to the query.

Simple pattern:

```text
retriever returns 30 chunks
reranker scores 30 chunks
context builder uses best 5–10 chunks
```

### Acceptance Criteria

Move to Phase 5 when:

- [ ] hybrid search beats vector-only search on your eval set
- [ ] reranking improves source relevance
- [ ] metadata filters work
- [ ] exact-term queries work better than before
- [ ] you can compare retrieval versions using the same eval set

---

## Phase 5: Simple Web UI

### Objective

Make the system usable every day.

### UI Features

Build a small interface with:

- chat input
- answer panel
- source panel
- retrieved chunks panel
- upload button
- feedback buttons
- document list
- re-index button

### Recommended Stack

Simple path:

```text
Streamlit + FastAPI backend
```

More production-like path:

```text
Next.js frontend + FastAPI backend
```

### Important UX Rule

Do not hide retrieval.

Show:

- answer
- sources
- retrieved chunks
- similarity/rerank scores
- evidence quality

This helps debugging and builds trust.

### Acceptance Criteria

Move to Phase 6 when:

- [ ] you use the app for your own notes for at least one week
- [ ] Markdown files can be uploaded from browser
- [ ] sources are visible next to answers
- [ ] thumbs-up / thumbs-down feedback is stored
- [ ] bad answers are logged for later evaluation

---

## Phase 6: PDF and Office Document Ingestion

### Objective

Add real-world document formats.

### Supported Formats

Start with:

```text
.pdf
.docx
.html
.txt
```

Then add:

```text
.pptx
.xlsx
.csv
```

### Key Problem

PDFs and office documents contain:

- headers
- footers
- page numbers
- tables
- figures
- images
- multi-column layouts
- scanned pages
- strange line breaks

Bad extraction creates bad retrieval.

### Recommended Pipeline

```text
Original file
  ↓
Detect file type
  ↓
Parse into structured elements
  ↓
Normalize to Markdown-like text
  ↓
Preserve page/section/table metadata
  ↓
Chunk intelligently
  ↓
Embed
  ↓
Store with source pointers
```

### PDF Pipeline

```text
PDF file
  ↓
Detect digital vs scanned
  ↓
If digital: extract text + tables
  ↓
If scanned: OCR
  ↓
Preserve page numbers
  ↓
Preserve headings
  ↓
Convert tables to Markdown tables
  ↓
Chunk by section or page
  ↓
Store page-level citations
```

### PDF Chunk Metadata

```json
{
  "source": "paper.pdf",
  "page": 12,
  "section": "3.2 Retrieval Evaluation",
  "chunk_type": "paragraph",
  "has_table": false
}
```

### Acceptance Criteria

Move to Phase 7 when:

- [ ] at least 20 PDFs are indexed
- [ ] answers cite page numbers
- [ ] tables are searchable
- [ ] scanned PDFs are OCRed or clearly marked unsupported
- [ ] extraction quality can be inspected before indexing

---

## Phase 7: Audio Knowledge Ingestion

### Objective

Make audio files searchable through transcription.

### Audio Pipeline

```text
Audio file
  ↓
Transcribe speech to text
  ↓
Optional speaker diarization
  ↓
Split transcript into timestamped segments
  ↓
Summarize long sections
  ↓
Chunk by topic / timestamp
  ↓
Embed transcript chunks
  ↓
Cite answers with timestamps
```

### Audio Metadata

```json
{
  "source": "meeting-2026-05-12.mp3",
  "speaker": "Takeshi",
  "start_time": "00:12:31",
  "end_time": "00:13:08",
  "topic": "RAG evaluation",
  "content_type": "audio_transcript"
}
```

### Example Query

```text
What did I say about hybrid search in last week's meeting?
```

Expected answer format:

```text
You mentioned that hybrid search should combine vector similarity with exact keyword matching, especially for project names and technical terms.

Source: meeting-2026-05-12.mp3, 00:12:31–00:13:08
```

### Acceptance Criteria

Move to Phase 8 when:

- [ ] audio files can be uploaded
- [ ] transcripts are searchable semantically
- [ ] answers cite timestamps
- [ ] long audio is chunked by topic or timestamp
- [ ] transcript quality can be inspected

---

## Phase 8: Video Knowledge Ingestion

### Objective

Make videos searchable through transcript, frame OCR, and visual descriptions.

### Video Is Multiple Data Types

A video may contain:

- audio
- transcript
- frames
- slides
- screen text
- visual objects
- timestamps

### Video Pipeline

```text
Video file
  ↓
Extract audio
  ↓
Transcribe audio
  ↓
Sample important frames
  ↓
OCR text from frames
  ↓
Optionally caption key frames
  ↓
Link transcript segments to timestamps
  ↓
Link frames to timestamps
  ↓
Index transcript + OCR + visual descriptions
```

### What to Index

Index at least three chunk types:

```text
Transcript chunks
Slide/OCR text chunks
Frame description chunks
```

### Example Transcript Chunk

```json
{
  "source": "lecture-rag.mp4",
  "start_time": "00:21:10",
  "end_time": "00:22:02",
  "chunk_type": "transcript",
  "text": "The speaker explains reranking..."
}
```

### Example Frame OCR Chunk

```json
{
  "source": "lecture-rag.mp4",
  "timestamp": "00:21:34",
  "chunk_type": "frame_ocr",
  "text": "Dense retrieval + sparse retrieval + reranker"
}
```

### Acceptance Criteria

Move to Phase 9 when:

- [ ] video transcripts are searchable
- [ ] answers can cite video timestamps
- [ ] slide text / screen text is searchable
- [ ] spoken content and visual content are distinguishable
- [ ] user can jump to the original timestamp

---

## Phase 9: Personal Capture Workflows

### Objective

Make the system easy to feed with new knowledge.

### Input Sources

Add these one by one:

```text
Local folder sync
Manual upload
Web page clipping
Obsidian vault sync
Notion export
Google Drive export
GitHub repo docs
Audio note upload
Video upload
```

### Recommended Order

```text
1. Local folder sync
2. Manual upload
3. Web page clipping
4. Obsidian / Markdown vault
5. PDFs
6. Audio
7. Video
8. Cloud services
```

### Capture Format

Normalize captured knowledge into Markdown-like records:

```markdown
---
title: "Article about RAG evaluation"
source_url: "https://example.com/article"
captured_at: "2026-05-12"
content_type: "webpage"
tags: ["rag", "evaluation"]
---

# Summary

...

# Original Content

...
```

### Acceptance Criteria

Move to Phase 10 when:

- [ ] new knowledge can be added quickly
- [ ] new files are automatically indexed
- [ ] duplicate documents are detected
- [ ] search supports tag, date, source, and semantic meaning

---

## Phase 10: Knowledge Organization and Memory

### Objective

Turn the system from a search tool into a personal intelligence system.

### Document-Level Summaries

For every document, generate and store:

```text
short summary
long summary
key ideas
entities
tags
questions this document can answer
```

### Entity Extraction

Extract entities such as:

```text
people
projects
companies
books
papers
technologies
concepts
dates
tasks
decisions
```

Example:

```json
{
  "entity": "hybrid search",
  "type": "concept",
  "mentioned_in": ["rag-study.md", "lecture-rag.mp4"],
  "related_to": ["BM25", "dense retrieval", "reranking"]
}
```

### Optional Knowledge Graph

Add a graph only when you need cross-document reasoning, such as:

```text
What ideas about RAG evaluation appear across my notes, PDFs, and meetings?
Which people are connected to which projects?
How has my thinking about AI agents changed over time?
```

### Acceptance Criteria

Move to Phase 11 when:

- [ ] system can summarize a topic across many sources
- [ ] entities link related documents
- [ ] topic browsing exists
- [ ] document summaries are stored separately from chunks

---

## Phase 11: Production Backend

### Objective

Convert the prototype into a reliable service.

### Production Architecture

```text
Frontend
  Next.js / React / Streamlit

Backend API
  FastAPI

Database
  Postgres

Vector DB
  Qdrant / pgvector / Weaviate / Pinecone

Object storage
  local disk first, later S3-compatible storage

Background workers
  Celery / RQ / Dramatiq

Queue
  Redis

LLM provider
  OpenAI / Anthropic / local model

Observability
  logs, traces, metrics, eval dashboard
```

### Ingestion Should Be Async

Do not parse large files inside a normal web request.

Use background jobs:

```text
file_uploaded
  ↓
create_ingestion_job
  ↓
worker picks job
  ↓
parse file
  ↓
chunk
  ↓
embed
  ↓
write database
  ↓
mark job complete
```

### Job Statuses

```text
pending
processing
completed
failed
needs_review
unsupported_format
```

### Acceptance Criteria

Move to Phase 12 when:

- [ ] large files do not block UI
- [ ] failed ingestion jobs can be retried
- [ ] every job has logs
- [ ] system survives restart
- [ ] migrations are managed
- [ ] database and files can be backed up/restored

---

## Phase 12: Guardrails and Reliability

### Objective

Make answers grounded, predictable, and safe.

### Answer Rules

Your system prompt should include:

```text
Use only the provided sources.
If sources do not contain the answer, say you do not know.
Cite every important claim.
Do not invent file names, page numbers, or timestamps.
Separate facts from interpretation.
Ask a follow-up only when necessary.
```

### Confidence Behavior

```text
High-quality retrieval:
  answer normally

Weak retrieval:
  say evidence is limited

No relevant retrieval:
  say you do not know

Conflicting sources:
  explain the conflict and cite both
```

### Freshness Metadata

Store:

```text
created_at
modified_at
indexed_at
source_published_at
document_version
```

### Acceptance Criteria

Move to Phase 13 when:

- [ ] assistant refuses unsupported answers
- [ ] conflicting sources are handled clearly
- [ ] citations are never fake
- [ ] old and new versions are distinguishable
- [ ] missing evidence is reported honestly

---

## Phase 13: Advanced Query Intelligence

### Objective

Make retrieval strategy adapt to the user’s question.

### Query Types

Classify queries as:

```text
fact lookup
summary
comparison
timeline
brainstorming
personal memory
document-specific question
multi-document research
action request
```

### Example Strategies

```text
Question: "Summarize this PDF"
Strategy: retrieve document by ID, not broad semantic search

Question: "What do I know about vector databases?"
Strategy: broad topic retrieval across many sources

Question: "What did I say in yesterday's audio note?"
Strategy: filter by date + content_type=audio_transcript
```

### Query Expansion

User asks:

```text
How do vector databases work?
```

System also searches:

```text
vector database
semantic search
embeddings
nearest neighbor search
cosine similarity
ANN
HNSW
```

### Multi-Step Retrieval

For complex questions:

```text
Find relevant documents
  ↓
Summarize each document
  ↓
Compare summaries
  ↓
Generate final answer
```

### Acceptance Criteria

Move to Phase 14 when:

- [ ] broad research questions work better
- [ ] document-specific questions avoid unrelated sources
- [ ] date-specific questions respect date filters
- [ ] system can explain its retrieval strategy

---

## Phase 14: Agent Layer

### Objective

Add agent tools after retrieval is reliable.

### Tools

```text
search_knowledge_base(query, filters)
read_document(document_id)
summarize_document(document_id)
compare_documents(document_ids)
create_note(title, content, tags)
update_tags(document_id, tags)
create_flashcards(document_id)
extract_tasks(document_id)
```

### Agent Rule

The agent should not answer from memory when knowledge-base search is required.

The loop should be:

```text
User request
  ↓
Agent decides whether search is needed
  ↓
Agent calls search_knowledge_base
  ↓
Agent reads source chunks
  ↓
Agent answers with citations
  ↓
Agent optionally performs action
```

### Example

User:

```text
Create a study plan based on all my notes about RAG.
```

Agent flow:

```text
Search: RAG notes
Read top documents
Extract concepts
Group by difficulty
Create study plan
Save as new note
Link back to sources
```

### Acceptance Criteria

Move to Phase 15 when:

- [ ] agent actions are logged
- [ ] every created note links back to sources
- [ ] destructive actions require confirmation
- [ ] agent can explain which tools it used

---

## Phase 15: Production-Ready Checklist

### Core Capabilities

- [ ] upload files
- [ ] sync local folders
- [ ] parse Markdown
- [ ] parse PDF
- [ ] parse DOCX
- [ ] parse PPTX
- [ ] parse HTML
- [ ] parse audio
- [ ] parse video
- [ ] extract text
- [ ] extract tables
- [ ] OCR images/scanned PDFs
- [ ] transcribe audio
- [ ] chunk by content type
- [ ] embed and index chunks
- [ ] vector search
- [ ] keyword search
- [ ] hybrid search
- [ ] reranking
- [ ] metadata filtering
- [ ] source citations
- [ ] page citations
- [ ] timestamp citations
- [ ] evaluation suite
- [ ] feedback loop
- [ ] background ingestion jobs
- [ ] backups
- [ ] monitoring
- [ ] versioning

### Security

- [ ] local-first option
- [ ] API keys stored safely
- [ ] private files not sent to unnecessary services
- [ ] optional encryption at rest
- [ ] access control if multi-user

### Reliability

- [ ] failed jobs can be retried
- [ ] ingestion logs are stored
- [ ] re-indexing is supported
- [ ] backups are automated
- [ ] database migrations are managed
- [ ] prompts are versioned
- [ ] embedding models are versioned

### Quality

- [ ] retrieval evals
- [ ] answer evals
- [ ] citation evals
- [ ] regression tests
- [ ] feedback review workflow

### Performance

- [ ] async ingestion
- [ ] caching
- [ ] streaming answers
- [ ] top-k tuning
- [ ] reranking only when needed
- [ ] cost tracking

### UX

- [ ] source previews
- [ ] page citations
- [ ] timestamp citations
- [ ] document browser
- [ ] search filters
- [ ] “why this answer?” panel
- [ ] “show retrieved chunks” panel

---

## Suggested Repository Structure

```text
personal-kb-ai/
  README.md
  ROADMAP.md
  pyproject.toml
  .env.example
  docker-compose.yml

  app/
    __init__.py

    api/
      main.py
      routes_chat.py
      routes_documents.py
      routes_ingestion.py
      routes_eval.py

    core/
      config.py
      logging.py
      types.py
      errors.py

    ingestion/
      loaders/
        markdown_loader.py
        pdf_loader.py
        docx_loader.py
        html_loader.py
        audio_loader.py
        video_loader.py
      chunkers/
        markdown_chunker.py
        recursive_chunker.py
        transcript_chunker.py
      pipeline.py
      jobs.py

    retrieval/
      vector_retriever.py
      keyword_retriever.py
      hybrid_retriever.py
      reranker.py
      context_builder.py
      query_classifier.py
      query_expander.py

    generation/
      prompts.py
      answer_generator.py
      citation_formatter.py

    storage/
      db.py
      models.py
      repositories.py
      vector_store.py
      object_store.py

    evals/
      test_questions.yaml
      run_eval.py
      metrics.py
      reports.py

    agents/
      tools.py
      agent.py

  scripts/
    index.py
    ask.py
    inspect.py
    rebuild_index.py
    run_eval.py

  kb/
    example-note.md

  tests/
    test_chunking.py
    test_retrieval.py
    test_citations.py

  frontend/
    # optional Next.js or Streamlit app
```

---

## Core Data Models

### Document

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Document:
    id: str
    source_uri: str
    title: Optional[str]
    file_type: str
    content_hash: str
    created_at: str
    updated_at: str
    indexed_at: Optional[str]
    status: str
```

### Chunk

```python
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Chunk:
    id: str
    document_id: str
    chunk_index: int
    text: str
    token_count: int
    heading: Optional[str] = None
    page_number: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    metadata: Dict[str, Any] = None
```

### Retrieval Result

```python
from dataclasses import dataclass

@dataclass
class RetrievalResult:
    chunk_id: str
    text: str
    source_uri: str
    score: float
    rank: int
    retriever_type: str
    metadata: dict
```

---

## Prompt Templates

### Grounded Answer Prompt

```text
You are a personal knowledge-base assistant.

Answer the user's question using only the provided sources.

Rules:
- Use only the context below.
- If the answer is not supported by the context, say: "I do not know based on the available sources."
- Cite sources for important claims.
- Do not invent file names, page numbers, timestamps, or URLs.
- If sources conflict, explain the conflict and cite both.
- Keep the answer clear and practical.

User question:
{question}

Retrieved context:
{context}

Answer:
```

### Unknown Answer Behavior

```text
The provided sources do not contain enough information to answer this question reliably.

Relevant sources checked:
{sources}

What is missing:
{missing_information}
```

### Citation Format

Markdown source:

```text
Source: rag-study.md > Vector Search
```

PDF source:

```text
Source: paper.pdf, page 12
```

Audio source:

```text
Source: meeting-2026-05-12.mp3, 00:12:31–00:13:08
```

Video source:

```text
Source: lecture-rag.mp4, 00:21:10–00:22:02
```

---

## Evaluation Plan

### Evaluation Dataset

Create:

```text
evals/test_questions.yaml
```

Example:

```yaml
- id: q001
  question: "What is my preferred chunking strategy for Markdown?"
  expected_sources:
    - "rag-study.md"
  expected_answer_contains:
    - "heading"
    - "overlap"
  type: "fact_lookup"

- id: q002
  question: "What did I say about hybrid search in my meeting?"
  expected_sources:
    - "meeting-2026-05-12.mp3"
  expected_timestamp_range:
    start: "00:12:00"
    end: "00:14:00"
  type: "audio_memory"

- id: q003
  question: "What do I know about vector databases across all notes?"
  expected_sources:
    - "vector-db-notes.md"
    - "rag-study.md"
  type: "multi_document_research"
```

### Retrieval Metrics

```python
def top_k_accuracy(results, expected_sources, k):
    top_sources = [r.source_uri for r in results[:k]]
    return any(src in top_sources for src in expected_sources)
```

Track:

```text
top_1_accuracy
top_3_accuracy
top_5_accuracy
mean_reciprocal_rank
retrieval_latency_ms
```

### Answer Metrics

Track manually at first:

```text
faithfulness: answer is supported by sources
completeness: answer covers important facts
citation_accuracy: citations point to the right source
unknown_accuracy: system says “I do not know” when evidence is missing
```

---

## Implementation Tickets

### Milestone 1: Markdown CLI RAG

- [ ] Create `kb/` folder
- [ ] Add 20 Markdown files
- [ ] Implement Markdown loader
- [ ] Implement heading-based chunker
- [ ] Implement embedding client
- [ ] Implement local vector store
- [ ] Implement `index.py`
- [ ] Implement `ask.py`
- [ ] Implement `inspect.py`
- [ ] Add answer prompt with source citations

### Milestone 2: Metadata and Incremental Indexing

- [ ] Add SQLite database
- [ ] Add `documents` table
- [ ] Add `chunks` table
- [ ] Add `embeddings` table
- [ ] Add content hash detection
- [ ] Re-index only changed files
- [ ] Add document/chunk inspection commands

### Milestone 3: Evaluation

- [ ] Create `evals/test_questions.yaml`
- [ ] Add 30 test questions
- [ ] Implement retrieval evaluation
- [ ] Track top-1/top-3/top-5 accuracy
- [ ] Save eval reports
- [ ] Add regression comparison

### Milestone 4: Hybrid Search

- [ ] Add keyword index
- [ ] Implement BM25 or full-text search
- [ ] Merge vector and keyword results
- [ ] Add metadata filters
- [ ] Add reranker
- [ ] Compare with vector-only baseline

### Milestone 5: Web UI

- [ ] Add FastAPI backend
- [ ] Add chat endpoint
- [ ] Add document upload endpoint
- [ ] Add source/chunk endpoint
- [ ] Add feedback endpoint
- [ ] Build simple Streamlit or Next.js UI
- [ ] Show answer + sources + chunks

### Milestone 6: PDF and Office Docs

- [ ] Add PDF loader
- [ ] Preserve page numbers
- [ ] Add table extraction strategy
- [ ] Add OCR fallback or unsupported marker
- [ ] Add DOCX loader
- [ ] Add HTML loader
- [ ] Add document extraction preview

### Milestone 7: Audio

- [ ] Add audio upload
- [ ] Add transcription pipeline
- [ ] Store timestamped transcript segments
- [ ] Add transcript chunker
- [ ] Add timestamp citations
- [ ] Add transcript quality inspection

### Milestone 8: Video

- [ ] Extract audio from video
- [ ] Transcribe audio
- [ ] Sample frames
- [ ] OCR frame text
- [ ] Store frame timestamps
- [ ] Search transcript + OCR content
- [ ] Add timestamp jump links

### Milestone 9: Production Backend

- [ ] Move metadata DB to Postgres
- [ ] Move vector DB to Qdrant or pgvector
- [ ] Add Redis
- [ ] Add background worker
- [ ] Add ingestion job table
- [ ] Add retry logic
- [ ] Add backups
- [ ] Add structured logs

### Milestone 10: Agent Layer

- [ ] Implement `search_knowledge_base` tool
- [ ] Implement `read_document` tool
- [ ] Implement `summarize_document` tool
- [ ] Implement `create_note` tool
- [ ] Add action logs
- [ ] Require confirmation for destructive actions

---

## References

These are useful technologies and concepts to research while implementing this roadmap:

- Retrieval-Augmented Generation: https://docs.langchain.com/oss/python/langchain/rag
- OpenAI embeddings: https://developers.openai.com/api/docs/guides/embeddings
- OpenAI File Search: https://developers.openai.com/api/docs/guides/tools-file-search
- Qdrant hybrid search: https://qdrant.tech/documentation/search/hybrid-queries/
- Qdrant vector database: https://github.com/qdrant/qdrant
- pgvector: https://github.com/pgvector/pgvector
- Cohere rerank: https://docs.cohere.com/docs/rerank
- Microsoft MarkItDown: https://github.com/microsoft/markitdown
- Unstructured document partitioning: https://docs.unstructured.io/open-source/core-functionality/partitioning
- Tesseract OCR: https://tesseract-ocr.github.io/tessdoc/
- FFmpeg: https://ffmpeg.org/ffmpeg.html
- Celery task queue: https://docs.celeryq.dev/en/stable/index.html

---

## Final Principle

Do not build a perfect system first.

Build this sequence:

```text
working → inspectable → measurable → extensible → reliable → production-ready
```

The best roadmap is not the one with the most features.

The best roadmap is the one where every phase produces a usable system and teaches you exactly what to improve next.
