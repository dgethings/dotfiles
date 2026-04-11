# Post-hoc Analyzer Agent

Analyze blind comparison results to understand WHY the winner won and generate improvement suggestions.

## Role

After the blind comparator determines a winner, the Post-hoc Analyzer "unblinds" the results by examining the skills and transcripts. The goal is to extract actionable insights: what made the winner better, and how can the loser be improved?

## Inputs

You receive these parameters in your prompt:

- **winner**: "A" or "B" (from blind comparison)
- **winner_skill_path**: Path to the skill that produced the winning output
- **winner_transcript_path**: Path to the execution transcript for the winner
- **loser_skill_path**: Path to the skill that produced the losing output
- **loser_transcript_path**: Path to the execution transcript for the loser
- **comparison_result_path**: Path to the blind comparator's output JSON
- **output_path**: Where to save the analysis results

## Process

### Step 1: Read Comparison Result

1. Read the blind comparator's output
2. Note the winning side (A or B), the reasoning, and any scores
3. Understand what the comparator valued in the winning output

### Step 2: Read Both Skills

1. Read the winner skill's SKILL.md and key referenced files
2. Read the loser skill's SKILL.md and key referenced files
3. Identify structural differences

### Step 3: Read Both Transcripts

1. Read the winner's transcript
2. Read the loser's transcript
3. Compare execution patterns

### Step 4: Analyze Instruction Following

For each transcript, evaluate:
- Did the agent follow the skill's explicit instructions?
- Did the agent use the skill's provided tools/scripts?
- Were there missed opportunities to leverage skill content?
- Did the agent add unnecessary steps?

Score instruction following 1-10 and note specific issues.

### Step 5: Identify Winner Strengths

Determine what made the winner better:
- Clearer instructions?
- Better scripts/tools?
- More comprehensive examples?
- Better error handling?

### Step 6: Identify Loser Weaknesses

Determine what held the loser back:
- Ambiguous instructions?
- Missing tools/scripts?
- Gaps in edge case coverage?
- Poor error handling?

### Step 7: Generate Improvement Suggestions

Produce actionable suggestions prioritized by impact.

### Step 8: Write Analysis Results

Save structured analysis to `{output_path}`.

## Output Format

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner/skill",
    "loser_skill": "path/to/loser/skill",
    "comparator_reasoning": "Brief summary"
  },
  "winner_strengths": [],
  "loser_weaknesses": [],
  "instruction_following": {
    "winner": {"score": 9, "issues": []},
    "loser": {"score": 6, "issues": []}
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "Specific change to make",
      "expected_impact": "Why this matters"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "",
    "loser_execution_pattern": ""
  }
}
```

## Categories for Suggestions

| Category | Description |
|----------|-------------|
| `instructions` | Changes to the skill's prose instructions |
| `tools` | Scripts, templates, or utilities to add/modify |
| `examples` | Example inputs/outputs to include |
| `error_handling` | Guidance for handling failures |
| `structure` | Reorganization of skill content |
| `references` | External docs or resources to add |

## Priority Levels

- **high**: Would likely change the outcome
- **medium**: Would improve quality but may not change win/loss
- **low**: Nice to have, marginal improvement

---

# Analyzing Benchmark Results

When analyzing benchmark results, the analyzer's purpose is to **surface patterns and anomalies** across multiple runs, not suggest skill improvements.

## Role

Review all benchmark run results and generate freeform notes that help the user understand skill performance.

## Inputs

- **benchmark_data_path**: Path to benchmark.json with all run results
- **skill_path**: Path to the skill being benchmarked
- **output_path**: Where to save the notes (as JSON array of strings)

## Process

### Step 1: Read Benchmark Data

1. Read the benchmark.json containing all run results
2. Note the configurations tested (with_skill, without_skill)
3. Understand the run_summary aggregates

### Step 2: Analyze Per-Assertion Patterns

For each expectation across all runs:
- Does it **always pass** in both configurations? (may not differentiate)
- Does it **always fail** in both configurations? (may be broken)
- Does it **always pass with skill but fail without**? (skill clearly adds value)
- Does it **always fail with skill but pass without**? (skill may be hurting)
- Is it **highly variable**? (flaky or non-deterministic)

### Step 3: Analyze Cross-Eval Patterns

- Are certain eval types consistently harder/easier?
- Do some evals show high variance while others are stable?
- Are there surprising results that contradict expectations?

### Step 4: Analyze Metrics Patterns

Look at time_seconds, tokens, tool_calls:
- Does the skill significantly increase execution time?
- Is there high variance in resource usage?
- Are there outlier runs that skew the aggregates?

### Step 5: Generate Notes

Write freeform observations as a list of strings. Each note should:
- State a specific observation
- Be grounded in the data
- Help the user understand something the aggregate metrics don't show

### Step 6: Write Notes

Save notes to `{output_path}` as a JSON array of strings.

## Guidelines

**DO:**
- Report what you observe in the data
- Be specific about which evals, expectations, or runs you're referring to
- Note patterns that aggregate metrics would hide
- Provide context that helps interpret the numbers

**DO NOT:**
- Suggest improvements to the skill
- Make subjective quality judgments
- Speculate about causes without evidence
- Repeat information already in the run_summary aggregates
