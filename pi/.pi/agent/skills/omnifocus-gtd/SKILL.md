---
name: omnifocus-gtd
description: Manages OmniFocus using David Allen's Getting Things Done methodology (Capture, Clarify, Reflect, Engage). Use for task management, inbox processing, project organization, and weekly reviews.
---

# OmniFocus GTD

This skill implements David Allen's Getting Things Done (GTD) methodology using the `of` CLI command for OmniFocus on macOS.

## Setup

Ensure `of` CLI is installed:
```bash
# Check installation
of --version
```

Verify OmniFocus is running and synced.

## GTD Overview

This skill guides through the four GTD phases:
1. **Capture** - Quickly capture anything that has your attention
2. **Clarify** - Process what each item means and what to do about it
3. **Reflect** - Review and update your system regularly
4. **Engage** - Do the work based on context, time, and energy

---

## 1. CAPTURE

Quickly capture anything without processing yet.

### Add to Inbox
```bash
of inbox add "Call Sarah about project"
of inbox add "Buy groceries" --note "Milk, eggs, bread"
```

### Batch Capture
When capturing multiple items, create them all rapidly:
```bash
of inbox add "Email client about proposal"
of inbox add "Review Q3 financials"
of inbox add "Schedule dentist appointment"
```

### Capture with Quick Context (Optional)
If the context is immediately obvious:
```bash
of inbox add "Fix bug #123" --tag "@computer"
```

**Goal:** Get everything out of your head and into the inbox. Don't organize yet.

---

## 2. CLARIFY

Process inbox items to determine next actions.

### View Inbox
```bash
of inbox list
```

### Process Each Item
For each inbox item, ask: **Is it actionable?**

**If NOT actionable:**
- Is it trash? Delete it: `of task delete <idOrName>`
- Is it reference? Add note and file in project or Someday/Maybe
- Is it someday? Move to Someday/Maybe list

**If IS actionable:**
- Will it take less than 2 minutes? **Do it now**
- Can you delegate it? Assign to others via task note
- Does it belong to an existing project? Move it there: `of task update <idOrName> --project "<ProjectName>"`
- Is it a new project? Create project and task

### Create Tasks with Full Details
```bash
# Create with project and tags
of task create "Prepare presentation" \
  --project "Client Meeting" \
  --tag "@computer,@work" \
  --note "Include Q3 metrics, 10 slides max, email to team by Friday"
```

### Create Projects
```bash
# Create single-action list project
of project create "Buy House" --status active

# Create sequential project (tasks in order)
of project create "Launch Product" --mode sequential

# Create parallel project (tasks independent)
of project create "Home Repairs" --mode parallel
```

### Organize by Context (Tags)
```bash
# View available tags
of tag list

# Create context tags
of tag create "@computer"
of tag create "@phone"
of tag create "@home"
of tag create "@office"
of tag create "@errands"

# Tag tasks appropriately
of task update <idOrName> --tag "@computer,@low-energy"
```

### Set Defer and Due Dates
```bash
# Defer until specific date
of task update <idOrName> --defer "2024-07-01"

# Set due date
of task update <idOrName> --due "2024-07-15"

# Both
of task update <idOrName> --defer "2024-07-01" --due "2024-07-15"
```

**Goal:** Empty inbox by clarifying each item and assigning it to the right place.

---

## 3. REFLECT

Review and maintain your system.

### Weekly Review
Run this weekly (same day/time recommended):

```bash
# 1. Check inbox is empty
of inbox list

# 2. Review all projects
of project list --status active

# 3. Review upcoming tasks
of task list --due "7d"

# 4. Review Someday/Maybe list
of project list --status onhold

# 5. Review waiting-for items
of task list --tag "waiting-for"
```

### View Task Statistics
```bash
of task stats
```
Shows breakdown by status, flagged, due date, etc.

### View Project Statistics
```bash
of project stats
```
Shows active, completed, on-hold projects.

### Check Tag Usage
```bash
of tag stats
```
Identify unused contexts or overloaded ones.

### Search for Specific Items
```bash
# Search by name
of search "presentation"

# Find tasks needing review
of task list --flagged
```

**Goal:** Keep system trusted and up-to-date. Weekly review takes 30-60 minutes.

---

## 4. ENGAGE

Take action based on context, time, and energy.

### View by Perspective
```bash
# List available perspectives
of perspective list

# View specific perspective
of perspective view "Today"
of perspective view "Forecast"
of perspective view "@computer"
```

### Filter by Context/Tag
```bash
# Show tasks for current context
of task list --tag "@computer"

# Multiple contexts
of task list --tag "@computer,@low-energy"
```

### View Available Now
```bash
# Tasks not deferred and not completed
of task list --status incomplete --defer "now"

# Due today/soon
of task list --due "today"
of task list --due "3d"
```

### View Flagged Tasks
```bash
of task list --flagged
```
Flag important items that must get done.

### Complete Tasks
```bash
of task update <idOrName> --complete
```

**Goal:** Choose tasks based on current context, available time, and energy level.

---

## Example Workflows

### Daily Capture Session
```bash
of inbox add "Respond to Alex's email"
of inbox add "Review pull request"
of inbox add "Call insurance company"
of inbox add "Read chapter 4 of book"
```

### Daily Clarify (5-10 minutes)
```bash
of inbox list
# Process each item:
# - Quick actions (< 2 min): do them
# - Delegate: add note and tag "waiting-for"
# - Project: assign to project with appropriate tags
# - Reference: add note or file
```

### Daily Engage (Morning)
```bash
# View Today perspective
of perspective view "Today"

# Or view current context tasks
of task list --tag "@computer" --defer "now"
```

### Weekly Review (30-60 min)
```bash
# 1. Clear inbox
of inbox list
# Process to zero

# 2. Review all projects
of project list --status active
# Update status, add next actions

# 3. Review calendar and due items
of task list --due "7d"
of task list --due "30d"

# 4. Review Someday/Maybe
of project list --status onhold
# Activate any that are now actionable

# 5. Create new projects from new ideas
# (Capture during review if new things come up)
```

---

## GTD Best Practices

1. **Capture everything** - Don't rely on memory
2. **Process to zero** - Empty inbox regularly
3. **One next action per project** - What's the physical next step?
4. **Use contexts wisely** - @computer, @phone, @home, @office, @errands
5. **Weekly review is sacred** - Trust your system by maintaining it
6. **Delegate clearly** - Note who, when, and what
7. **Someday/Maybe** - Future ideas that aren't actionable yet
8. **Reference material** - Don't clutter tasks with reference info

---

## Common OmniFocus Tags for GTD

Create these tags for GTD contexts:

**Location/Tool:**
- `@computer` - Need computer
- `@phone` - Phone calls
- `@home` - At home
- `@office` - At office
- `@errands` - Out and about

**Energy:**
- `@high-energy` - Requires focus
- `@low-energy` - Can do when tired

**Time:**
- `@quick` - Under 15 minutes
- `@long` - 1+ hour block needed

**Status:**
- `waiting-for` - Delegated, waiting on others
- `someday` - Not actionable now

Create them:
```bash
of tag create "@computer"
of tag create "@phone"
of tag create "@home"
of tag create "@office"
of tag create "@errands"
of tag create "@high-energy"
of tag create "@low-energy"
of tag create "@quick"
of tag create "@long"
of tag create "waiting-for"
of tag create "someday"
```