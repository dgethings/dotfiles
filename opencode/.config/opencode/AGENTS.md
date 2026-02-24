# uv Rules

- Use `uv` for all Python package management tasks - it's an extremely fast Python package and project manager written in Rust
- `uv` can replace `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, and `virtualenv`
- For pip-compatible commands, prepend `uv` to the pip command (e.g., `uv pip install ruff`)
- For project management, use uv's first-class project interface (e.g., `uv add ruff`) which includes lockfiles and workspace support
- Use `uv` to: install Python dependencies, run scripts, manage virtual environments, build and publish packages, and install Python itself
- When fetching uv documentation, use explicit `index.md` paths for directories to get clean markdown (e.g., `https://docs.astral.sh/uv/concepts/projects/dependencies/index.md`)
