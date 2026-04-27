# OmniFocus CLI — Full Command Reference

## Global Options

```
of [options] [command]
  -c, --compact   Minified JSON output (single line)
  -V, --version   Print version
  -h, --help      Print help
```

---

## `of task` — Task Management

### `of task list|ls`

List incomplete tasks.

| Flag | Description |
|---|---|
| `-f, --flagged` | Show only flagged tasks |
| `-p, --project <name>` | Filter by project |
| `-t, --tag <name>` | Filter by tag |
| `-c, --completed` | Include completed tasks |

Output: JSON array of task objects.

### `of task create <name>`

Create a new task.

| Flag | Description |
|---|---|
| `-p, --project <name>` | Assign to project |
| `--note <text>` | Add a note |
| `-t, --tag <tags...>` | Add one or more tags |
| `-d, --due <date>` | Set due date |
| `-D, --defer <date>` | Set defer date |
| `-f, --flagged` | Flag the task |
| `-e, --estimate <minutes>` | Estimated time in minutes |

Tasks are created in the Inbox by default unless `--project` is specified.

### `of task update <idOrName>`

Update an existing task. Accepts either the task ID (opaque string) or task name.

| Flag | Description |
|---|---|
| `-n, --name <name>` | Rename the task |
| `--note <text>` | Replace the note |
| `-p, --project <name>` | Move to a different project |
| `-t, --tag <tags...>` | Replace tags (not additive) |
| `-d, --due <date>` | Set due date |
| `-D, --defer <date>` | Set defer date |
| `-f, --flag` | Flag the task |
| `-F, --unflag` | Remove flag |
| `-c, --complete` | Mark as completed |
| `-C, --incomplete` | Mark as incomplete |
| `-e, --estimate <minutes>` | Estimated time in minutes |

### `of task view <idOrName>`

View full task details.

### `of task delete|rm <idOrName>`

Delete a task.

### `of task stats`

Show aggregate task statistics.

---

## `of project` — Project Management

### `of project list|ls`

| Flag | Description |
|---|---|
| `-f, --folder <name>` | Filter by folder |
| `-s, --status <status>` | Filter by status: `active`, `on hold`, `dropped` |
| `-d, --dropped` | Include dropped projects |

Output: JSON array of project objects with `id`, `name`, `note`, `status`, `folder`,
`sequential`, `taskCount`, `remainingCount`, `tags`.

### `of project create <name>`

| Flag | Description |
|---|---|
| `-f, --folder <name>` | Assign to folder |
| `--note <text>` | Add a note |
| `-t, --tag <tags...>` | Add tags |
| `-s, --sequential` | Make sequential |
| `--status <status>` | Set initial status |

### `of project update <idOrName>`

| Flag | Description |
|---|---|
| `-n, --name <name>` | Rename |
| `--note <text>` | Replace note |
| `-f, --folder <name>` | Move to folder |
| `-t, --tag <tags...>` | Replace tags |
| `-s, --sequential` | Make sequential |
| `-p, --parallel` | Make parallel |
| `--status <status>` | Change status |

### `of project view <idOrName>`

View full project details.

### `of project delete|rm <idOrName>`

Delete a project.

### `of project stats`

Show aggregate project statistics.

---

## `of inbox` — Inbox Management

### `of inbox list|ls`

List all inbox tasks.

### `of inbox count`

Return the number of inbox items.

### `of inbox add <name>`

| Flag | Description |
|---|---|
| `--note <text>` | Add a note |
| `-t, --tag <tags...>` | Add tags |
| `-d, --due <date>` | Set due date |
| `-D, --defer <date>` | Set defer date |
| `-f, --flagged` | Flag the task |
| `-e, --estimate <minutes>` | Estimated time in minutes |

---

## `of search <query>`

Search tasks by name or note content. Returns JSON array of matching tasks.

---

## `of tag` — Tag Management

### `of tag list|ls`

| Flag | Description |
|---|---|
| `-u, --unused-days <days>` | Show tags unused for N days |
| `-s, --sort <field>` | Sort by: `name`, `usage`, `activity` |
| `-a, --active-only` | Count only incomplete tasks |

### `of tag create <name>`

Create a new tag.

### `of tag view <idOrName>`

View tag details and associated tasks.

### `of tag update <idOrName>`

Update tag properties.

### `of tag delete|rm <idOrName>`

Delete a tag.

### `of tag stats`

Show tag usage statistics.

---

## `of folder` — Folder Hierarchy

### `of folder list|ls`

List top-level folders with nested children.

### `of folder view <idOrName>`

View folder details and children.

---

## `of perspective` — Perspectives

### `of perspective list|ls`

List all saved perspectives.

### `of perspective view <name>`

View tasks filtered by a perspective.

---

## `of mcp`

Run OmniFocus MCP server (for AI tool integrations).
