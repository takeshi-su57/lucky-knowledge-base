# Issue 04 Hybrid Search and Reranking Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship hybrid retrieval (dense + keyword + reranking), strategy toggles, and measurable quality gains over vector-only retrieval.

**Architecture:** Extend retrieval as additive modules (`keyword_retriever`, `hybrid_retriever`, `reranker`) and minimally wire strategy selection into pipeline and CLI/eval entrypoints. Preserve existing behavior under `vector_only`, and verify improvements with eval metrics.

**Tech Stack:** Python stdlib (`unittest`, `collections`, `math`), existing `lkb` modules and CLI scripts.

---

### Task 1: Add Failing Tests for Hybrid Retrieval Components

**Files:**
- Modify: `tests/test_integration_rag.py`
- Create: `tests/test_hybrid_retrieval.py`

- [ ] **Step 1: Add unit tests for keyword retriever ranking and acronym/exact-term behavior**
- [ ] **Step 2: Add unit tests for hybrid merge/dedupe ordering and metadata filter application**
- [ ] **Step 3: Add unit tests for reranker reordering behavior**
- [ ] **Step 4: Add integration tests for exact-term query success under hybrid strategy**
- [ ] **Step 5: Run targeted tests and confirm RED failures**

### Task 2: Implement Keyword, Hybrid, and Reranker Modules

**Files:**
- Create: `src/lkb/retrieval/keyword_retriever.py`
- Create: `src/lkb/retrieval/hybrid_retriever.py`
- Create: `src/lkb/retrieval/reranker.py`
- Create: `src/lkb/retrieval/vector_retriever.py`
- Create: `src/lkb/retrieval/__init__.py`
- Modify: `src/lkb/retrieval.py`

- [ ] **Step 1: Implement keyword retrieval scoring with IDF-like term weighting**
- [ ] **Step 2: Implement merge/dedupe with stable score normalization**
- [ ] **Step 3: Implement metadata filter helper shared across retrieval strategies**
- [ ] **Step 4: Implement reranker using lexical/semantic blend**
- [ ] **Step 5: Keep legacy imports/behavior backward-compatible**
- [ ] **Step 6: Re-run targeted tests and reach GREEN**

### Task 3: Wire Retrieval Strategy Selection and Evaluation Comparison

**Files:**
- Modify: `src/lkb/pipeline.py`
- Modify: `scripts/ask.py`
- Modify: `src/lkb/eval_harness.py`
- Modify: `scripts/run_eval.py`
- Modify: `tests/test_eval_harness.py`

- [ ] **Step 1: Add retrieval strategy arg (`vector_only` or `hybrid`) in pipeline and CLI**
- [ ] **Step 2: Add eval helper that compares strategies and computes `top5_accuracy_delta`**
- [ ] **Step 3: Add exact-term query success metric calculation**
- [ ] **Step 4: Add tests for strategy selection and metric fields**
- [ ] **Step 5: Re-run related tests and confirm GREEN**

### Task 4: Verify, Document, and Ship

**Files:**
- Modify: `docs/issues/04-hybrid-search-and-reranking.md`

- [ ] **Step 1: Run full verification commands and capture outputs**
- [ ] **Step 2: Run eval command and capture final metrics**
- [ ] **Step 3: Update issue doc with implementation details, evidence, release notes, migration/config, rollback**
- [ ] **Step 4: Sync GitHub issue status, open PR, merge, and close issue**
