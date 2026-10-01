---
name: swe-orchestrator
description: >-
  Lead orchestrator for the multi-agent AI software engineering team.
  Coordinates Architect (Gemini Pro), Coder (Local Ollama Qwen2.5-Coder), QA (Gemini Flash),
  and Auditor (Gemini Pro) through Phase Gates G0 to G6. Use when starting a software project,
  executing a multi-step feature, managing defect triage, or driving milestone audits.
---

# SWE Team Orchestrator

The **SWE Team Orchestrator** manages a multi-agent software engineering lifecycle. It coordinates specialized AI roles, pairs local LLMs with online frontier models, enforces phase gates, and maintains GitOps state flow.

```mermaid
flowchart TD
    Human([Human / Product Owner]) --> G0[G0: Intake Ready]
    G0 -->|Task & Scope| Architect[swe-architect<br/><i>Gemini 2.5 Pro</i>]
    
    subgraph Design & Planning
        Architect -->|DESIGN.md| G1[G1: Design Complete]
        G1 -->|PLAN.md| G2[G2: Plan Ready]
    end
    
    subgraph Local Implementation Loop
        G2 -->|Task Scope & Contracts| Coder[swe-coder<br/><i>Ollama Qwen2.5-Coder</i>]
        Coder -->|Code & Tests| G3[G3: Implementation Complete]
        G3 -->|HANDOFF.md & Diff| QA[swe-qa<br/><i>Gemini 2.5 Flash</i>]
        QA -->|QA_REPORT.md| G4{G4: QA Complete}
        G4 -- Pass --> G5_Check[Milestone Ready]
        G4 -- Coder Fix -->|Defect Findings| Coder
        G4 -- Spec Issue -->|Plan Ambiguity| Architect
    end

    subgraph Milestone Audit
        G5_Check --> Auditor[swe-auditor<br/><i>Gemini 2.5 Pro (Independent)</i>]
        Auditor -->|AUDITOR_DECISION.md| G5{G5: Milestone Accepted}
        G5 -- Accept --> G6[G6: Release Approved]
        G5 -- Escalate --> Human
    end
```

## Model Matrix & Separation of Duties

| Role | Assigned Model | Host / Runtime | Primary Function | Independence Boundary |
|---|---|---|---|---|
| **Architect** | Gemini 2.5 Pro | Google AI / Cloud | System architecture, interfaces, `PLAN.md` | Cannot code implementation as Coder |
| **Coder** | Qwen2.5-Coder (14B/32B) | Local Ollama (`:11434`) | Implementation, local unit testing, refactoring | Cannot validate own work as QA |
| **QA** | Gemini 2.5 Flash | Google AI / Cloud | Independent validation, boundary tests, triage | Must use independent session/model from Coder |
| **Auditor** | Gemini 2.5 Pro | Google AI / Cloud | Milestone audit, drift check, security, disposition | Must use independent session/model from Architect |

---

## Operating Protocol

### Step 1: Intake & Gate G0 Check
1. Capture feature request or defect description.
2. Confirm the scope, repository targets, constraints, and initial acceptance criteria.
3. Activate the [`swe-architect`](../swe-architect/SKILL.md) skill.

### Step 2: Architecture & Planning (Gates G1 & G2)
1. Architect produces [`DESIGN.md`](./references/templates/DESIGN_TEMPLATE.md) (types, interfaces, data flow, failure modes).
2. Architect decomposes the work into [`PLAN.md`](./references/templates/PLAN_TEMPLATE.md) (atomic tasks, file scopes, test requirements).
3. If risk is high, request human confirmation before proceeding to code.

### Step 3: Local Implementation & Testing (Gate G3)
1. Switch to active development branch (e.g., `dev` or `dev/feature-name`).
2. Dispatch tasks to [`swe-coder`](../swe-coder/SKILL.md).
3. Coder utilizes [`swe-local-bridge`](../swe-local-bridge/SKILL.md) to generate code with local Qwen2.5-Coder.
4. Coder runs local unit tests and compiles [`HANDOFF.md`](./references/templates/HANDOFF_TEMPLATE.md).

### Step 4: Independent QA Validation (Gate G4)
1. Invoke [`swe-qa`](../swe-qa/SKILL.md).
2. QA runs full test suite, adds targeted boundary/negative tests, and inspects the diff.
3. QA generates [`QA_REPORT.md`](./references/templates/QA_REPORT_TEMPLATE.md).
4. **Triage Loop**:
   - If findings require fixes: route back to Coder (tracked cycle count).
   - If cycle count exceeds **3**: trigger automatic human escalation.
   - If QA passes: advance to milestone audit.

### Step 5: Milestone Audit & Drift Check (Gate G5)
1. Freeze `dev` branch. Create milestone audit branch `audit/milestone-name`.
2. Invoke [`swe-auditor`](../swe-auditor/SKILL.md).
3. Auditor verifies compliance against `PLAN.md`, writes E2E/integration tests, inspects security posture, and files [`AUDITOR_DECISION.md`](./references/templates/AUDITOR_DECISION_TEMPLATE.md).

### Step 6: Release Boundary (Gate G6)
1. Present the audit package and disposition to the human developer.
2. Upon human sign-off, merge the tested changes into `main`.

---

## Escalation & Loop Breakers

- **Coder-QA Loop Cap**: Maximum 3 rework iterations per task. If QA rejects the 3rd attempt, halt and summarize root causes for human intervention.
- **Architectural Revision Cap**: Maximum 2 design revisions before pausing for user alignment.
- **Security / Destructive Action Stop**: Any task modifying credentials, deployment infrastructure, or external APIs halts immediately for human confirmation.
