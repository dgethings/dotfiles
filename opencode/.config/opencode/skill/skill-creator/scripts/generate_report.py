#!/usr/bin/env python3
"""Generate an HTML report from run_loop.py output.

Takes the JSON output from run_loop.py and generates a visual HTML report
showing each description attempt with check/x for each test case.
"""

import argparse
import html
import json
import sys
from pathlib import Path


def generate_html(data: dict, auto_refresh: bool = False, skill_name: str = "") -> str:
    history = data.get("history", [])
    title_prefix = html.escape(skill_name + " \u2014 ") if skill_name else ""

    train_queries: list[dict] = []
    test_queries: list[dict] = []
    if history:
        for r in history[0].get("train_results", history[0].get("results", [])):
            train_queries.append(
                {"query": r["query"], "should_trigger": r.get("should_trigger", True)}
            )
        if history[0].get("test_results"):
            for r in history[0].get("test_results", []):
                test_queries.append(
                    {
                        "query": r["query"],
                        "should_trigger": r.get("should_trigger", True),
                    }
                )

    refresh_tag = (
        '    <meta http-equiv="refresh" content="5">\n' if auto_refresh else ""
    )

    html_parts = [
        """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
"""
        + refresh_tag
        + """    <title>"""
        + title_prefix
        + """Skill Description Optimization</title>
    <style>
        body { font-family: Georgia, serif; max-width: 100%; margin: 0 auto; padding: 20px; background: #faf9f5; color: #141413; }
        h1 { font-family: sans-serif; }
        .summary { background: white; padding: 15px; border-radius: 6px; margin-bottom: 20px; border: 1px solid #e8e6dc; }
        .best { color: #788c5d; font-weight: bold; }
        table { border-collapse: collapse; background: white; border: 1px solid #e8e6dc; font-size: 12px; min-width: 100%; }
        th, td { padding: 8px; text-align: left; border: 1px solid #e8e6dc; }
        th { background: #141413; color: #faf9f5; font-weight: 500; }
        th.test-col { background: #6a9bcc; }
        td.description { font-family: monospace; font-size: 11px; word-wrap: break-word; max-width: 400px; }
        td.result { text-align: center; font-size: 16px; }
        td.test-result { background: #f0f6fc; }
        .pass { color: #788c5d; }
        .fail { color: #c44; }
        .rate { font-size: 9px; color: #b0aea5; display: block; }
        .best-row { background: #f5f8f2; }
    </style>
</head>
<body>
    <h1>"""
        + title_prefix
        + """Skill Description Optimization</h1>
"""
    ]

    best_test_score = data.get("best_test_score")
    html_parts.append(f"""
    <div class="summary">
        <p><strong>Original:</strong> {html.escape(data.get("original_description", "N/A"))}</p>
        <p class="best"><strong>Best:</strong> {html.escape(data.get("best_description", "N/A"))}</p>
        <p><strong>Best Score:</strong> {data.get("best_score", "N/A")}</p>
    </div>
""")

    html_parts.append(
        "<table><thead><tr><th>Iter</th><th>Train</th><th>Test</th><th>Description</th>"
    )

    for qinfo in train_queries:
        html_parts.append(f"<th>{html.escape(qinfo['query'])}</th>")
    for qinfo in test_queries:
        html_parts.append(f'<th class="test-col">{html.escape(qinfo["query"])}</th>')

    html_parts.append("</tr></thead><tbody>")

    if test_queries:
        best_iter = max(history, key=lambda h: h.get("test_passed") or 0).get(
            "iteration"
        )
    else:
        best_iter = max(
            history, key=lambda h: h.get("train_passed", h.get("passed", 0))
        ).get("iteration")

    for h in history:
        iteration = h.get("iteration", "?")
        train_passed = h.get("train_passed", h.get("passed", 0))
        train_total = h.get("train_total", h.get("total", 0))
        test_passed = h.get("test_passed")
        test_total = h.get("test_total")
        description = h.get("description", "")
        train_results = h.get("train_results", h.get("results", []))
        test_results = h.get("test_results", [])

        train_by_query = {r["query"]: r for r in train_results}
        test_by_query = {r["query"]: r for r in test_results} if test_results else {}

        row_class = "best-row" if iteration == best_iter else ""
        html_parts.append(
            f'<tr class="{row_class}"><td>{iteration}</td><td>{train_passed}/{train_total}</td><td>{test_passed or "-"}/{test_total or "-"}</td><td class="description">{html.escape(description)}</td>'
        )

        for qinfo in train_queries:
            r = train_by_query.get(qinfo["query"], {})
            icon = "\u2713" if r.get("pass") else "\u2717"
            css = "pass" if r.get("pass") else "fail"
            triggers = r.get("triggers", 0)
            runs = r.get("runs", 0)
            html_parts.append(
                f'<td class="result {css}">{icon}<span class="rate">{triggers}/{runs}</span></td>'
            )

        for qinfo in test_queries:
            r = test_by_query.get(qinfo["query"], {})
            icon = "\u2713" if r.get("pass") else "\u2717"
            css = "pass" if r.get("pass") else "fail"
            triggers = r.get("triggers", 0)
            runs = r.get("runs", 0)
            html_parts.append(
                f'<td class="result test-result {css}">{icon}<span class="rate">{triggers}/{runs}</span></td>'
            )

        html_parts.append("</tr>")

    html_parts.append("</tbody></table></body></html>")
    return "".join(html_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML report from run_loop output"
    )
    parser.add_argument(
        "input", help="Path to JSON output from run_loop.py (or - for stdin)"
    )
    parser.add_argument("-o", "--output", default=None, help="Output HTML file")
    parser.add_argument("--skill-name", default="", help="Skill name for report title")
    args = parser.parse_args()

    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text())

    html_output = generate_html(data, skill_name=args.skill_name)

    if args.output:
        Path(args.output).write_text(html_output)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(html_output)


if __name__ == "__main__":
    main()
