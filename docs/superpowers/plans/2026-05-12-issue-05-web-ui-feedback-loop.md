# Issue 05 Web UI and Feedback Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver API + Streamlit UI for chat/evidence/upload/reindex/feedback, with persistent feedback and bad-answer traces.

**Architecture:** Add a FastAPI app module and minimal persistence helpers in `store.py`, then add a Streamlit UI that consumes the API contracts. Keep changes additive and preserve existing pipeline behavior.

**Tech Stack:** Python, FastAPI, Streamlit, unittest, existing `lkb` indexing/retrieval pipeline.

---

### Task 1: Add Failing Tests for API, UI Contracts, and E2E Flow

**Files:**
- Create: `tests/test_web_api.py`
- Create: `tests/test_web_ui_smoke.py`

- [ ] **Step 1: Add `/chat` integration test asserting answer + citations + chunks fields**
- [ ] **Step 2: Add `/upload` + `/reindex` flow test**
- [ ] **Step 3: Add `/feedback` persistence test with bad-answer trace expectation**
- [ ] **Step 4: Add end-to-end test `upload -> reindex -> ask -> citation visible`**
- [ ] **Step 5: Add UI smoke tests for evidence rendering contracts**
- [ ] **Step 6: Run targeted tests and confirm RED failures**

### Task 2: Implement FastAPI Endpoints and Persistence

**Files:**
- Create: `src/lkb/api.py`
- Modify: `src/lkb/store.py`
- Modify: `src/lkb/pipeline.py`
- Modify: `src/lkb/sql/001_issue02_schema_up.sql`
- Modify: `src/lkb/models.py`

- [ ] **Step 1: Add request/response models and endpoint handlers**
- [ ] **Step 2: Add feedback-event and bad-answer storage helpers**
- [ ] **Step 3: Return answer/query ids needed for feedback linkage**
- [ ] **Step 4: Wire upload/reindex contracts and error handling**
- [ ] **Step 5: Re-run targeted tests and reach GREEN**

### Task 3: Implement Streamlit UI and Runtime Entry Points

**Files:**
- Create: `apps/streamlit_app.py`
- Create: `scripts/run_api.py`
- Create: `scripts/run_ui.py`

- [ ] **Step 1: Build UI panes for answer, citations, and retrieved chunks**
- [ ] **Step 2: Add upload/reindex controls and feedback actions**
- [ ] **Step 3: Add basic error and session-state handling**
- [ ] **Step 4: Re-run smoke tests and e2e checks**

### Task 4: Verify, Document, and Release

**Files:**
- Modify: `docs/issues/05-web-ui-and-feedback-loop.md`

- [ ] **Step 1: Run full verification commands and capture outputs**
- [ ] **Step 2: Update issue doc with shipped details, evidence, metrics, release notes, migration/config, rollback**
- [ ] **Step 3: Sync GitHub issue + open PR + merge + close issue**

