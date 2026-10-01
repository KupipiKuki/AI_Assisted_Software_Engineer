# Implementation Plan & Task Baseline

**Work Item ID:** WI-{{ID}}  
**Design Reference:** [DESIGN.md](./DESIGN.md)  
**Assigned Coder Model:** {{CODER_MODEL}} (e.g., Local Qwen2.5-Coder:14b / Ollama)  
**Assigned QA Model:** {{QA_MODEL}} (e.g., Gemini 2.5 Flash)  
**Assigned Auditor Model:** {{AUDITOR_MODEL}} (e.g., Gemini 2.5 Pro)  
**Git Branch Baseline:** `dev/WI-{{ID}}` (or `qwen-dev`)  
**Status:** PROPOSED | APPROVED | IN_PROGRESS | COMPLETED  

---

## 1. Acceptance Criteria Mapping
*Each criterion must be objective, verifiable, and testable by QA.*

| Criterion ID | Description | Validation Method | Assigned QA Test |
|---|---|---|---|
| AC-1 | | Automated Unit Test | `tests/unit/test_*.py` |
| AC-2 | | Integration / Boundary Test | `tests/integration/test_*.py` |
| AC-3 | | Performance / Benchmark | Benchmark runner |

---

## 2. Decomposed Tasks
*Sequenced in small, verifiable units. Local Coder works on one task at a time.*

### Task 1: {{Task Title}}
- **Task ID:** T-1
- **Target Files:** `src/path/to/file.py`, `tests/test_file.py`
- **Dependencies:** None
- **Scope:** 
- **Unit Tests Required:**
- **Completion Condition:** Local unit test passes; diff contains no out-of-scope edits.

### Task 2: {{Task Title}}
- **Task ID:** T-2
- **Target Files:**
- **Dependencies:** T-1
- **Scope:**
- **Unit Tests Required:**
- **Completion Condition:**

---

## 3. Test & Verification Plan
- **Pre-execution Baseline Test Command:** `pytest tests/`
- **Unit Test Coverage Requirement:**
- **Regression Check Command:**

---

## 4. Execution Guardrails
- **Max Coder-QA Rework Cycles:** 3 (automatic human escalation if exceeded)
- **Branch Freezing:** While Gemini Auditor evaluates milestone, Coder is locked out of touched files.
- **Atomic PR Target:** Clean, single-purpose commits per task.
