# Issue 05 - Web UI and Feedback Loop

## Goal
Ship a daily-usable UI that exposes answers, evidence, and user feedback.

## Scope
- In: chat UI, source panel, retrieved chunks panel, upload, re-index action, thumbs feedback.
- Out: multimodal ingestion.

## Deliverables
- FastAPI endpoints for chat/upload/feedback
- Streamlit or Next.js frontend for query and evidence display
- Logging for bad answers and feedback events

## Implementation Tasks
1. Add API endpoints and request/response contracts.
2. Build chat + evidence UI panes.
3. Add upload + re-index controls.
4. Persist feedback and bad-answer logs.
5. Add basic session and error handling UX.

## Tests
- API integration tests for chat/upload/feedback.
- UI smoke tests for main user flow.
- End-to-end test: upload -> index -> ask -> citation visible.

## Definition of Done
- App usable for one-week internal dogfooding.
- Sources visible next to answers.
- Feedback stored and queryable.
- Bad answers logged with retrieval trace.

## Success Metrics
- `weekly_active_days >= 5` (personal usage week).
- `citation_panel_render_success = 100%` in E2E suite.

## Deployment
- Release tag: `v0.5.0-web-ui`
- Deployment runbook includes startup and rollback steps.

---

## Implementation Status
Completed on branch `issue-05-web-ui-feedback-loop`.

## What Shipped
- Added FastAPI application with endpoints:
  - `POST /chat`
  - `POST /upload`
  - `POST /reindex`
  - `POST /feedback`
  - `GET /feedback/events`
  - `GET /feedback/bad-answers`
  - file: `src/lkb/api.py`
- Added Streamlit frontend:
  - chat answer pane
  - citations/source panel
  - retrieved chunk evidence panel
  - upload + re-index controls
  - thumbs feedback controls
  - file: `apps/streamlit_app.py`
- Added runtime entry scripts:
  - `scripts/run_api.py`
  - `scripts/run_ui.py`
- Added UI contract helpers:
  - `src/lkb/web_ui_helpers.py`
- Extended persistence for feedback and bad-answer traces:
  - `feedback_events` table
  - `bad_answer_logs` table
  - store helpers in `src/lkb/store.py`
  - schema updates in `src/lkb/sql/001_issue02_schema_up.sql` and rollback updates in `src/lkb/sql/001_issue02_schema_down.sql`
- Extended ask results to include query/answer ids for feedback linking:
  - `src/lkb/models.py`
  - `src/lkb/pipeline.py`
- Added tests:
  - `tests/test_web_api.py`
  - `tests/test_web_ui_smoke.py`
- Added dependency manifest:
  - `requirements.txt`

## Code Review Findings and Resolution
1. **Finding:** Streamlit feedback could attach an edited input question instead of the actual asked question.
   - **Resolution:** persisted `last_question` in session state when chat succeeds and used it for thumbs submissions.
2. **Finding:** Down migration script did not include newly added feedback log tables.
   - **Resolution:** updated `src/lkb/sql/001_issue02_schema_down.sql` to drop `feedback_events` and `bad_answer_logs`.

## Verification Evidence

### Targeted Issue 05 Tests
Command:
```powershell
$env:PYTHONPATH='src'; python -m unittest tests.test_web_api tests.test_web_ui_smoke -v
```

Result:
- `Ran 6 tests in 5.367s`
- `OK`

### Full Regression Suite
Command:
```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests -v
```

Result:
- `Ran 27 tests in 14.594s`
- `OK`

### E2E Flow Evidence (upload -> index -> ask -> citation visible)
- Validated by `tests.test_web_api.WebApiIntegrationTests.test_upload_reindex_then_ask_has_citation`.
- Assertion ensures citation list includes uploaded file path (`topic-99.md`) after upload/reindex/query.

## Success Metrics
- `citation_panel_render_success = 100%` in automated E2E checks:
  - **Actual:** `100%` (`1/1` end-to-end citation visibility checks passed) ✅
- `weekly_active_days >= 5` (personal usage week):
  - **Current:** `not yet measurable in CI session` (operational post-release metric to track during first dogfooding week) ⚠️

## Release Notes
- Introduced a deployable web UI stack for daily usage:
  - FastAPI backend for chat/upload/reindex/feedback
  - Streamlit frontend with evidence visibility and feedback UX
- Added persistent feedback event logs and bad-answer retrieval traces to support quality iteration.
- Preserved existing retrieval/indexing behavior and backward compatibility for prior CLI and test flows.

## Migration / Config Changes
1. Install dependencies:
   - `python -m pip install -r requirements.txt`
2. Start API:
   - `$env:PYTHONPATH='src'; python scripts/run_api.py --kb-dir kb --index-dir .index --host 127.0.0.1 --port 8000`
3. Start UI:
   - `$env:PYTHONPATH='src'; python scripts/run_ui.py --api-base-url http://127.0.0.1:8000 --port 8501`

## Rollback Path
1. Stop UI/API processes.
2. Revert Issue 05 commit(s) that add:
   - `src/lkb/api.py`
   - `apps/streamlit_app.py`
   - new schema table usage in `store.py` and SQL migration files
3. Optional data rollback:
   - apply `src/lkb/sql/001_issue02_schema_down.sql` then re-apply baseline schema up script if a clean schema reset is required.
4. Re-run verification:
   - `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v`
