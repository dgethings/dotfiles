# PSR Setup Checklist

Use this checklist when setting up PSR in a project that has no existing `[tool.semantic_release]` config.

## Prerequisites

- [ ] Python project with `pyproject.toml`
- [ ] Git repository with at least one commit
- [ ] GitHub remote configured
- [ ] `uv` is installed

## Step 1: Install PSR

```bash
uv add --dev python-semantic-release
```

## Step 2: Generate Default Config

```bash
semantic-release generate-config --pyproject >> pyproject.toml
```

Then edit `pyproject.toml` and remove any keys you don't need to override.

## Step 3: Required Configuration Keys

Edit `[tool.semantic_release]` in `pyproject.toml`. Here are the keys that typically need setting:

### Version Source

Tell PSR where to stamp the version. For a standard `pyproject.toml` project:

```toml
[tool.semantic_release]
version_toml = ["pyproject.toml:project.version"]
```

For a monorepo subpackage:

```toml
[tool.semantic_release]
version_toml = ["packages/my-lib/pyproject.toml:project.version"]
```

For projects using poetry:

```toml
[tool.semantic_release]
version_toml = ["pyproject.toml:tool.poetry.version"]
```

### Commit Parser

Default to `conventional` (Conventional Commits). This means `feat:` bumps minor, `fix:` and `perf:` bump patch.

```toml
[tool.semantic_release]
commit_parser = "conventional"

[tool.semantic_release.commit_parser_options]
minor_tags = ["feat"]
patch_tags = ["fix", "perf"]
parse_squash_commits = true
ignore_merge_commits = true
```

### Changelog

Configure what commits appear in the changelog and where it's written:

```toml
[tool.semantic_release.changelog]
exclude_commit_patterns = [
    '''chore(?:\([^)]*?\))?: .+''',
    '''ci(?:\([^)]*?\))?: .+''',
    '''refactor(?:\([^)]*?\))?: .+''',
    '''style(?:\([^)]*?\))?: .+''',
    '''test(?:\([^)]*?\))?: .+''',
    '''build\((?!deps\): .+)''',
    '''Initial [Cc]ommit.*''',
]

[tool.semantic_release.changelog.default_templates]
changelog_file = "CHANGELOG.md"
output_format = "md"
```

### Build Command (uv projects)

See `references/uv-integration.md` for full details. Minimal version:

```toml
[tool.semantic_release]
build_command = """
  uv lock --upgrade-package "$PACKAGE_NAME"
  git add uv.lock
  uv build
"""
```

If the project does not need to build distribution artifacts (GitHub Release only):

```toml
[tool.semantic_release]
build_command = "uv lock --upgrade-package \"$PACKAGE_NAME\" && git add uv.lock"
```

Or if no lock file handling is needed:

```toml
[tool.semantic_release]
build_command = "uv build"
```

### Remote VCS Configuration

```toml
[tool.semantic_release]
remote = "github"
remote.type = "github"
```

### Project Version

Set the initial version in `pyproject.toml`:

```toml
[project]
name = "my-package"
version = "0.0.0"  # or the last released version for existing projects
```

Important: No `v` prefix. Must be valid SemVer (`MAJOR.MINOR.PATCH`).

### Release Branches (Optional)

Only needed if you use pre-release branches. Default configuration handles `main`/`master` fine.

```toml
[tool.semantic_release.branches.alpha]
match = "^(feat|fix|perf)/.+"
prerelease = true
prerelease_token = "alpha"
```

## Step 4: Test the Configuration

```bash
# Preview — what would happen (no side effects)
semantic-release -v --noop version

# If the preview looks good, try stamping without committing
semantic-release -v version --no-commit --no-tag

# Check what changed
git diff
```

## Step 5: Commit the Configuration

```bash
git add pyproject.toml uv.lock
git commit -m "chore(config): configure Python Semantic Release"
```

## Optional: PyPI Publishing

Only configure this if the user explicitly asks for PyPI publishing.

```toml
[tool.semantic_release]
build_command = """
  uv lock --upgrade-package "$PACKAGE_NAME"
  git add uv.lock
  uv build
"""
```

And add a publish step in the GitHub Actions workflow (see `references/github-actions-workflow.md`).

Without explicit user request, do NOT add any `publish` configuration or PyPI-related workflow steps. PSR's default behavior (GitHub Release only) is sufficient.
