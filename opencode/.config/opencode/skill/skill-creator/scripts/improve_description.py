#!/usr/bin/env python3
"""Improve a skill description based on eval results.

Takes eval results (from run_eval.py) and generates an improved description
by calling `opencode run` as a subprocess.

Adapted from the Claude Code version which uses `claude -p`.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from scripts.utils import parse_skill_md


def _call_opencode(prompt: str, model: str | None, timeout: int = 300) -> str:
    """Run `opencode run` with the prompt and return the text response."""
    cmd = ["opencode", "run"]
    if model:
        cmd.extend(["--model", model])

    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"opencode run exited {result.returncode}\nstderr: {result.stderr}"
        )
    return result.stdout


def improve_description(
    skill_name: str,
    skill_content: str,
    current_description: str,
    eval_results: dict,
    history: list[dict],
    model: str,
    log_dir: Path | None = None,
    iteration: int | None = None,
) -> str:
    failed_triggers = [
        r for r in eval_results["results"] if r["should_trigger"] and not r["pass"]
    ]
    false_triggers = [
        r for r in eval_results["results"] if not r["should_trigger"] and not r["pass"]
    ]

    train_score = (
        f"{eval_results['summary']['passed']}/{eval_results['summary']['total']}"
    )

    prompt = f"""You are optimizing a skill description for an opencode skill called "{skill_name}". A "skill" is a reusable instruction package with progressive disclosure -- there's a name and description that the model sees when deciding whether to use the skill, and then if it does use the skill, it reads the SKILL.md file which has more details and references to other resources.

The description appears in the model's "available_skills" list. When a user sends a query, the model decides whether to invoke the skill based solely on the name and description. Your goal is to write a description that triggers for relevant queries, and doesn't trigger for irrelevant ones.

Here's the current description:
<current_description>
"{current_description}"
</current_description>

Current scores (Train: {train_score}):
"""

    if failed_triggers:
        prompt += "FAILED TO TRIGGER (should have triggered but didn't):\n"
        for r in failed_triggers:
            prompt += (
                f'  - "{r["query"]}" (triggered {r["triggers"]}/{r["runs"]} times)\n'
            )
        prompt += "\n"

    if false_triggers:
        prompt += "FALSE TRIGGERS (triggered but shouldn't have):\n"
        for r in false_triggers:
            prompt += (
                f'  - "{r["query"]}" (triggered {r["triggers"]}/{r["runs"]} times)\n'
            )
        prompt += "\n"

    if history:
        prompt += "PREVIOUS ATTEMPTS (do NOT repeat these):\n\n"
        for h in history:
            train_s = f"{h.get('train_passed', h.get('passed', 0))}/{h.get('train_total', h.get('total', 0))}"
            prompt += f"<attempt train={train_s}>\n"
            prompt += f'Description: "{h["description"]}"\n'
            if "results" in h:
                prompt += "Results:\n"
                for r in h["results"]:
                    status = "PASS" if r["pass"] else "FAIL"
                    prompt += f'  [{status}] "{r["query"][:80]}" (triggered {r["triggers"]}/{r["runs"]})\n'
            prompt += "</attempt>\n\n"

    prompt += f"""Skill content (for context):
<skill_content>
{skill_content}
</skill_content>

Based on the failures, write a new and improved description. Generalize from the failures to broader categories of user intent. Don't produce an expanding list of specific queries. The description should be 100-200 words and under 1024 characters.

Tips:
- Use imperative form: "Use this skill for" not "this skill does"
- Focus on user intent, not implementation details
- Make it distinctive and immediately recognizable
- If failing repeatedly, try different sentence structures

Respond with only the new description text in <new_description> tags."""

    text = _call_opencode(prompt, model)

    match = re.search(r"<new_description>(.*?)</new_description>", text, re.DOTALL)
    description = (
        match.group(1).strip().strip('"') if match else text.strip().strip('"')
    )

    if len(description) > 1024:
        shorten_prompt = (
            f"{prompt}\n\n---\n\nA previous attempt produced this description "
            f"({len(description)} chars, over 1024 limit):\n\n"
            f'"{description}"\n\n'
            f"Rewrite it to be under 1024 characters. Respond in <new_description> tags."
        )
        shorten_text = _call_opencode(shorten_prompt, model)
        match = re.search(
            r"<new_description>(.*?)</new_description>", shorten_text, re.DOTALL
        )
        description = (
            match.group(1).strip().strip('"')
            if match
            else shorten_text.strip().strip('"')
        )

    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"improve_iter_{iteration or 'unknown'}.json"
        log_file.write_text(
            json.dumps(
                {
                    "iteration": iteration,
                    "parsed_description": description,
                    "char_count": len(description),
                },
                indent=2,
            )
        )

    return description


def main():
    parser = argparse.ArgumentParser(
        description="Improve a skill description based on eval results"
    )
    parser.add_argument(
        "--eval-results", required=True, help="Path to eval results JSON"
    )
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--history", default=None, help="Path to history JSON")
    parser.add_argument(
        "--model", required=True, help="Model for improvement (provider/model)"
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    eval_results = json.loads(Path(args.eval_results).read_text())
    history = []
    if args.history:
        history = json.loads(Path(args.history).read_text())

    name, _, content = parse_skill_md(skill_path)
    current_description = eval_results["description"]

    new_description = improve_description(
        skill_name=name,
        skill_content=content,
        current_description=current_description,
        eval_results=eval_results,
        history=history,
        model=args.model,
    )

    output = {
        "description": new_description,
        "history": history
        + [
            {
                "description": current_description,
                "passed": eval_results["summary"]["passed"],
                "failed": eval_results["summary"]["failed"],
                "total": eval_results["summary"]["total"],
                "results": eval_results["results"],
            }
        ],
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
