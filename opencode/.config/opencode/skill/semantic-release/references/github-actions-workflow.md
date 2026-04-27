# GitHub Actions Workflow Templates

## Standard Single-Package Workflow (GitHub Release Only)

This is the default template. It creates a GitHub Release (tag + release page) when the version bumps. No PyPI publishing.

```yaml
name: Release

on:
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  release:
    runs-on: ubuntu-latest
    concurrency:
      group: ${{ github.workflow }}-release-${{ github.ref_name }}
      cancel-in-progress: false

    permissions:
      contents: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          ref: ${{ github.ref_name }}

      - name: Force branch to workflow SHA
        run: git reset --hard ${{ github.sha }}

      - name: Semantic Release
        id: release
        uses: python-semantic-release/python-semantic-release@v10
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          git_committer_name: "github-actions"
          git_committer_email: "actions@users.noreply.github.com"

      - name: Upload to GitHub Release Assets
        uses: python-semantic-release/publish-action@v10
        if: steps.release.outputs.released == 'true'
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          tag: ${{ steps.release.outputs.tag }}

    outputs:
      released: ${{ steps.release.outputs.released == 'true' }}
      version: ${{ steps.release.outputs.version }}
      tag: ${{ steps.release.outputs.tag }}
```

## Standard Single-Package + PyPI Publishing

Only use this when the user explicitly requests PyPI publishing.

```yaml
name: Release

on:
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  release:
    runs-on: ubuntu-latest
    concurrency:
      group: ${{ github.workflow }}-release-${{ github.ref_name }}
      cancel-in-progress: false

    permissions:
      contents: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          ref: ${{ github.ref_name }}

      - name: Force branch to workflow SHA
        run: git reset --hard ${{ github.sha }}

      - name: Semantic Release
        id: release
        uses: python-semantic-release/python-semantic-release@v10
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          git_committer_name: "github-actions"
          git_committer_email: "actions@users.noreply.github.com"

      - name: Upload to GitHub Release Assets
        uses: python-semantic-release/publish-action@v10
        if: steps.release.outputs.released == 'true'
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          tag: ${{ steps.release.outputs.tag }}

      - name: Save distribution artifacts
        uses: actions/upload-artifact@v4
        if: steps.release.outputs.released == 'true'
        with:
          name: distribution-artifacts
          path: dist
          if-no-files-found: error

    outputs:
      released: ${{ steps.release.outputs.released == 'true' }}
      version: ${{ steps.release.outputs.version }}
      tag: ${{ steps.release.outputs.tag }}

  publish-pypi:
    runs-on: ubuntu-latest
    needs: release
    if: needs.release.outputs.released == 'true'

    environment:
      name: pypi

    permissions:
      contents: read
      id-token: write

    steps:
      - name: Download distribution artifacts
        uses: actions/download-artifact@v4
        with:
          name: distribution-artifacts
          path: dist

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@v1
        with:
          packages-dir: dist
```

## Monorepo Workflow

For repos with multiple Python packages in subdirectories:

```yaml
name: Release

on:
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  release:
    runs-on: ubuntu-latest
    concurrency:
      group: ${{ github.workflow }}-release-${{ github.ref_name }}
      cancel-in-progress: false

    permissions:
      contents: write

    env:
      PACKAGE_A_DIR: packages/package-a
      PACKAGE_B_DIR: packages/package-b

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          ref: ${{ github.ref_name }}

      - name: Force branch to workflow SHA
        run: git reset --hard ${{ github.sha }}

      - name: Release package-a
        id: release-a
        uses: python-semantic-release/python-semantic-release@v10
        with:
          directory: ${{ env.PACKAGE_A_DIR }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          git_committer_name: "github-actions"
          git_committer_email: "actions@users.noreply.github.com"

      - name: Release package-b
        id: release-b
        uses: python-semantic-release/python-semantic-release@v10
        with:
          directory: ${{ env.PACKAGE_B_DIR }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          git_committer_name: "github-actions"
          git_committer_email: "actions@users.noreply.github.com"

      - name: Upload package-a to GitHub Release
        uses: python-semantic-release/publish-action@v10
        if: steps.release-a.outputs.released == 'true'
        with:
          directory: ${{ env.PACKAGE_A_DIR }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          tag: ${{ steps.release-a.outputs.tag }}

      - name: Upload package-b to GitHub Release
        uses: python-semantic-release/publish-action@v10
        if: steps.release-b.outputs.released == 'true'
        with:
          directory: ${{ env.PACKAGE_B_DIR }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          tag: ${{ steps.release-b.outputs.tag }}
```

## uv-Aware Workflow (Using PSR CLI directly)

When you need more control than the Docker-based GitHub Action provides (e.g., uv is already in the environment):

```yaml
name: Release

on:
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  release:
    runs-on: ubuntu-latest
    concurrency:
      group: ${{ github.workflow }}-release-${{ github.ref_name }}
      cancel-in-progress: false

    permissions:
      contents: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          ref: ${{ github.ref_name }}

      - name: Force branch to workflow SHA
        run: git reset --hard ${{ github.sha }}

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --extra build

      - name: Semantic Release
        id: release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: uv run semantic-release -v --strict version

      - name: Publish to GitHub Release
        if: steps.release.outputs.released == 'true'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: uv run semantic-release publish

    outputs:
      released: ${{ steps.release.outputs.released == 'true' }}
      version: ${{ steps.release.outputs.version }}
      tag: ${{ steps.release.outputs.tag }}
```

## Notes

- **Concurrency control** prevents race conditions when multiple pushes happen in quick succession.
- **Force reset** ensures the branch is at exactly the workflow SHA, preventing accidental release of un-evaluated commits.
- **PSR v10.5.0+** automatically handles shallow clone conversion. No need for `fetch-depth: 0`.
- **`GITHUB_TOKEN`** is automatically provided by GitHub Actions but has the same permissions as the triggering user. For protected branches, you may need a Personal Access Token stored as a separate secret.
- The `--strict` flag causes PSR to return a non-zero exit code on conditions that would otherwise silently pass, which is useful for CI.
