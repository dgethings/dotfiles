---
description: Run a task inside a fresh wt-managed worktree via the worktree-worker subagent
---
Run this task inside a dedicated worktree using the `wt` command and the worktree-worker subagent: $@

Steps:

1. If the repo tracks work in beads (CLAUDE.md mentions `bd`), check `bd list --status open` for an issue matching this task; claim it (`bd update <id> --claim`) or create one (`bd create ...`) so the work is tracked.
2. Pick a branch name using the repo's conventional prefix (see AGENTS.md — e.g. `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`) plus a short slug for the task.
3. From the repo's main worktree, create the worktree: `wt switch --create <branch> -b main` (output gives the worktree path, typically a sibling directory named after the branch slug).
4. Dispatch the subagent tool ONCE, single mode: `agent: "worktree-worker"`, `task: "<the task above, plus any repo-specific context>"`, `cwd: "<the worktree path>"`. Let it run to completion — it handles deps, implementation, quality gates, commit, push, PR, CI, and merge per the repo's own workflow.
5. When the subagent reports back: `wt switch main`, then `git pull`. Verify the PR merged (or note why not).
6. Clean up: `wt remove <branch>` (use `--force` only if the worker left uncommitted scratch that is safe to discard — check first).
7. Close the beads issue if the worker did not (`bd close <id>`), referencing the PR number.

Report the outcome: PR URL, merge status, issue ID closed, and any follow-ups the worker flagged.
