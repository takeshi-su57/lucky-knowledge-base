# Issue 05 Web UI and Feedback Loop Design

## Goal
Ship a daily-usable web interface with explicit evidence display, upload/re-index controls, and persisted user feedback/bad-answer logging.

## Scope Alignment
- In scope:
  - FastAPI endpoints for `chat`, `upload`, `reindex`, and `feedback`
  - Streamlit frontend with chat pane, citations panel, retrieved chunk panel, and controls
  - feedback event logging and bad-answer trace logging
  - basic session and API error handling UX
- Out of scope:
  - multimodal ingestion (PDF/audio/video)
  - non-local authentication or multi-user security model

## Proposed Architecture
1. Add an API layer (`src/lkb/api.py`) that wraps existing pipeline/indexing functions.
2. Extend store operations with explicit feedback-event and bad-answer persistence while preserving existing query/answer records.
3. Add a Streamlit app (`apps/streamlit_app.py`) that calls API endpoints and renders:
   - answer text
   - citation/source panel
   - retrieved chunk evidence panel
   - upload and re-index controls
   - thumbs feedback controls
4. Keep API contracts small and explicit to support future UI replacement without backend rewrites.

## Data Flow
1. User uploads markdown via `/upload` and triggers `/reindex`.
2. User asks via `/chat`; backend retrieves chunks, returns answer + citations + chunk evidence + ids.
3. UI renders answer plus evidence panels.
4. User submits thumbs/comment via `/feedback`.
5. Backend stores feedback event and logs bad-answer trace on negative feedback.

## Error Handling and Session Behavior
- API returns structured errors (`detail`) for invalid payloads and missing feedback targets.
- UI keeps lightweight per-browser-session state (latest answer id, latest chat payload) and displays inline errors when endpoint calls fail.
- Re-index operation returns summary metrics to show immediate system state.

## Test Strategy
- API integration tests:
  - `/chat` returns answer, citations, and chunk evidence
  - `/upload` stores file and `/reindex` returns index report
  - `/feedback` persists event and bad-answer log
- UI smoke tests:
  - verify payload shaping and rendering data contracts for answer/evidence panels
- E2E test:
  - upload -> reindex -> ask -> citation panel non-empty

## Success Metrics
- `citation_panel_render_success = 100%` in automated E2E checks
- `weekly_active_days >= 5` tracked as a dogfooding target (cannot be proven in one CI run; documented as operational follow-up)

## Tradeoff Decision
Choose Streamlit for fastest deployable UI iteration in this milestone while keeping backend contracts framework-neutral for a later Next.js migration if needed.

