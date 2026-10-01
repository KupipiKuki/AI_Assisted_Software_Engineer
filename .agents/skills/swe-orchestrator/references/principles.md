# Core Engineering Principles for AI Software Engineering Teams

These principles guide decisions across all roles (Architect, Coder, QA, Auditor). Derived from **SWEBOK v4** and proven multi-agent paradigms (**pstack**).

---

## 1. Architectural & Design Discipline

- **Foundational Thinking**: Get the data structures, core types, and component relationships right first. Downstream implementation logic becomes straightforward once the data model is sound.
- **Boundary Discipline**: Concentrate guards, validation, and serialization at system boundaries (API endpoints, CLI parsers, config files, network calls). Keep internal domain logic pure and rely on verified internal types.
- **Type-System Discipline**: Make illegal states unrepresentable. Prefer algebraic data types, explicit enums, and discriminated unions over vague primitive types or `any`. Refuse to lie to the compiler or type checker.
- **Exhaust the Design Space**: For complex architectural choices, evaluate at least two structurally distinct candidate designs before committing.
- **Redesign from First Principles**: When fundamental requirements shift, redesign as if the requirement had been a day-one assumption, rather than bolting on fragile shims.

---

## 2. Construction & Coding Hygiene

- **Laziness Protocol**: Bias toward deletion and the smallest coherent change that solves the problem. Do not add speculative abstractions.
- **Subtract Before You Add**: Clean up dead code, redundant branches, and obsolete wrappers before adding new features.
- **Minimize Reader Load**: Collapse single-caller wrappers, shrink mutable scope, and keep the distance between a question and its answer as short as possible.
- **Fix Root Causes**: Trace every defect to its root cause and eliminate it there. Avoid nil-check guards or catch-all exception swallowers that mask bugs.
- **Test Behavior, Not Implementation**: Call code the way real consumers call it, asserting externally observable results rather than internal mock interactions.

---

## 3. Multi-Model & Independence Governance

- **Separation of Duties**: The Coder model must never review or validate its own code as QA. The Architect must never audit its own milestone as Auditor.
- **Guard the Context Window**: Use local models for bulk file generation; prune context by transmitting contracts, signatures, and diffs instead of entire repositories.
- **Evidence Before Disposition**: No gate or milestone may be accepted based solely on agent claims or self-reports. All claims must be backed by diffs, test logs, and reproducible console outputs.
- **Loop Breakers**: Automatically cap Coder-QA rework cycles at 3. Escalate immediately to human review if unresolved.
