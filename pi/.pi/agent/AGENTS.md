# Git Worktrees

- When creating, opening, removing, or listing git worktrees, always prefer `herdr` (or `worktrunk` if installed) over raw `git worktree` commands.
- Before using herdr, check `HERDR_ENV=1`. If it passes, use `herdr worktree create/open/remove/list`.
- Use `--no-focus` unless the user asked to switch context.
- Always pass an explicit `--path` inside the repo's project root (e.g. `<repo-root>/<branch-name>`) so worktrees sit alongside existing checkouts like `main/`, NOT in herdr's default `~/.herdr/worktrees` location.
- Only fall back to plain `git worktree` if neither tool is available; say so explicitly when doing so.
