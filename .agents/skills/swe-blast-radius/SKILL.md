---
name: swe-blast-radius
description: >-
  Impact and blast-radius analysis skill for software changes.
  Traces callers, data flow, dependencies, and external consumers of modified functions or types.
  Use before refactoring, modifying shared interfaces, or updating dependencies.
---

# SWE Blast Radius (Change Impact Analysis)

The **SWE Blast Radius** skill calculates the full downstream ripple effect of a proposed modification to an interface, function, schema, or configuration.

## When to Use
- During Phase G1 (Architect design phase) when touching shared components.
- During Phase G4 (QA inspection) to determine which regression suites must be run.
- Before deprecating or altering existing APIs.

---

## 4-Step Blast Radius Analysis Procedure

### Step 1: Symbol & Signature Mapping
Identify all exact symbols (types, classes, functions, constants) being modified:
```bash
# Example: Find all imports and usages across codebase
rg "def calculate_tax" src/
rg "from billing.tax import" src/
```

### Step 2: Caller Tree & Dependency Graph
Trace direct callers, indirect callers, and external serialization contracts:
1. **Direct Callers**: Modules that directly call the modified symbol.
2. **Indirect Callers**: Upstream workflows triggered by direct callers.
3. **Data Schemas & Serialization**: Database tables, serialized JSON payloads, REST/gRPC contracts, and event messages.

### Step 3: Risk Classification Matrix

| Scope | Direct Callers | External Contracts Touched | Risk Level | Required Verification |
|---|---|---|---|---|
| **Isolated** | 1 (internal to module) | None | **LOW** | Focused unit test only |
| **Shared Internal** | > 1 (internal packages) | None | **MODERATE** | Full integration test suite |
| **Public / Boundary** | Any external consumer | Public API / DB / Queue | **HIGH** | Milestone audit + Backward compatibility test |

### Step 4: Blast Radius Report Output
Produce a blast radius section for `DESIGN.md` or `QA_REPORT.md`:

```markdown
### Blast Radius Summary
- **Symbols Changed:** `billing.calculator.process_invoice()`
- **Direct Callers (3):** `routes/api/checkout.py`, `workers/recurring_billing.py`, `cli/admin_recalc.py`
- **Data Serialization Impact:** Adds optional field `tax_breakdown` (non-breaking, backward compatible)
- **Required Test Suites:** `tests/unit/test_calculator.py`, `tests/integration/test_checkout.py`, `tests/e2e/test_billing.py`
- **Risk Assessment:** MODERATE
```
