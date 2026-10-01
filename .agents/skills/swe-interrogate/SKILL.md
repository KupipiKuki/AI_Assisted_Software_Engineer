---
name: swe-interrogate
description: >-
  Adversarial multi-perspective code and security review skill.
  Applies rigorous pressure across multiple lenses (Architecture, Correctness, Security, Performance,
  and Code Hygiene) to interrogate a pull request or git diff before final milestone approval.
---

# SWE Interrogate (Adversarial Multi-Lens Code Review)

The **SWE Interrogate** skill subjects a code diff to rigorous adversarial pressure across multiple specialized lenses before allowing a milestone or pull request to merge.

## When to Use
- Before marking Gate G5 (Milestone Accepted) in [`swe-auditor`](../swe-auditor/SKILL.md).
- When preparing a pull request for human sign-off.
- On security-critical or shared infrastructure modifications.

---

## The 5 Interrogation Lenses

### Lens 1: Architectural & Contract Integrity
- Does this change violate module layering or encapsulation?
- Are new public functions properly typed and documented?
- Does it leak internal implementation details to external callers?
- Did it introduce circular dependencies?

### Lens 2: Correctness & Edge Cases
- What happens on `null`, `None`, empty strings, zero, or max-int values?
- Are off-by-one errors possible in loop or slice bounds?
- Are errors and exceptions caught at the right granularity?
- Is there any silent failure or swallowed exception?

### Lens 3: Security & Privacy (SWEBOK & OWASP)
- Are untrusted inputs sanitized before reaching SQL, shell commands, or file system paths?
- Are credentials, tokens, or personal identifiers (PII) exposed in logs or commits?
- Are authorization checks performed before privileged operations?

### Lens 4: Performance & Resource Lifecycle
- Are there hidden N+1 queries, unindexed searches, or quadratic loops?
- Are files, database connections, and network sockets explicitly closed (e.g., using context managers)?
- Could this create an unbounded memory leak under continuous load?

### Lens 5: Hygiene & "Unslop"
- Strip useless AI boilerplate comments (e.g., `// This function returns x`).
- Ensure variable and function names convey explicit intent.
- Ensure formatting adheres strictly to repository linters.

---

## Interrogation Report Output

Produce a structured markdown section in the review thread or audit package:

```markdown
### Adversarial Interrogation Findings
- **Lens 1 (Architecture):** PASS
- **Lens 2 (Correctness):** 1 Finding (Potential None-dereference in `parser.py:42`)
- **Lens 3 (Security):** PASS
- **Lens 4 (Performance):** PASS
- **Lens 5 (Hygiene):** 2 trivial comments removed
```
