---
description: Morning routine — review OmniFocus and flag 3-5 tasks for today
---

# Morning Routine (5 min)

Load the `morning-routine` skill and follow its instructions.

Here is the live OmniFocus data to work with:

## Forecast (due items & calendar)
!`of perspective view "Forecast" -c 2>/dev/null | jq -r '.[] | "- **\(.name)** (\(.project)) — due: \(.due // "none")\(.tags | length | if . > 0 then " [" + (.tags | join(", ")) + "]" else "" end)\(.flagged | if . then " ⚑" else "" end)"' 2>/dev/null || echo "No data available"`

## Ready Now (available tasks)
!`of perspective view "Ready Now" -c 2>/dev/null | jq -r '.[] | "- **\(.name)** (\(.project))\(.tags | length | if . > 0 then " [" + (.tags | join(", ")) + "]" else "" end)\(.estimatedMinutes | if . then " (~" + tostring + "min)" else "" end)\(.flagged | if . then " ⚑" else "" end)"' 2>/dev/null || echo "No data available"`

## Already Flagged
!`of task ls --flagged -c 2>/dev/null | jq -r '.[] | "- **\(.name)** (\(.project))\(.tags | length | if . > 0 then " [" + (.tags | join(", ")) + "]" else "" end)"' 2>/dev/null || echo "No flagged tasks"`

## Your Job

1. Present a clean **Morning Brief** — group overdue/due-today items with `!!` markers, then available tasks, deduplicating anything that appears in both
2. **Recommend 3-5 tasks** to flag, with brief reasoning (prefer overdue/urgent + at least one quick win)
3. Ask me to confirm or adjust, then flag the chosen tasks using `of task update <id> --flag`
4. Keep it fast — this is a 5-minute ritual, not a planning session
