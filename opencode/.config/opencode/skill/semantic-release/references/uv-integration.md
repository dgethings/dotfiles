# uv Integration with PSR

PSR updates the version in `pyproject.toml`, which causes `uv.lock` to go out of sync. This reference covers the two main approaches to handle this.

## Approach 1: Build Command (Recommended)

Include the lock update in PSR's `build_command`. PSR provides the `$PACKAGE_NAME` environment variable.

### Standard project with build artifacts

```toml
[tool.semantic_release]
build_command = """
  uv lock --upgrade-package "$PACKAGE_NAME"
  git add uv.lock
  uv build
"""
```

### Project without build artifacts (GitHub Release only)

```toml
[tool.semantic_release]
build_command = """
  uv lock --upgrade-package "$PACKAGE_NAME"
  git add uv.lock
"""
```

### In the PSR GitHub Action (Docker environment)

The PSR GitHub Action runs in Docker and does not have `uv` installed by default. Include uv installation in the build command:

```toml
[project.optional-dependencies]
build = ["uv ~= 0.7"]

[tool.semantic_release]
build_command = """
  python -m pip install -e '.[build]'
  uv lock --upgrade-package "$PACKAGE_NAME"
  git add uv.lock
  uv build
"""
```

This way Dependabot/Renovate can keep the uv version pinned via optional-dependencies.

## Approach 2: Two-Pass (for advanced CI pipelines)

When the build happens in a separate CI job from the release:

```bash
# Pass 1: Stamp version only (no changelog, no commit, no tag)
semantic-release -v version --skip-build --no-commit --no-tag --no-changelog

# Update the lock file now that pyproject.toml has the new version
uv lock --upgrade-package <your-package-name>

# Stage the lock file so PSR includes it in the release commit
git add uv.lock

# Pass 2: Full release (PSR skips build since --skip-build is not set here)
semantic-release -v version
```

In this approach, you'd carry the `dist/` and `uv.lock` artifacts between jobs using `actions/upload-artifact` and `actions/download-artifact`.

## Key Points

- `uv lock --upgrade-package <name>` only updates that specific package in the lock file — it does NOT upgrade other dependencies. This is important because you don't want PSR to accidentally pick up new dependency versions at release time.
- The `$PACKAGE_NAME` env var is set by PSR to the value of `project.name` from `pyproject.toml`.
- Always `git add uv.lock` before the release commit so PSR includes it in the tagged commit.
- If using `uv sync` as part of development, the lock file will be auto-updated on the next `uv sync` after a release.
