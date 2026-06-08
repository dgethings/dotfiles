---
description: Weekly Review — GTD weekly review following the 4-phase template
subtask: false
---

# Weekly Review

Load the `obsidian-cli` and `omnifocus-cli` skills for context.

## Current Date & Context

!`echo "Today is $(date '+%Y-%m-%d %A')"`

### Month-End Detection
!`python3 -c "
import datetime, sys
today = datetime.date.today()
days_left = (datetime.date(today.year, today.month + 1, 1) if today.month < 12 else datetime.date(today.year + 1, 1, 1)) - today
if days_left.days <= 7:
    print('MONTHLY_REVIEW=true — this is the last weekly review of the month')
else:
    print('MONTHLY_REVIEW=false — %d days remaining in month' % days_left.days)
"`

## OmniFocus Data

### Inbox Count
!`inbox=$(of inbox count 2>/dev/null); echo "OmniFocus Inbox: **${inbox:-?} items**"`

### Projects Due for Review
!`of project ls -c 2>/dev/null | jq -r '.[] | select(.status == "active") | "- **\(.name)** — \(.remainingCount) remaining"' 2>/dev/null || echo "Could not load projects"`

### Flagged Tasks
!`of task ls --flagged -c 2>/dev/null | jq -r '.[] | "- **\(.name)** (\(.project))"' 2>/dev/null || echo "No flagged tasks"`

### Forecast (Due This Week)
!`of perspective view "Forecast" -c 2>/dev/null | jq -r '.[] | "- **\(.name)** (\(.project)) — due: \(.due // "none")"' 2>/dev/null || echo "No data available"`

---

## Setup

Before starting, create the weekly review note from the template:

```bash
obsidian create path="Weekly Reviews/Weekly Review — $(date '+%Y-%m-%d')" template="Weekly Review"
```

Then read it back to confirm:

```bash
obsidian read path="Weekly Reviews/Weekly Review — $(date '+%Y-%m-%d').md"
```

Tell the user the note is ready and present a summary of their current OmniFocus state (inbox count, active projects, flagged tasks, forecast).

---

## Phase-by-Phase Guide

Walk the user through each phase **one at a time**. For each phase:

1. Present the phase title and its checklist items
2. Guide the user through each item with specific actions
3. As the user confirms completion of each checkbox, toggle it in the note using `obsidian task path="Weekly Reviews/Weekly Review — $(date '+%Y-%m-%d').md" line=<N> toggle`
4. Prompt the user to fill in the free-text sections (bolded prompts / HTML comments)
5. Once all items in a phase are done, move to the next phase

### Phase 1: Get Clear (~15 min)

Checklist items to work through:
- Process OmniFocus Inbox to zero — guide them to open `omnifocus:///inbox` and process each item. Show the current inbox count. As they process, re-check `of inbox count` to track progress.
- Process email inboxes to zero — ask them to confirm when done
- Move reference material to Obsidian — ask if there are emails, documents, or notes to file. Offer to create wiki pages for anything substantial.
- File downloads and receipts — ask them to confirm when done

After all checkboxes are toggled, prompt:
> "What inbox items did you process this week? Any notable clarifications or where things landed?"

Collect their response and append it to the **Inbox items processed this week** section.

### Phase 2: Get Current (~20 min)

Checklist items to work through:
- Review all projects due for review — present the active projects list above. For each, ask: "Does this have a clear next action?" If not, create one with `of inbox add "<next action>" --project "<Project Name>"`.
- Ensure every active project has a clear next action — use the project data to identify any with 0 remaining tasks that are still active.
- Check Waiting For items — ask: "Who are you waiting on? Any follow-ups needed?" Search with `of search "waiting"` if needed.
- Check Forecast for upcoming deadlines — present the forecast data above. Flag anything urgent.
- Remove flags from last week's unfinished tasks — list the currently flagged tasks. Ask which to unflag. Use `of task update <id> --unflag`.
- Review Someday/Maybe — ask if there's anything to activate or delete.

After checkboxes, prompt for the two free-text sections:
> "Quick notes on projects reviewed — completions, changes, new next actions?"
> "Any Waiting For follow-ups needed?"

Collect and append to the note.

### Phase 3: Reflect (~10 min)

Present the reflection prompts one at a time:

1. > "What worked this week? (3-5 things)"
2. > "What didn't work? Obstacles, missed tasks, friction?"
3. > "What are you avoiding? Tasks that keep getting deferred — why?"
4. > "Energy & Focus — rate 1-10. When was energy highest? Lowest?"
5. > "Any adjustments for next week based on this reflection?"

Collect each response and append it to the corresponding section in the note.

### Phase 4: Plan Next Week (~5 min)

Checklist items:
- Set 3 key priorities — ask:
  > "What are your 3 key priorities for next week?"
  Collect and fill in the numbered list.
- Flag the most important tasks in OmniFocus — recommend tasks to flag based on the forecast and project data. Ask for confirmation, then flag with `of task update <id> --flag`.
- Ensure next actions exist for all active projects — check for any active projects with 0 remaining tasks.

### Phase 5: Monthly Review (~10 min) — conditional

**Only present this phase if MONTHLY_REVIEW is true.** If false, skip directly to Completion.

Announce:
> "This is the last weekly review of the month — time for the monthly review steps."

First, gather the monthly OmniFocus data:

```bash
of project ls --dropped -c 2>/dev/null | jq -r '.[] | "- **\(.name)** (\(.status))"' 2>/dev/null || echo "No dropped projects"
of project ls -c --status "on hold" 2>/dev/null | jq -r '.[] | "- **\(.name)** — \(.remainingCount) remaining"' 2>/dev/null || echo "No on-hold projects"
of tag ls --unused-days 30 -c 2>/dev/null | jq -r '.[] | "- **\(.name)** — last used: \(.lastUsed // "never")"' 2>/dev/null || echo "Could not load tags"
```

Checklist items to work through:
- **Review Someday/Maybe folder** — show on-hold projects. For each, ask: "Activate, delete, or keep on hold?" Use `of project update <id> --status "active"` to activate or `of project delete <id>` to drop.
- **Review areas of responsibility (Horizon 2)** — prompt: "Think about your key areas of responsibility (health, finances, relationships, career, etc.). Which got attention this month? Which were neglected? Any need a new project or next action?" Collect the response.
- **Clean up completed/dropped projects** — show dropped projects. Ask: "Any of these should be permanently deleted?" Use `of project delete <id>` to remove.
- **Review tag usage** — show tags unused in 30+ days. Ask: "Any of these tags should be deleted or merged?" Use `of tag delete <id>` to remove.

After all monthly checkboxes are toggled, collect free-text responses for each section and append them to the note.

If the user says "skip" to Phase 5, toggle all checkboxes and append "(skipped)" to each section. Move on.

---

### Links

Remind the user they can open these OmniFocus views at any time:
- [Open OmniFocus Forecast](omnifocus:///forecast)
- [Open OmniFocus Flagged](omnifocus:///flagged)
- [Open OmniFocus Projects](omnifocus:///projects)

---

## Completion

Once all phases are done (4 or 5 depending on monthly review):

1. Update the note's `updated` property: `obsidian property:set path="Weekly Reviews/Weekly Review — $(date '+%Y-%m-%d').md" name="updated" value="$(date '+%Y-%m-%d')"`
2. Append to the daily note:
   ```bash
   obsidian daily:append content="### Wiki Activity
   - Completed: [[Weekly Reviews/Weekly Review — $(date '+%Y-%m-%d')]]"
   ```
3. Append to the activity log:
   ```bash
   obsidian append path="log.md" content="## [$(date '+%Y-%m-%d %H:%M')] review | Weekly Review completed"
   ```
4. Present a brief summary:
   > "Weekly Review complete. Note saved at `Weekly Reviews/Weekly Review — <date>`. Have a great week!"
   > If monthly review was done: "Monthly review also completed — Someday/Maybe, areas of responsibility, projects, and tags are cleaned up."

## Rules

- Go **one phase at a time** — don't dump all phases at once
- **Toggle checkboxes** in the Obsidian note as the user confirms completion
- Use task/project **IDs** (not names) for all OmniFocus updates
- Keep the pace moving — this should take 45-50 minutes total
- If the user wants to skip an item, toggle it anyway and note it was skipped
- For Phase 3, collect responses and write them into the note — don't just show them
- Be concise in your prompts — this is a workflow, not a conversation
