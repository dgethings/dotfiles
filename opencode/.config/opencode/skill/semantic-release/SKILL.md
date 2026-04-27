---
name: semantic-release
description: >
  Set up and run Python Semantic Release (PSR) in Python projects. Use when the user wants to
  configure semantic versioning, set up automated releases, configure PSR in pyproject.toml,
  create GitHub Actions CI workflows for PSR, run PSR locally for dry-run/testing, integrate PSR
  with uv-managed projects, or configure PSR for monorepo layouts. Triggers on mentions of
  semantic release, PSR, semantic versioning, version bumping, automated releases, changelog
  generation, or commit-based versioning.
---

# Python Semantic Release (PSR)

This skill helps configure and run [Python Semantic Release](https://python-semantic-release.readthedocs.io/en/latest/) — a tool that automatically determines the next SemVer version from commit messages, stamps it into your project, generates a changelog, and creates Git tags/releases.

**Package version:** 10.x (current latest)

## Core Principle: Detect Then Act

Before doing anything, inspect the project:

1. Check `pyproject.toml` for an existing `[tool.semantic_release]` section
2. Check for `.github/workflows/release.yml` or similar
3. Check `git remote -v` to confirm GitHub
4. Check for monorepo layout (multiple `pyproject.toml` files in subdirectories)

Use these facts to determine which mode the user needs.

## Modes

### Mode 1: Full Project Setup (no PSR config exists)

Follow the setup checklist in `references/setup-checklist.md`. The high-level flow:

1. **Install PSR** as a dev dependency via `uv add --dev python-semantic-release`
2. **Generate default config** with `semantic-release generate-config --pyproject` and append to `pyproject.toml`
3. **Edit `pyproject.toml`** to configure the required keys (see checklist). Key settings:
   - `version_toml` — where PSR should stamp the version
   - `commit_parser` — use `"conventional"` as the default (feat/fix/perf)
   - `build_command` — uv-aware command including `uv lock` sync (see `references/uv-integration.md`)
   - `remote.type = "github"` — since all projects are GitHub-only
   - `changelog.exclude_commit_patterns` — filter out chore/ci/refactor/style/test commits
4. **Set `project.version`** to `"0.0.0"` for new projects, or the last released version for existing ones
5. **Test** with `semantic-release -v --noop version`
6. **Commit** the config with a `chore:` message

**Important:** Never configure PyPI publishing unless the user explicitly asks. PSR's default behavior creates a GitHub Release (tag + GitHub Release page) which is sufficient for most use cases. Only add a `publish` configuration or PyPI deploy workflow step when the user specifically requests PyPI publishing.

### Mode 2: GitHub Actions CI Setup

Read `references/github-actions-workflow.md` for full templates. The key decisions:

**Standard single-package workflow:**
- Use `python-semantic-release/python-semantic-release@v10` action
- Concurrency control to prevent race conditions on rapid pushes
- Checkout with `ref: ${{ github.ref_name }}` and force reset to workflow SHA
- PSR automatically handles shallow clone conversion (v10.5.0+)
- No PyPI publish step unless user explicitly requests it
- `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` with permissions: `contents: write`

**Monorepo workflow:**
- Run the PSR action multiple times with `directory` input per submodule
- Each submodule gets its own `id` to track whether it was released
- Only upload assets for submodules where `released == 'true'`

**uv projects in CI:**
- PSR GitHub Action runs in Docker and does not have `uv` pre-installed
- Either include `uv` in `build_command` or use the two-pass approach (see `references/uv-integration.md`)

### Mode 3: Local Dry-Run / Testing

When the repo is dirty or the user wants to test PSR locally:

```bash
# Preview what would happen (no side effects)
semantic-release -v --noop version

# Verbose output for debugging commit parsing issues
semantic-release -vv --noop version

# Stamp version + changelog locally without committing/tagging
semantic-release -v version --no-commit --no-tag

# Print only the next version number
semantic-release version --print

# Print the last released version
semantic-release version --print-last-released
```

Explain the output clearly: what version would be cut, which commits triggered it, and why.

## Monorepo Detection

A monorepo has multiple Python packages in subdirectories, each with their own `pyproject.toml`. For each subpackage:

- Set `version_toml` to the relative path (e.g., `"packages/my-lib/pyproject.toml:project.version"`)
- In GitHub Actions, use the `directory` input per action step
- Each subpackage should have its own `[tool.semantic_release]` config, or use a shared config with `directory`-aware settings

## Key PSR CLI Reference

The `semantic-release` command has important argument ordering: top-level flags (`--noop`, `-v`) must come BEFORE the subcommand.

```bash
# Correct
semantic-release -v --noop version --print

# Wrong — will fail
semantic-release version --print --noop -v
```

Common subcommands:
- `version` — determine next version, stamp files, build, commit, tag, push, create release
- `publish` — upload distribution artifacts to a GitHub Release
- `changelog` — generate/update the changelog file
- `generate-config` — output default configuration to stdout

Useful `version` flags:
- `--print` / `--print-tag` — show next version without side effects
- `--print-last-released` / `--print-last-released-tag` — show last released version
- `--major` / `--minor` / `--patch` — force a specific bump level
- `--as-prerelease` — convert next version to prerelease
- `--no-commit` / `--no-tag` / `--no-changelog` / `--no-push` / `--no-vcs-release` — disable individual steps
- `--skip-build` — skip the build command
- `--strict` — fail on conditions that would otherwise silently pass

## Reference Files

- `references/setup-checklist.md` — Step-by-step setup checklist with all pyproject.toml keys
- `references/uv-integration.md` — uv-specific build_command patterns and lock file handling
- `references/github-actions-workflow.md` — Full workflow YAML templates (standard, monorepo, uv)
- `references/commit-parsers.md` — Quick reference for parser options (conventional, angular, emoji, scipy)
- `references/troubleshooting.md` — Common PSR errors and fixes
