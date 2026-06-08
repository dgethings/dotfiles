---
description: Evening routine — wrap up the day in OmniFocus (2 min)
---

# Evening Routine (2 min)

Load the `morning-routine` skill for OmniFocus CLI context. Then follow the three steps below.

Here is the live OmniFocus data:

## Today's Flagged Tasks
!`of task ls --flagged -c 2>/dev/null | jq -r '.[] | "- **\(.name)** (\(.project))\(.completed | if . then " ✅" else " ❌ not done" end)\(.tags | length | if . > 0 then " [" + (.tags | join(", ")) + "]" else "" end)"' 2>/dev/null || echo "No flagged tasks"`

## Overdue
!`of perspective view "Forecast" -c 2>/dev/null | jq -r '[.[] | select(.due != null and (.due | split("T")[0]) < now | strftime("%Y-%m-%d"))] | if length == 0 then "Nothing overdue" else .[] | "- **\(.name)** (\(.project)) — was due \(.due | split("T")[0])" end' 2>/dev/null || echo "Could not load"`

## Due Tomorrow & Next Few Days
!`of perspective view "Forecast" -c 2>/dev/null | jq -r '[.[] | select(.due != null and (.due | split("T")[0]) <= ((now + (3*86400)) | strftime("%Y-%m-%d")))] | if length == 0 then "Nothing due soon" else .[] | "- **\(.name)** (\(.project)) — due \(.due | split("T")[0])\(.flagged | if . then " ⚑" else "" end)" end' 2>/dev/null || echo "Could not load"`

## Inbox
!`inbox=$(of inbox count 2>/dev/null); echo "Inbox has ${inbox:-?} items"'`

---

## Step 1: Check off completed tasks

Look at the flagged tasks above. Ask me:
> "Which of these did you finish today? Give me the numbers."

Then mark them complete with `of task update <id> --complete` (run in parallel).

## Step 2: Quick-capture loose thoughts

Ask me:
> "Anything on your mind to capture? Loose thoughts, follow-ups, ideas? One per line, or just free-form."

Then create each item with `of inbox add "<thought>"` (run in parallel). If I say "no" or "done", skip this step.

## Step 3: Flag anything urgent for tomorrow

Look at the overdue and due-soon items above. If anything is not yet flagged and looks urgent, recommend it:
> "Heads up — these look urgent for tomorrow:" + list

Ask me to confirm, then flag with `of task update <id> --flag`.

## Rules

- Keep it to 2 minutes — fast back-and-forth, no deep analysis
- If all flagged tasks are completed, say so — that's a win
- Don't over-prompt — if a step has nothing to do, skip it and move on
- Always use task IDs for updates, not names
- End with a brief wrap-up: "All set. See you tomorrow."
