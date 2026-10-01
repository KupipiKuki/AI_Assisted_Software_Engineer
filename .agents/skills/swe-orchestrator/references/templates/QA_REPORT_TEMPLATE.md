# Independent QA Validation Report

**Work Item ID:** WI-{{ID}}  
**Task ID / Milestone:** T-{{ID}}  
**QA Model:** {{QA_MODEL}} (e.g., Gemini 2.5 Flash)  
**Target Code Revision / Commit:** {{COMMIT_HASH}}  
**Date:** {{DATE}}  
**Overall Disposition:** PASS | CODER_FIX_REQUIRED | QA_CORRECTION_REQUIRED | ARCHITECT_REVIEW_REQUIRED | BLOCKED  

---

## 1. Test Execution & Evidence Log
*All test commands must be exact, automated, and reproducible.*

| Test Suite / Command | Execution Time | Passed | Failed | Status |
|---|---|---|---|---|
| `pytest tests/unit/` | 1.2s | 14 | 0 | PASS |
| `pytest tests/integration/` | 3.5s | 4 | 0 | PASS |
| `pytest tests/qa_adversarial/` | 0.8s | 3 | 1 | FAIL |

### Execution Console Output Snippet
```text
{{PASTE_TEST_RESULTS}}
```

---

## 2. Independent Test Additions
*Tests created by QA that were not authored by Coder (Boundary, Negative, Concurrency, Fuzzing).*

- **New Test Files Added:** `tests/qa_adversarial/test_edge_cases.py`
- **Scenarios Tested:**
  - Null / Empty input handling
  - Extremely large payload / buffer limits
  - Malformed network/data input
  - Race condition / concurrent invocation

---

## 3. Scope & Diff Inspection Findings
*Review of `git diff` for out-of-scope edits, unnecessary dependencies, commented-out dead code, or architecture violations.*

- **Scope Adherence:** FULLY_ALIGNED | SCOPE_CREEP_DETECTED
- **Observations:**

---

## 4. Defect Findings & Classification
*Only filled if defects were identified.*

### Finding DF-1
- **Severity:** CRITICAL | HIGH | MEDIUM | LOW
- **Type:** LOGIC_ERROR | REGRESSION | BOUNDARY_FAILURE | PERFORMANCE | SECURITY
- **Description:** 
- **Reproduction Steps / Command:**
- **Assigned Route:** Coder fix required | Architect review required

---

## 5. Acceptance Criteria Status

| Criterion ID | Expected Behavior | Observed Behavior | Status |
|---|---|---|---|
| AC-1 | | | VERIFIED |
| AC-2 | | | VERIFIED |

---

## 6. Recommended Next Action
- [ ] Advance to Milestone Review (Auditor)
- [ ] Route back to Coder for localized bug fix (Cycle count: {{N}}/3)
- [ ] Route back to Architect for spec/interface ambiguity
- [ ] Escalate to Human Supervisor
