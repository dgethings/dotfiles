# Troubleshooting PSR

## Common Errors

### "No release will be made"

This is not an error — it means PSR analyzed the commits since the last release and determined none of them warrant a version bump. Check:
- Are the commit messages using the configured commit parser format?
- Do they use recognized bump types (e.g., `feat:`, `fix:`)?
- Were the commits made after the last release tag?

### "The current repository is dirty"

PSR refuses to run on a dirty working tree by default. Options:
- Commit or stash your changes
- Use `--no-commit` to test without PSR making its own commit (but repo must still be clean for the initial state check)

### "InvalidSemVerError" or version parsing issues

PSR uses strict SemVer (`MAJOR.MINOR.PATCH`). It does NOT support PEP 440 canonical versions.
- Version must be `"1.0.0"` not `"1.0.0rc1"` or `"v1.0.0"`
- No `v` prefix in `project.version`

### uv.lock out of sync after release

After PSR stamps the new version, `uv.lock` becomes stale. Fix:
- Add `uv lock --upgrade-package "$PACKAGE_NAME"` and `git add uv.lock` to the `build_command`
- See `references/uv-integration.md` for full details

### Shallow clone in CI

PSR needs full git history to evaluate commits. As of v10.5.0, PSR automatically handles shallow clone conversion. For older versions, use `fetch-depth: 0` on `actions/checkout`.

### "upstream branch has changed"

PSR verifies the upstream hasn't changed before pushing. If you get this:
- Pull the latest changes and re-run
- This prevents push conflicts when another commit was made during the release process

### Permission denied on push

- Check that `GITHUB_TOKEN` has `contents: write` permission in the workflow
- For protected branches, `GITHUB_TOKEN` has the same permissions as the user who triggered the workflow. Use a PAT stored as a secret if needed.

### Build command fails in PSR GitHub Action

The PSR GitHub Action runs in Docker without `uv`. Options:
- Include uv installation in `build_command` (see `references/uv-integration.md`)
- Use the CLI directly instead of the Docker-based action (see `references/github-actions-workflow.md`)

### Wrong version calculated

- Run `semantic-release -vv --noop version` for verbose debug output
- Check which commits are being parsed with `git log <last-tag>..HEAD --oneline`
- Verify the commit parser configuration matches your commit message style

## Debug Commands

```bash
# Check what version PSR thinks is current
semantic-release version --print-last-released

# Check what the next version would be
semantic-release version --print

# Full verbose no-op run
semantic-release -vv --noop version

# Check git history since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline
```
