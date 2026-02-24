# Commands and SubCommands

Organize your CLI into multiple commands and nested command groups.

## Basic Commands

Create multiple commands using `typer.Typer()`:

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

@app.command()
def list():
    """List all users."""
    print("Users: Alice, Bob, Charlie")

if __name__ == "__main__":
    app()
```

Usage:
```bash
$ python main.py create Alice
Creating user: Alice

$ python main.py delete Alice
Deleting user: Alice

$ python main.py list
Users: Alice, Bob, Charlie

$ python main.py --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for current shell.
  --show-completion     Show completion for current shell.
  --help                Show this message and exit.

Commands:
  create  Create a user.
  delete  Delete a user.
  list    List all users.
```

## Custom Command Names

Rename commands using the `name` parameter:

```python
@app.command(name="create-user")
def create_user(name: str):
    """Create a user."""
    print(f"Creating user: {name}")
```

Usage: `python main.py create-user Alice`

## No Args is Help

Show help when no command is provided:

```python
app = typer.Typer(no_args_is_help=True)
```

## Command Help Text

Add help text to commands via function docstring:

```python
@app.command()
def create(name: str):
    """
    Create a new user in the system.

    The user will be created with default settings.
    """
    print(f"Creating user: {name}")
```

## Command Arguments

Commands can have their own arguments and options:

```python
@app.command()
def create(
    name: str = typer.Argument(..., help="User name"),
    email: str = typer.Option(..., help="User email"),
    admin: bool = typer.Option(False, help="Make admin"),
):
    """Create a new user."""
    role = "admin" if admin else "user"
    print(f"Creating {role} {name} ({email})")
```

Usage:
```bash
$ python main.py create Alice --email alice@example.com --admin
Creating admin Alice (alice@example.com)
```

## SubCommands (Command Groups)

Organize related commands into groups:

```python
import typer

app = typer.Typer()
users_app = typer.Typer(help="User management commands")
admin_app = typer.Typer(help="Admin commands")

# Add sub-typer apps
app.add_typer(users_app, name="users")
app.add_typer(admin_app, name="admin")

# Users commands
@users_app.command()
def create(name: str):
    print(f"Creating user: {name}")

@users_app.command()
def delete(name: str):
    print(f"Deleting user: {name}")

# Admin commands
@admin_app.command()
def reset():
    print("Resetting system...")

if __name__ == "__main__":
    app()
```

Usage:
```bash
$ python main.py users create Alice
Creating user: Alice

$ python main.py users delete Alice
Deleting user: Alice

$ python main.py admin reset
Resetting system...

$ python main.py --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  users   User management commands
  admin    Admin commands

$ python main.py users --help
Usage: main.py users [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Create a user.
  delete  Delete a user.
```

## Nested SubCommands

Create deeply nested command structures:

```python
app = typer.Typer()
db_app = typer.Typer()
users_app = typer.Typer()

app.add_typer(db_app, name="db")
db_app.add_typer(users_app, name="users")

@users_app.command()
def create():
    print("Creating database user...")

@users_app.command()
def list():
    print("Listing database users...")
```

Usage:
```bash
$ python main.py db users create
Creating database user...
```

## Command Callbacks

Run code before each command in a group:

```python
users_app = typer.Typer()

@users_app.callback()
def users_callback(verbose: bool = False):
    """Process all users commands."""
    if verbose:
        typer.echo("Verbose mode enabled")

@users_app.command()
def create(name: str):
    print(f"Creating user: {name}")
```

Usage:
```bash
$ python main.py users create Alice --verbose
Verbose mode enabled
Creating user: Alice
```

## Using Context

Access the Click context for advanced use cases:

```python
from typer import Context, Option

@app.command()
def create(
    name: str,
    ctx: Context,
):
    """Create a user with context access."""
    # Access the Click context
    typer.echo(f"Creating user: {name}")
    typer.echo(f"Command info: {ctx.info_name}")
```

## One Command Per File

Organize commands across multiple files:

`main.py`:
```python
import typer
from commands import users, admin

app = typer.Typer()
app.add_typer(users.app, name="users")
app.add_typer(admin.app, name="admin")

if __name__ == "__main__":
    app()
```

`commands/users.py`:
```python
import typer

app = typer.Typer()

@app.command()
def create(name: str):
    print(f"Creating user: {name}")

@app.command()
def delete(name: str):
    print(f"Deleting user: {name}")
```

`commands/admin.py`:
```python
import typer

app = typer.Typer()

@app.command()
def reset():
    print("Resetting system...")
```

## Aliases

Create command aliases:

```python
@app.command("create", aliases=["add", "new"])
def create_user(name: str):
    """Create a user."""
    print(f"Creating user: {name}")
```

Usage:
```bash
$ python main.py create Alice
$ python main.py add Alice
$ python main.py new Alice
# All do the same thing
```

## Hidden Commands

Hide commands from help:

```python
@app.command(hidden=True)
def secret():
    """This won't show in --help."""
    print("Secret command!")
```

## Command Categories

Group commands in help output:

```python
app = typer.Typer()

@app.command(help_category="User Commands")
def create(name: str):
    """Create a user."""
    pass

@app.command(help_category="System Commands")
def status():
    """Show system status."""
    pass

@app.command(help_category="User Commands")
def delete(name: str):
    """Delete a user."""
    pass
```

## Command Sorting

Commands appear in declaration order. Control this by ordering your decorators:

```python
app = typer.Typer()

@app.command()  # Appears 1st
def status():
    """Status."""
    pass

@app.command()  # Appears 2nd
def list():
    """List."""
    pass

@app.command()  # Appears 3rd
def create():
    """Create."""
    pass
```

## Deprecated Commands

Mark commands as deprecated:

```python
@app.command(deprecated=True)
def old_command():
    """This command is deprecated."""
    pass
```

## Rich Integration

Use Rich for beautiful command output:

```python
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

@app.command()
def list():
    """List users in a table."""
    table = Table(title="Users")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Role")

    table.add_row("Alice", "alice@example.com", "Admin")
    table.add_row("Bob", "bob@example.com", "User")

    console.print(table)
```

## Best Practices

1. **Use descriptive command names** - `create-user` vs `mkusr`
2. **Add help text** - Docstrings appear in `--help`
3. **Group related commands** - Use sub-typer for logical organization
4. **Keep commands focused** - One command does one thing well
5. **Use callbacks for setup** - Common initialization logic
6. **Leverage Rich** - Beautiful output when helpful
7. **Consider aliases** - Multiple ways to invoke common commands
8. **Use no_args_is_help** - Better UX for users
