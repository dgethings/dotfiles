---
name: typer
description: "Python library for building elegant CLI applications with minimal code. Use when creating Python scripts that need to parse command-line arguments, options, or flags. Specifically use for: (1) Creating CLI tools with argument parsing, (2) Building command-line interfaces with multiple subcommands, (3) Adding help text and documentation to scripts, (4) Implementing prompts, progress bars, and colored output, (5) Building CLI apps with type safety using Python type hints"
---

# Typer

## Overview

Typer is a Python library for building CLI applications using type hints. It's built on Click but provides an intuitive, FastAPI-like developer experience.

## When to Use Typer

Use this skill when:
- Creating a Python script that needs to accept command-line arguments or options
- Building a CLI tool with multiple commands (like `git commit`, `git push`)
- Adding help text, prompts, or progress bars to a script
- Wanting type-safe argument parsing with Python type hints
- Need user-friendly error messages and validation

## Quick Start

### Installation

```bash
uv add typer
```

### Simple CLI

```python
import typer

def main(name: str, count: int = 1):
    """Say hello multiple times."""
    for _ in range(count):
        typer.echo(f"Hello {name}")

if __name__ == "__main__":
    typer.run(main)
```

Run:
```bash
$ python main.py Alice --count 3
Hello Alice
Hello Alice
Hello Alice
```

## Core Concepts

### CLI Arguments vs Options

- **CLI Arguments**: Required, order-dependent parameters (e.g., `script.py name age`)
- **CLI Options**: Optional parameters with `--` prefix (e.g., `script.py --name Alice`)

```python
# name is required argument, --count is optional option
def main(name: str, count: int = 1):
    pass
```

### Typer App

For multiple commands, use `typer.Typer()`:

```python
import typer

app = typer.Typer()

@app.command()
def create(name: str):
    """Create a user."""
    print(f"Creating user: {name}")

@app.command()
def delete(name: str):
    """Delete a user."""
    print(f"Deleting user: {name}")

if __name__ == "__main__":
    app()
```

## Parameter Types

Typer uses Python type hints for automatic validation and conversion:

```python
def process(
    name: str,              # String
    age: int,               # Integer
    height: float,           # Float
    active: bool = False,    # Boolean flag (--active/--no-active)
):
    pass
```

### Common Types

- `str`, `int`, `float` - Basic types
- `bool` - Creates `--flag/--no-flag` options
- `list[str]` - Multiple values
- `datetime` - Date/time parsing
- `enum.Enum` - Choice validation
- `pathlib.Path` - Path validation
- `typing.Optional[T]` - Optional values

See `references/parameter_types.md` for all supported types.

## Arguments and Options

### CLI Arguments (Required)

```python
def main(name: str, age: int):
    """Required arguments, order matters."""
    print(f"{name} is {age} years old")
```

Usage: `python main.py Alice 30`

### CLI Options (Optional)

```python
def main(
    name: str,
    age: int = typer.Option(20, help="Age in years"),
    verbose: bool = False,
):
    """Optional parameters with defaults."""
    pass
```

Usage: `python main.py Alice --age 30 --verbose`

### Adding Help

```python
def main(
    name: str = typer.Argument(..., help="User name"),
    count: int = typer.Option(1, help="Number of times"),
):
    pass
```

## Multiple Commands

Create CLI apps with subcommands (like git):

```python
import typer

app = typer.Typer()

@app.command()
def deploy(env: str = typer.Option("dev", help="Environment to deploy")):
    """Deploy application."""
    print(f"Deploying to {env}")

@app.command()
def rollback(version: str = typer.Argument(..., help="Version to rollback")):
    """Rollback to a specific version."""
    print(f"Rolling back to {version}")

if __name__ == "__main__":
    app()
```

Usage:
```bash
$ python main.py deploy --env prod
$ python main.py rollback v1.2.3
```

## SubCommands (Nested)

Organize commands into groups:

```python
app = typer.Typer()
users_app = typer.Typer()
app.add_typer(users_app, name="users", help="Manage users")

@users_app.command()
def create(name: str):
    print(f"Creating user: {name}")

@users_app.command()
def delete(name: str):
    print(f"Deleting user: {name}")
```

Usage:
```bash
$ python main.py users create Alice
$ python main.py users delete Alice
```

See `references/commands.md` for detailed command organization.

## Progress Bars

Use Rich for beautiful progress displays:

```python
import typer
from rich.progress import track

app = typer.Typer()

@app.command()
def process():
    """Process items with progress bar."""
    for item in track(range(100), description="Processing..."):
        # Your processing logic
        pass

if __name__ == "__main__":
    app()
```

See `references/progress.md` for more progress bar options.

## Prompts

Prompt users for input:

```python
def main(
    name: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, confirmation_prompt=True, hide_input=True),
):
    """Prompt for user input."""
    print(f"Hello {name}")
```

## Environment Variables

Read values from environment variables:

```python
def main(
    api_key: str = typer.Option(None, envvar="API_KEY"),
):
    """Get API key from environment."""
    print(f"API key: {api_key}")
```

## Testing

Test Typer apps with `CliRunner`:

```python
from typer.testing import CliRunner
from main import app

runner = CliRunner()
result = runner.invoke(app, ["Alice", "--count", "3"])
assert result.exit_code == 0
assert "Hello Alice" in result.stdout
```

## Resources

### references/
- `parameter_types.md` - All supported parameter types with examples
- `commands.md` - Commands, subcommands, and CLI organization
- `progress.md` - Progress bars and spinners

### scripts/
No executable scripts included. Typer is a framework, not a collection of tools.

### assets/
No assets included. This is a pure Python library.

## Development

- Always use `typer.echo()` instead of `print()` for consistent output
- Use `--help` to see generated documentation
- Use `typer.Option()` and `typer.Argument()` for advanced configuration
- Leverage Rich for beautiful console output when possible
- Type hints are your friend - use them for validation and help text
