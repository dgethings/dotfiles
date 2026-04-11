---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. This skill should be used whenever a user mentions creating, editing, testing, evaluating, or optimizing opencode skills, even if they don't explicitly say "skill-creator".
license: Complete terms in LICENSE.txt
---

# Skill Creator

A skill for creating new opencode skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run opencode-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
- Rewrite the skill based on feedback
- Repeat until satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages.

## Communicating with the user

Pay attention to context cues to understand how to phrase your communication. The user may be a developer or someone less technical. Briefly explain terms if you're in doubt.

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture. If so, extract answers from the conversation history first.

1. What should this skill enable the model to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works?

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier (lowercase, hyphens, matches directory name)
- **description**: When to trigger, what it does. Include both what the skill does AND specific contexts for when to use it. Opencode models tend to "undertrigger" skills — make descriptions a little "pushy" to compensate.
- **the rest of the skill body**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading)

Keep SKILL.md under 500 lines. If approaching this limit, split content into reference files with clear pointers.

**Domain organization**: When a skill supports multiple variants, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

#### Writing Patterns

Prefer imperative form in instructions.

**Defining output formats:**
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern:**
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing Style

Explain to the model *why* things are important instead of heavy-handed MUSTs. Use theory of mind and make the skill general. Start with a draft and then look at it with fresh eyes.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts. Share them with the user for approval. Then run them.

Save test cases to `evals/evals.json`:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": [],
      "expectations": ["The output includes X", "The skill used script Y"]
    }
  ]
}
```

See `references/schemas.md` for the full schema.

## Running and evaluating test cases

This section is one continuous sequence — don't stop partway through.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.). Don't create all of this upfront — create directories as you go.

### Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two opencode subagents using the Task tool in the same turn — one with the skill, one without. Launch everything at once so it all finishes around the same time.

**With-skill run** — use the `general` subagent:

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about>
```

The subagent should read the SKILL.md first, then follow its instructions to complete the task.

**Baseline run** (same prompt, no skill):
- **Creating a new skill**: no skill at all. Same prompt, save to `without_skill/outputs/`.
- **Improving an existing skill**: snapshot the skill first (`cp -r <skill-path> <workspace>/skill-snapshot/`), then point the baseline subagent at the snapshot. Save to `old_skill/outputs/`.

Write an `eval_metadata.json` for each test case (assertions can be empty for now). Give each eval a descriptive name. Use this name for the directory too.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: While runs are in progress, draft assertions

Don't just wait — draft quantitative assertions for each test case and explain them to the user. Good assertions are objectively verifiable with descriptive names. Update `eval_metadata.json` and `evals/evals.json` with the assertions.

### Step 3: As runs complete, capture timing data

If available, note the duration and token counts from subagent completions. Save to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

### Step 4: Grade, aggregate, and launch the viewer

Once all runs are done:

1. **Grade each run** — spawn a `general` subagent that reads `references/grader.md` and evaluates each assertion against the outputs. Save results to `grading.json`. The grading.json expectations array must use `text`, `passed`, and `evidence` fields.

2. **Aggregate into benchmark** — run:
   ```bash
   python <skill-creator-path>/scripts/aggregate_benchmark.py <workspace>/iteration-N --skill-name <name>
   ```
   This produces `benchmark.json` and `benchmark.md`.

3. **Do an analyst pass** — read the benchmark data and surface patterns. See `references/analyzer.md` for what to look for.

4. **Launch the viewer** — prefer `--static` mode:
   ```bash
   python <skill-creator-path>/scripts/generate_review.py <workspace>/iteration-N --static /tmp/eval_review_<name>.html --skill-name "my-skill" --benchmark <workspace>/iteration-N/benchmark.json
   ```
   Then open the file for the user: `open /tmp/eval_review_<name>.html`

   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

5. **Tell the user**: "I've opened the results in your browser. There are two tabs — 'Outputs' for qualitative review, 'Benchmark' for quantitative comparison. When you're done, let me know."

### Step 5: Read the feedback

When the user says they're done, read `feedback.json` from the workspace. Empty feedback means it looked fine. Focus improvements on cases with specific complaints.

---

## Improving the skill

### How to think about improvements

1. **Generalize from the feedback.** Don't put in fiddly overfitty changes. Try different metaphors and patterns.
2. **Keep the prompt lean.** Remove things that aren't pulling their weight.
3. **Explain the why.** Today's LLMs are smart — explain the reasoning so the model understands why something matters.
4. **Look for repeated work across test cases.** If all 3 test cases resulted in similar helper scripts, bundle that script into `scripts/`.

Take your time and really mull things over. Write a draft revision and then look at it anew.

### The iteration loop

After improving the skill:

1. Apply improvements
2. Rerun all test cases into `iteration-<N+1>/`
3. Launch the reviewer with `--previous-workspace`
4. Wait for user review
5. Read feedback, improve, repeat

Keep going until the user is happy, feedback is all empty, or you're not making meaningful progress.

---

## Advanced: Blind comparison

For rigorous comparison between two versions, use the blind comparison system. Read `references/comparator.md` and `references/analyzer.md` for details. Spawn a `general` subagent as the comparator — give it two outputs without telling it which is which.

This is optional and most users won't need it.

---

## Description Optimization

The description field in SKILL.md frontmatter is the primary mechanism that determines whether the model invokes a skill. After creating or improving a skill, offer to optimize the description.

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "a realistic user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Make queries realistic with file paths, personal context, detail. Focus on edge cases. For should-not-trigger, use near-misses — queries that share keywords but need something different.

### Step 2: Review with user

Present the eval set to the user using the HTML template:

1. Read the template from `assets/eval_review.html`
2. Replace `__EVAL_DATA_PLACEHOLDER__` with the JSON array
3. Replace `__SKILL_NAME_PLACEHOLDER__` and `__SKILL_DESCRIPTION_PLACEHOLDER__`
4. Write to `/tmp/eval_review_<skill-name>.html` and open it
5. The user edits and exports to `~/Downloads/eval_set.json`

### Step 3: Run the optimization loop

Save the eval set and run:

```bash
python <skill-creator-path>/scripts/run_loop.py \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id> \
  --max-iterations 5 \
  --verbose
```

Use the model ID from your session (in provider/model format). The script uses `opencode run --format json` for trigger testing.

While it runs, periodically tail the output for updates.

The script handles the full loop: splits into 60/40 train/test, evaluates the current description (3 runs per query), calls `opencode run` to propose improvements, re-evaluates, and iterates up to 5 times. Returns JSON with `best_description`.

### Step 4: Apply the result

Take `best_description` from the JSON output and update the skill's SKILL.md frontmatter. Show before/after.

---

## Reference files

The references/ directory contains instructions for specialized subagents:

- `references/grader.md` — How to evaluate assertions against outputs
- `references/comparator.md` — How to do blind A/B comparison
- `references/analyzer.md` — How to analyze benchmark results
- `references/schemas.md` — JSON schemas for evals, grading, benchmark
- `references/workflows.md` — Sequential and conditional workflow patterns
- `references/output-patterns.md` — Template and example patterns

## Scripts

- `scripts/init_skill.py` — Create a new skill from template
- `scripts/package_skill.py` — Package a skill into a .skill file
- `scripts/quick_validate.py` — Validate skill structure
- `scripts/generate_review.py` — Generate eval viewer (HTML)
- `scripts/aggregate_benchmark.py` — Aggregate grading into benchmark stats
- `scripts/run_eval.py` — Test description triggering via `opencode run`
- `scripts/improve_description.py` — Improve descriptions via `opencode run`
- `scripts/run_loop.py` — Full eval + improve loop
- `scripts/generate_report.py` — HTML report for description optimization
- `scripts/utils.py` — Shared utilities (SKILL.md parsing)

---

Repeating the core loop for emphasis:

- Figure out what the skill is about
- Draft or edit the skill
- Run opencode-with-access-to-the-skill on test prompts (use `general` subagent)
- With the user, evaluate the outputs:
  - Generate eval viewer with `scripts/generate_review.py --static`
  - Run quantitative evals with `scripts/aggregate_benchmark.py`
- Repeat until satisfied

Good luck!
