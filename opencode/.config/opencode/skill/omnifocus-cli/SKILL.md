---
name: omnifocus-cli
version: "1.0.0"
description: >
  Use this skill whenever the user wants Opencode to access, search, or manage their
  OmniFocus task management data — reading tasks, projects, inbox items, tags, folders,
  or perspectives; searching tasks; creating or updating tasks; checking what's due or
  flagged; getting an overview of their workload; or using OmniFocus as a research/data
  source. Also trigger when the user asks about their tasks, to-dos, projects, or
  productivity system and you need to look up real data rather than guess. The `of`
  CLI (OmniFocus CLI) is the only way to access this data — without this skill, Opencode
  has no way to read or modify OmniFocus. Skip for conceptual questions about GTD
  methodology, OmniFocus GUI usage, settings configuration, or plugin recommendations —
  anything where the user wants an explanation rather than Opencode performing a lookup
  or action.
triggers:
  - "omnifocus"
  - "of task"
  - "of project"
  - "my tasks"
  - "my to-dos"
  - "what's due"
  - "flagged tasks"
  - "inbox"
  - "add task"
  - "create task"
  - "complete task"
  - "my projects"
  - "search tasks"
  - "workload"
  - "to do"
  - "todo"
  - "task list"
  - "overdue"
  - "deferred"
  - "omnifocus cli"
---

# OmniFocus CLI (`of`)

A command-line interface for OmniFocus on macOS. Use it to query, create, update, and
manage tasks, projects, inbox items, tags, folders, and perspectives.

All output is JSON by default. The `-c` / `--compact` flag produces single-line JSON.

> Read `references/command-reference.md` for full parameter details on every subcommand.

## Prerequisites

| Requirement | Details |
|---|---|
| OmniFocus | Installed on macOS |
| `of` CLI | Available in PATH (`/Users/dgethings/.bun/bin/of`) |

## Command Overview

| Command | Key Subcommands | Purpose |
|---|---|---|
| **task** | `list`, `create`, `update`, `delete`, `view`, `stats` | Task CRUD and statistics |
| **project** | `list`, `create`, `update`, `delete`, `view`, `stats` | Project CRUD and statistics |
| **inbox** | `list`, `count`, `add` | Inbox management |
| **search** | `<query>` | Full-text search across tasks |
| **tag** | `list`, `create`, `view`, `update`, `delete`, `stats` | Tag management and analysis |
| **folder** | `list`, `view` | Folder hierarchy |
| **perspective** | `list`, `view` | Saved OmniFocus perspectives |

## Quick Reference

### Tasks

```bash
of task ls                         # List incomplete tasks
of task ls --flagged               # Flagged tasks only
of task ls --project "Project"     # Filter by project
of task ls --tag "Errands"         # Filter by tag
of task ls --completed             # Include completed tasks
of task view <idOrName>            # View full task details
of task create "Task name"         # Create in inbox
of task create "Task name" --project "P" --tag "t1" "t2" --due "2026-04-15" --note "details"
of task update <idOrName> --complete           # Mark complete
of task update <idOrName> --name "New name"    # Rename
of task update <idOrName> --project "Project"  # Move to project
of task stats                       # Task statistics overview
```

### Projects

```bash
of project ls                       # List active projects
of project ls --dropped             # Include dropped projects
of project ls --status on-hold      # Filter by status
of project ls --folder "Personal"   # Filter by folder
of project view <idOrName>          # View project details
of project create "New Project" --folder "F" --sequential
of project stats                    # Project statistics overview
```

### Inbox

```bash
of inbox ls                         # List inbox tasks
of inbox count                      # Count inbox items
of inbox add "Quick task" --note "details" --flagged
```

### Search

```bash
of search "meeting notes"           # Search tasks by name or note content
```

### Tags

```bash
of tag ls                           # List all tags
of tag ls --sort usage              # Sort by most used
of tag ls --unused-days 30          # Tags not used in 30 days
of tag ls --active-only             # Count only incomplete tasks
of tag view <idOrName>              # View tag and its tasks
of tag stats                        # Tag usage statistics
```

### Folders & Perspectives

```bash
of folder ls                        # Top-level folders with children
of folder view <idOrName>           # Folder details and children
of perspective ls                   # List all perspectives
of perspective view "Focus"         # View tasks in a perspective
```

## Common Research Patterns

### Get a workload overview

Start broad and drill down:

```bash
of task stats                       # Overall task statistics
of task ls --flagged                # What's important right now
of inbox ls                         # Uncaptured items
of project ls | jq '[.[] | select(.remainingCount > 0)]'  # Active projects with work left
```

### Find tasks related to a topic

```bash
of search "topic"
```

### Check what's actionable now

```bash
of task ls                          # All available tasks
of task ls --flagged                # High priority
of inbox ls                         # Unprocessed items
```

### Understand project context

```bash
of folder ls                        # See how projects are organized
of project ls --folder "Personal"   # Projects in a folder
of project view "Project Name"      # Full project details
```

### Analyze tag usage

```bash
of tag stats                        # Overview
of tag ls --sort usage              # Most-used tags
of tag ls --unused-days 90          # Candidates for cleanup
```

## Output Format

All commands return JSON arrays or objects. Task objects include fields like `id`, `name`,
`note`, `status`, `project`, `tags`, `dueDate`, `deferDate`, `flagged`, `completed`,
`estimate`. Project objects include `id`, `name`, `status`, `folder`, `taskCount`,
`remainingCount`, `tags`.

Use `jq` for filtering and transforming output:

```bash
of task ls | jq '[.[] | {name, project, dueDate}] | sort_by(.dueDate)'
of project ls | jq '[.[] | select(.remainingCount > 0) | .name]'
```

## Tips

1. **Use `jq` liberally** — output is JSON, so pipe through `jq` to extract relevant fields.
2. **Search is the fastest way** to find tasks related to a topic when you don't know the project or tag.
3. **`task ls` returns incomplete tasks by default** — pass `--completed` to include done tasks.
4. **IDs are opaque strings** like `"nbCPgvWhKvw"` — use them for precise updates, or match by name.
5. **`--tag` accepts multiple values** — `of task create "X" --tag "errand" "urgent"` adds both tags.
6. **Dates** — use `YYYY-MM-DD` format, or natural language if the CLI supports it.
