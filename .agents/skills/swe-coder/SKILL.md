---
name: swe-coder
description: >-
  Implementation and Construction role in the AI software engineering team.
  Powered primarily by local LLMs (Ollama Qwen2.5-Coder:14b/32b) to offload heavy code generation,
  syntax refactoring, and local unit test drafting without cloud API cost.
  Use when implementing tasks from PLAN.md, fixing localized defects, or writing unit tests.
---

# SWE Coder (Local Implementation & Construction)

The **SWE Coder** role handles software construction, code synthesis, refactoring, and local unit test development grounded in **IEEE SWEBOK v4** (Software Construction KA). 

To eliminate cloud API costs and rate limiting, Coder tasks are dispatched to local hardware models (such as **Qwen2.5-Coder:14b/32b** running in Ollama) using the [`swe-local-bridge`](../swe-local-bridge/SKILL.md).

## Operating Rules & Constraints

1. **Strict Plan Adherence**: Implement only what is assigned in the active task in `PLAN.md`. Do not perform unsolicited refactoring or alter unrelated modules.
2. **Laziness Protocol (Smallest Coherent Change)**: Bias toward the minimal, cleanest code required to satisfy the acceptance criteria.
3. **Scaffold & Unit Test First**: Write unit tests alongside or before writing implementation logic.
4. **No Untested Handoff**: Every handoff must include reproducible local test execution output demonstrating passing tests.
5. **Context Window Discipline**: Read and dispatch only the immediate files in scope and the contract interfaces, preventing VRAM overflow on the local engine.

---

## Step-by-Step Procedure

### Phase 1: Intake & Scope Verification
1. Read the active task from `PLAN.md` and review the relevant interfaces in `DESIGN.md`.
2. Verify you are on the development branch: `git checkout dev` (or `dev/feature-name`).
3. Run existing tests to confirm a clean baseline before making modifications.

### Phase 2: Local Code Generation via Ollama
1. Format a concise prompt containing:
   - Specific task objective.
   - Interface signature / contract from `DESIGN.md`.
   - Existing file contents or stub.
2. Dispatch prompt to the local model via the bridge:
   ```bash
   python .agents/skills/swe-local-bridge/scripts/ollama_bridge.py generate \
     --prompt "path/to/task_prompt.txt" \
     --model "qwen2.5-coder:14b"
   ```
3. Apply the generated code to the target source files.

### Phase 3: Unit Testing & Self-Check
1. Write or update unit tests covering:
   - Happy path behaviors.
   - Expected error conditions and exception handling.
2. Run the test suite locally:
   ```bash
   pytest tests/unit/
   ```
3. Inspect `git diff` to ensure no accidental edits, leftover debug print statements, or comment noise were introduced.

### Phase 4: Compiling the Handoff Package (`HANDOFF.md`)
Create [`HANDOFF.md`](../swe-orchestrator/references/templates/HANDOFF_TEMPLATE.md):
- List files added, modified, or removed.
- Include the git diff summary.
- Record the exact terminal command run and passing console output.
- Note any assumptions or suggestions for the QA engineer.
- Notify [`swe-orchestrator`](../swe-orchestrator/SKILL.md) that Gate G3 is complete.
