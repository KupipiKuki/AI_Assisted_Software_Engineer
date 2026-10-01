"""
Ollama Bridge for Local Coding LLM (Qwen2.5-Coder)
Handles connectivity, model querying, context pruning, and health verification
for local AI software engineering roles.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error

DEFAULT_OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("LOCAL_CODER_MODEL", "qwen2.5-coder:14b")


def check_health(host: str = DEFAULT_OLLAMA_HOST) -> dict:
    """Check if Ollama server is accessible and list installed models."""
    url = f"{host.rstrip('/')}/api/tags"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                models = [m.get("name") for m in data.get("models", [])]
                return {
                    "status": "online",
                    "host": host,
                    "models": models,
                    "message": f"Connected to Ollama. {len(models)} model(s) available."
                }
    except urllib.error.URLError as e:
        return {
            "status": "offline",
            "host": host,
            "models": [],
            "message": f"Cannot connect to Ollama at {host}: {e.reason}"
        }
    except Exception as e:
        return {
            "status": "error",
            "host": host,
            "models": [],
            "message": f"Unexpected error checking Ollama: {str(e)}"
        }


def generate_code(
    prompt: str,
    system_prompt: str = "",
    model: str = DEFAULT_MODEL,
    host: str = DEFAULT_OLLAMA_HOST,
    temperature: float = 0.2,
    max_tokens: int = 4096
) -> dict:
    """Send code generation request to local Ollama instance."""
    url = f"{host.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt or (
            "You are an expert software engineer and implementation specialist. "
            "Write clean, idiomatic, and robust code. Adhere strictly to the requested "
            "task scope, interface contracts, and unit test requirements. "
            "Do not introduce unneeded abstractions or modify unrelated code."
        ),
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }

    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            if resp.status == 200:
                res_data = json.loads(resp.read().decode("utf-8"))
                return {
                    "success": True,
                    "model": model,
                    "response": res_data.get("response", ""),
                    "total_duration": res_data.get("total_duration", 0),
                    "eval_count": res_data.get("eval_count", 0)
                }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "error": f"Ollama connection error at {host}: {e.reason}",
            "hint": "Ensure Ollama is running (`ollama serve`) and model is pulled (`ollama pull " + model + "`)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Generation error: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(description="Ollama Local Coding Bridge")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Health check command
    health_parser = subparsers.add_parser("health", help="Check Ollama status and models")
    health_parser.add_argument("--host", default=DEFAULT_OLLAMA_HOST, help="Ollama host URL")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate code using local model")
    gen_parser.add_argument("--prompt", required=True, help="Prompt text or file path")
    gen_parser.add_argument("--system", default="", help="Optional system prompt or file path")
    gen_parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name")
    gen_parser.add_argument("--host", default=DEFAULT_OLLAMA_HOST, help="Ollama host URL")
    gen_parser.add_argument("--temp", type=float, default=0.2, help="Sampling temperature")

    args = parser.parse_args()

    if args.command == "health":
        result = check_health(args.host)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] == "online" else 1)

    elif args.command == "generate":
        prompt_content = args.prompt
        if os.path.exists(args.prompt):
            with open(args.prompt, "r", encoding="utf-8") as f:
                prompt_content = f.read()

        system_content = args.system
        if args.system and os.path.exists(args.system):
            with open(args.system, "r", encoding="utf-8") as f:
                system_content = f.read()

        result = generate_code(
            prompt=prompt_content,
            system_prompt=system_content,
            model=args.model,
            host=args.host,
            temperature=args.temp
        )
        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("success") else 1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
