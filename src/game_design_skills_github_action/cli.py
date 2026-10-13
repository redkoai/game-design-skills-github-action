"""Minimal runtime for Game Design Skills GitHub Action."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

MANIFEST = {
    "publish_gate": "must work in a fresh public test repo",
    "shape": "GitHub Action",
    "slug": "game-design-skills-github-action",
    "theme": "Domain-specific agent skill packs",
    "title": "Game Design Skills GitHub Action",
    "validation_query": "game design AI agent skills"
}
REQUIRED_FIELDS = ["name", "description", "tasks"]


def load_payload(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def analyze(payload: dict) -> dict:
    missing = [field for field in REQUIRED_FIELDS if not payload.get(field)]
    tasks = payload.get("tasks") if isinstance(payload.get("tasks"), list) else []
    checks = []
    checks.append({"name": "required_fields", "passed": not missing, "detail": ", ".join(missing) or "all present"})
    checks.append({"name": "has_tasks", "passed": len(tasks) > 0, "detail": f"{len(tasks)} task(s)"})
    checks.append({"name": "has_success_metric", "passed": bool(payload.get("success_metric")), "detail": payload.get("success_metric", "missing")})
    checks.append({"name": "has_limitations", "passed": bool(payload.get("limitations")), "detail": "present" if payload.get("limitations") else "missing"})
    passed = sum(1 for check in checks if check["passed"])
    return {
        "project": payload.get("name", MANIFEST["title"]),
        "candidate": MANIFEST,
        "score": round((passed / len(checks)) * 100, 1),
        "checks": checks,
        "ready": passed == len(checks),
    }


def render_markdown(result: dict) -> str:
    lines = [
        f"# {result['project']} Readiness Report",
        "",
        f"Score: {result['score']}/100",
        "",
        f"Ready: {'yes' if result['ready'] else 'no'}",
        "",
        "## Checks",
        "",
    ]
    for check in result["checks"]:
        marker = "PASS" if check["passed"] else "FAIL"
        lines.append(f"- {marker} {check['name']}: {check['detail']}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=MANIFEST["title"])
    parser.add_argument("--input", default="examples/sample_input.json")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args(argv)
    result = analyze(load_payload(args.input))
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
