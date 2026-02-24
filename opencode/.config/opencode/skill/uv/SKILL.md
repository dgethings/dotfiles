---
name: uv
description: "Fast Python package and project manager. Use this skill when working with Python repositories to manage dependencies, Python versions, run scripts, or execute tools. Use when: adding/removing packages with uv add/remove, setting/updating Python versions with uv python, executing scripts with uv run, running Python tools with uvx or uv tool, or any project-level Python environment management tasks."
license: MIT
---

# uv

uv is an extremely fast Python package and project manager written in Rust. It can replace pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more.

## Core Concepts

uv works with projects that have a `pyproject.toml` file. The virtual environment is at `.venv` and automatically synced with project dependencies.

## Managing Dependencies

### Add dependencies

Add packages to the project:

```bash
uv add <package-name>
```

Add with specific version constraint:

```bash
uv add "package>=1.0.0,<2.0.0"
```

Add development dependency:

```bash
uv add --dev <package-name>
```

Add to specific dependency group:

```bash
uv add --group <group-name> <package-name>
```

Add optional dependency (extra):

```bash
uv add --optional <extra-name> <package-name>
```

Add from alternative source:

```bash
uv add git+https://github.com/user/repo
uv add ./local/path
uv add "package @ git+https://github.com/user/repo@tag"
```

Add from specific index:

```bash
uv add torch --index custom-index=https://example.com/simple
```

### Remove dependencies

Remove package from project:

```bash
uv remove <package-name>
```

Remove from specific group:

```bash
uv remove --dev <package-name>
uv remove --group <group-name> <package-name>
uv remove --optional <extra-name> <package-name>
```

### Update dependencies

Update package to latest compatible version:

```bash
uv add <package-name> --upgrade-package <package-name>
```

## Python Version Management

### Install Python

Install latest Python:

```bash
uv python install
```

Install specific version:

```bash
uv python install 3.12
uv python install 3.11 3.12
uv python install pypy@3.10
```

List available versions:

```bash
uv python list
```

Upgrade Python version:

```bash
uv python upgrade 3.12
uv python upgrade
```

### Request Python version

Request specific Python version for commands:

```bash
uv run --python 3.12 python script.py
uvx --python 3.10 ruff
uv tool install --python 3.11 mypy
```

## Running Commands in Projects

### Run commands in project environment

Run commands with project dependencies available:

```bash
uv run python -c "import mypackage"
uv run pytest
uv run my-script.sh
```

Run with additional dependencies for that invocation only:

```bash
uv run --with httpx==0.26.0 python -c "import httpx"
uv run --with "pytest<8" pytest
```

Run scripts with inline script metadata:

Scripts with `# /// script` blocks run in isolated environments:

```python
# /// script
# dependencies = ["httpx"]
# ///
import httpx
```

Execute with: `uv run script.py`

## Running Tools

### Run tools without installing (uvx)

Run a tool in temporary environment:

```bash
uvx ruff check .
uvx pycowsay "hello"
uvx mkdocs build
```

Run specific version:

```bash
uvx ruff@0.3.0 check
uvx ruff@latest check
```

Run with extras:

```bash
uvx --from 'mypy[faster-cache,reports]' mypy
```

Run with additional dependencies:

```bash
uvx --with mkdocs-material mkdocs build
```

Run from different source:

```bash
uvx --from git+https://github.com/user/repo toolname
uvx --from 'package==1.0.0' command
```

Run with different Python version:

```bash
uvx --python 3.10 toolname
```

### Install tools persistently

Install tool to PATH:

```bash
uv tool install ruff
uv tool install 'httpie>=1.0.0'
uv tool install git+https://github.com/user/repo
```

Install with extras:

```bash
uv tool install mkdocs --with mkdocs-material
```

Upgrade tool:

```bash
uv tool upgrade ruff
uv tool upgrade --all
```

## Project Management

### Initialize project

Create new project:

```bash
uv init
uv init my-project
```

Create virtual environment:

```bash
uv venv
```

Sync dependencies to environment:

```bash
uv sync
```

## Key Differences from pip

- Use `uv add` instead of `pip install`
- Use `uv remove` instead of `pip uninstall`
- Dependencies managed in `pyproject.toml`, not requirements.txt
- Automatic lockfile generation
- Supports workspace and dependency groups
- Faster than pip by default

## When to use which command

| Task | Command |
|------|---------|
| Add dependency to project | `uv add` |
| Remove dependency | `uv remove` |
| Run in project environment | `uv run` |
| Run tool temporarily | `uvx` or `uv tool run` |
| Install tool persistently | `uv tool install` |
| Install Python | `uv python install` |
| Create virtual environment | `uv venv` |
| Sync dependencies | `uv sync` |

## Important Notes

- uv automatically downloads Python versions when needed
- Use `uv run` when tool needs project installed (pytest, mypy)
- Use `uvx` when tool doesn't need project (ruff, black)
- Tools installed with `uv tool install` are isolated from project dependencies
- Default Python version is auto-detected; use `--python` to specify
- `uv add` creates/updates `pyproject.toml` automatically
- Lockfile is at `uv.lock` - commit this to version control
