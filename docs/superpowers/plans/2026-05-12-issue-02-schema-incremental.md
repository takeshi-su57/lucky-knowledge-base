# Issue 02 Schema And Incremental Indexing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add durable SQLite schema with content-hash incremental indexing and lineage inspection CLI.

**Architecture:** Keep existing ingestion/retrieval flow, replace JSON index persistence with SQLite repositories and migrations, and store embeddings per chunk so incremental runs can skip unchanged documents safely.

**Tech Stack:** Python, sqlite3, unittest, CLI scripts.

---

### Task 1: Define Tests For Issue 02 Behavior

**Files:**
- Create: `tests/test_schema_and_repository.py`
- Create: `tests/test_incremental_indexing.py`
- Test: `tests/test_integration_rag.py`

- [ ] **Step 1: Write failing tests for hash + repository + lineage**
- [ ] **Step 2: Write failing tests for incremental and full rebuild flows**
- [ ] **Step 3: Run full test suite and confirm RED**

### Task 2: Implement SQLite Schema And Repository Layer

**Files:**
- Create: `src/lkb/sql/001_issue02_schema_up.sql`
- Create: `src/lkb/sql/001_issue02_schema_down.sql`
- Create: `src/lkb/incremental.py`
- Modify: `src/lkb/models.py`
- Modify: `src/lkb/store.py`

- [ ] **Step 1: Implement schema migrations and connection helpers**
- [ ] **Step 2: Implement document/chunk/embedding CRUD + lineage loader**
- [ ] **Step 3: Add query/result/answer/feedback persistence path**

### Task 3: Wire Pipeline And CLI Commands

**Files:**
- Modify: `src/lkb/pipeline.py`
- Modify: `src/lkb/retrieval.py`
- Modify: `src/lkb/citations.py`
- Modify: `scripts/index.py`
- Create: `scripts/rebuild.py`
- Create: `scripts/lineage.py`

- [ ] **Step 1: Add incremental index and full rebuild pipeline APIs**
- [ ] **Step 2: Add lineage inspection API and CLI**
- [ ] **Step 3: Keep `ask`/`inspect` behavior backward compatible**

### Task 4: Verification, Metrics, And Issue Documentation

**Files:**
- Create: `scripts/eval_issue02.py`
- Modify: `docs/issues/02-schema-and-incremental-indexing.md`

- [ ] **Step 1: Run full tests and integration verification commands**
- [ ] **Step 2: Collect runtime reduction + lineage success metrics**
- [ ] **Step 3: Update issue doc with implementation notes, metrics, and release notes**
