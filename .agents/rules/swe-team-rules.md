---
description: >-
  Rules and operating constraints for the AI Software Engineering Team.
  Enforces separation of duties, model assignments, phase gates G0-G6, and GitOps branching.
always_on: true
---

# AI Software Engineering Team Operating Rules

Whenever performing software engineering tasks in this workspace, strictly adhere to the following operating standards:

## 1. Operating Model & Separation of Duties
- **Architect**: High-level reasoning, system design, and `PLAN.md` decomposition. Uses online frontier models (Gemini 2.5 Pro). Does not implement production code as Coder.
- **Coder**: Daily implementation, syntax generation, and local unit testing. Offloaded to local LLMs (Ollama `qwen2.5-coder:14b/32b`) to minimize cloud cost and avoid rate limits.
- **QA**: Independent validation, test suite execution, boundary tests, and triage. Uses fast online models (Gemini 2.5 Flash). Never uses the same model session as Coder.
- **Auditor**: Milestone auditing, architectural drift detection, security assessment, and disposition. Uses independent frontier models (Gemini 2.5 Pro). Never uses the same model session as Architect.

## 2. Evidence Before Disposition
- Never claim a task or gate is complete based on assertions alone.
- Every handoff and gate transition must be backed by concrete artifacts:
  - `DESIGN.md` (Gate G1)
  - `PLAN.md` (Gate G2)
  - `HANDOFF.md` with passing test output & diff (Gate G3)
  - `QA_REPORT.md` with reproducible commands (Gate G4)
  - `AUDITOR_DECISION.md` with holistic checks (Gate G5)

## 3. GitOps Branching Discipline
- `main`: Protected production branch. No direct commits. Merges require Gate G6 release approval.
- `dev` (or `dev/feature-name`): The active builder branch where Coder and QA iterate.
- `audit/milestone-name`: Ephemeral audit branch created by Auditor. When active, `dev` is frozen.

## 4. Loop Breakers & Human Escalation
- Maximum 3 rework iterations between Coder and QA. If a defect recurs 3 times, pause and escalate to the human supervisor.
- Maximum 2 architectural plan revisions before requesting human guidance.
- Any destructive operation, secret handling, or infrastructure change requires explicit human confirmation.
