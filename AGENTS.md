# AGENTS.md

## Project Goal

Build a **personal knowledge-base AI system** incrementally, shipping in small deployable milestones.

Primary source of truth for roadmap:
- `docs/personal_knowledge_base_roadmap.md`
- `docs/issues/README.md`
- `docs/issues/01-markdown-rag-mvp.md` ... `docs/issues/12-guardrails-query-intelligence-and-agent-tools.md`

Execution principle:
- Build in sequence, one issue at a time.
- Each issue must be deployable independently with clear tests and measurable success criteria.

---

## Engineering Principles

- Prefer **working -> inspectable -> measurable -> extensible -> reliable**.
- Keep changes minimal and focused on the active issue.
- Do not implement future-phase features early unless explicitly requested.
- Preserve backward compatibility with previously shipped issues.
- Never claim completion without running verification relevant to changed scope.

---

## Required Skills / Workflows

When working in this repo, apply these skills in order when relevant:

1. `using-superpowers` at session start.
2. `brainstorming` before creative design or feature-shaping work.
3. `writing-plans` before multi-step implementation.
4. `test-driven-development` for feature/bug implementation.
5. `systematic-debugging` for failures/regressions.
6. `verification-before-completion` before declaring done.
7. `requesting-code-review` before merge/handoff on major changes.

Use supporting skills as needed:
- `subagent-driven-development` for independent implementation tasks.
- `executing-plans` when implementing from an approved plan.
- `finishing-a-development-branch` at integration time.

---

## Delivery Contract Per Issue

For each active issue (`docs/issues/*.md`), implementation must include:

- Scope alignment with the issue document.
- Tests:
  - unit tests for core logic
  - integration/end-to-end checks for critical flow
- Evidence:
  - command outputs for test/verification runs
  - metric values tied to the issue success criteria
- Release notes:
  - what shipped
  - migration/config changes
  - rollback path

---

## Repo Conventions

- Put new planning/spec docs under `docs/`.
- Put issue decomposition under `docs/issues/`.
- Prefer explicit file/module names over ambiguous utilities.
- Avoid unrelated refactors during issue execution.

---

## Default Execution Order

Implement in this order unless explicitly overridden:

1. `01-markdown-rag-mvp`
2. `02-schema-and-incremental-indexing`
3. `03-retrieval-eval-harness`
4. `04-hybrid-search-and-reranking`
5. `05-web-ui-and-feedback-loop`
6. `06-pdf-docx-html-ingestion`
7. `07-audio-ingestion-and-timestamp-citations`
8. `08-video-ingestion-ocr-and-visual-indexing`
9. `09-capture-workflows-and-auto-sync`
10. `10-knowledge-organization-and-memory`
11. `11-production-backend-and-async-ingestion`
12. `12-guardrails-query-intelligence-and-agent-tools`

