---
name: swe-local-bridge
description: >-
  Manage and interface with the local LLM runtime (Ollama running Qwen2.5-Coder:14b or 32b).
  Use this skill to verify local engine health, pull or check models, prune context for local VRAM limits,
  and dispatch code generation or refactoring tasks to the local model.
---

# SWE Local Bridge (Ollama & Local Coding Models)

This skill provides the operational interface between the orchestration layer and local code-generation models (specifically **Qwen2.5-Coder** via **Ollama**). Offloading 80%+ of code generation and syntax refinement to local hardware minimizes cloud API cost, prevents rate limiting, and protects sensitive code.

## Configuration Defaults

- **Default Endpoint**: `http://localhost:11434` (overridable via `OLLAMA_HOST`)
- **Default Models**: 
  - `qwen2.5-coder:14b` (Optimal balance of speed and 16GB+ VRAM fits)
  - `qwen2.5-coder:32b` (Frontier-tier coding accuracy for 24GB+ VRAM or quantized on 16GB)
  - `qwen2.5-coder:7b` (Ultra-low latency fallback)

## Helper Script

The bundled Python script [`ollama_bridge.py`](./scripts/ollama_bridge.py) handles connectivity checks, context pruning, and generation dispatch.

### 1. Health & Model Discovery

Run the health check command to verify Ollama status:

```bash
python .agents/skills/swe-local-bridge/scripts/ollama_bridge.py health
```

Example successful output:
```json
{
  "status": "online",
  "host": "http://localhost:11434",
  "models": ["qwen2.5-coder:14b", "qwen2.5-coder:32b"],
  "message": "Connected to Ollama. 2 model(s) available."
}
```

If offline:
1. Ensure Ollama service is running (`ollama serve` or desktop app running).
2. Pull the required model if not listed: `ollama pull qwen2.5-coder:14b`.
3. If running on a LAN/remote machine, export `OLLAMA_HOST=http://<ip>:11434`.

### 2. Dispatching Code Generation to Local Model

When the **Coder** role executes a task from `PLAN.md`:

```bash
python .agents/skills/swe-local-bridge/scripts/ollama_bridge.py generate \
  --prompt "path/to/task_prompt.txt" \
  --system "path/to/system_instructions.txt" \
  --model "qwen2.5-coder:14b"
```

## Context Window Pruning Protocols (Local LLM Best Practices)

Local models operate most reliably when the context window is tightly managed:

1. **Pass Signatures, Not Full Repos**: Pass interface definitions, type signatures, and data contracts rather than entire codebase files.
2. **Targeted Diffs**: Give the local model only the active file and directly imported helper signatures.
3. **Explicit Task Bounds**: Limit each prompt to a single task or function implementation per the `PLAN.md` specification.
4. **Structured Format**: Require markdown code blocks for source files and unified diffs for modifications.
