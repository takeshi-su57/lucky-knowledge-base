# Issue 03 Retrieval Eval Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a repeatable retrieval evaluation harness with golden questions, core retrieval/answer metrics, baseline regression comparison, and machine-readable/markdown reports.

**Architecture:** Add a small eval module in `src/lkb/eval_harness.py` that loads a golden dataset, evaluates retrieval results via existing `ask_question`, computes metrics, and renders stable JSON/Markdown reports. Keep CLI orchestration in `scripts/run_eval.py` and store fixtures/baselines under `evals/`.

**Tech Stack:** Python stdlib (`unittest`, `json`, `datetime`, `pathlib`), existing local `lkb.pipeline` APIs.

---

### Task 1: Add Tests First for Eval Metrics and Report Contract

**Files:**
- Create: `tests/test_eval_harness.py`

- [ ] **Step 1: Write failing unit tests for top-k, MRR, citation accuracy, unknown-answer accuracy**
- [ ] **Step 2: Write failing contract test for report schema stability keys**
- [ ] **Step 3: Write failing integration-style test for mini seeded corpus evaluation flow**
- [ ] **Step 4: Run test module to confirm failures before implementation**

### Task 2: Implement Eval Harness Core

**Files:**
- Create: `src/lkb/eval_harness.py`

- [ ] **Step 1: Implement dataset loader (JSON-compatible YAML handling)**
- [ ] **Step 2: Implement evaluation loop calling existing retrieval pipeline**
- [ ] **Step 3: Implement metrics: top-1/top-3/top-5, MRR, citation accuracy, unknown-answer accuracy**
- [ ] **Step 4: Implement baseline comparison deltas and failed-example inspector output**
- [ ] **Step 5: Implement JSON + Markdown report renderers with stable schema**
- [ ] **Step 6: Re-run tests and make them pass**

### Task 3: Add CLI + Dataset + Baseline Artifact

**Files:**
- Create: `scripts/run_eval.py`
- Create: `evals/test_questions.yaml`
- Create: `evals/baseline_report.json`

- [ ] **Step 1: Implement CLI args for kb/index/report/baseline paths**
- [ ] **Step 2: Add >=50 golden questions mapped to corpus files and unknown prompts**
- [ ] **Step 3: Run eval once to generate initial baseline report artifact**
- [ ] **Step 4: Verify regression block includes deltas for all key metrics**

### Task 4: Update Issue Doc and Verify End-to-End

**Files:**
- Modify: `docs/issues/03-retrieval-eval-harness.md`

- [ ] **Step 1: Run targeted and full verification commands**
- [ ] **Step 2: Capture outputs and metrics in issue doc**
- [ ] **Step 3: Add release notes, migration/config, rollback details**
