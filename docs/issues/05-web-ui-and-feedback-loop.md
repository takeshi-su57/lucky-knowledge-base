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
