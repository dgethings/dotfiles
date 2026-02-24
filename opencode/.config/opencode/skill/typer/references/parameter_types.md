# Parameter Types

Typer uses Python type hints for automatic type conversion and validation.

## Basic Types

### String

```python
def main(name: str):
    print(f"Hello {name}")
```

Usage: `python main.py Alice`

### Integer

```python
def main(count: int):
    print(f"Count: {count}")
```

Usage: `python main.py 42`
- Automatically converts "42" to `42`
- Validates input is an integer

### Float

```python
def main(price: float):
    print(f"Price: ${price:.2f}")
```

Usage: `python main.py 19.99`
- Converts to float
- Accepts both integers and decimals

### Boolean

Boolean parameters become flags with `--flag` and `--no-flag`:

```python
def main(verbose: bool = False):
    if verbose:
        print("Verbose mode on")
```

Usage:
```bash
$ python main.py --verbose
Verbose mode on

$ python main.py --no-verbose
# verbose = False

$ python main.py
# verbose = False (default)
```

## Optional Types

### Optional String

```python
from typing import Optional

def main(name: Optional[str] = None):
    if name:
        print(f"Hello {name}")
    else:
        print("Hello World")
```

### Optional with Default

```python
from typing import Optional

def main(name: Optional[str] = typer.Option(None, "--name", "-n")):
    pass
```

## Lists (Multiple Values)

### Multiple Options

```python
def main(items: list[str] = typer.Option([])):
    """Accept multiple values."""
    for item in items:
        print(item)
```

Usage: `python main.py --items apple --items banana --items cherry`

### Multiple Arguments

```python
def main(items: list[str]):
    """Accept multiple arguments."""
    for item in items:
        print(item)
```

Usage: `python main.py apple banana cherry`

### Limited Multiple Values

```python
def main(items: list[str] = typer.Option([], min=1, max=3)):
    """Accept 1-3 values."""
    pass
```

## Enum (Choices)

Restrict values to specific choices:

```python
from enum import Enum

class Color(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"

def main(color: Color = typer.Option(Color.blue)):
    print(f"Color: {color.value}")
```

Usage:
```bash
$ python main.py --color red
Color: red

$ python main.py --color yellow
# Error: Invalid value for '--color': 'yellow' is not one of 'red', 'green', 'blue'.
```

## DateTime

```python
from datetime import datetime

def main(date: datetime = typer.Argument(...)):
    print(f"Date: {date}")
```

Usage:
- `python main.py "2024-01-15"` - ISO format
- `python main.py "01/15/2024"` - US format
- `python main.py "15-Jan-2024"` - UK format

### DateTime Options

```python
def main(
    start: datetime = typer.Option(..., formats=["%Y-%m-%d", "%d/%m/%Y"]),
):
    pass
```

## Path

```python
from pathlib import Path

def main(config: Path = typer.Argument(...)):
    print(f"Config file: {config}")
    print(f"Exists: {config.exists()}")
```

Usage: `python main.py ./config.yaml`

### Path Options

```python
def main(
    path: Path = typer.Argument(
        ...,
        exists=True,        # Path must exist
        file_okay=True,     # Must be a file
        dir_okay=False,      # Cannot be directory
        readable=True,       # Must be readable
        resolve_path=True,    # Return absolute path
    ),
):
    pass
```

## File

For file I/O operations:

```python
def main(
    input_file: typer.FileText = typer.Argument(...),
    output_file: typer.FileTextWrite = typer.Option(...),
):
    """Read from input, write to output."""
    content = input_file.read()
    output_file.write(content.upper())
```

Usage:
```bash
$ python main.py input.txt --output-file output.txt
```

### Binary Files

```python
def main(
    input_file: typer.FileBinaryRead = typer.Argument(...),
    output_file: typer.FileBinaryWrite = typer.Option(...),
):
    data = input_file.read()
    output_file.write(data)
```

## UUID

```python
from uuid import UUID

def main(user_id: UUID = typer.Argument(...)):
    print(f"User ID: {user_id}")
```

Usage: `python main.py 123e4567-e89b-12d3-a456-426614174000`

## Custom Types

Define your own type validators:

```python
class Username(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v

def main(username: Username):
    print(f"Username: {username}")
```

## Numbers with Ranges

### Integer Range

```python
def main(
    age: int = typer.Option(18, min=0, max=120),
):
    print(f"Age: {age}")
```

### Float Range

```python
def main(
    rating: float = typer.Option(3.5, min=0.0, max=5.0),
):
    print(f"Rating: {rating}")
```

## Default Values

### Simple Default

```python
def main(count: int = 10):
    print(f"Count: {count}")
```

### None Default with Optional

```python
def main(name: Optional[str] = None):
    if name is None:
        name = "World"
    print(f"Hello {name}")
```

### typer.Option Default

```python
def main(
    color: str = typer.Option("blue", "--color", "-c"),
):
    print(f"Color: {color}")
```

## Type Conversion Errors

Typer provides clear error messages for type mismatches:

```python
def main(age: int):
    print(f"Age: {age}")
```

```bash
$ python main.py twenty
Error: Invalid value for 'age': 'twenty' is not a valid integer

$ python main.py 25.5
Error: Invalid value for 'age': '25.5' is not a valid integer
```

## Combining Types

```python
from typing import Optional
from datetime import datetime
from pathlib import Path

def main(
    name: str = typer.Argument(...),
    age: int = typer.Option(18, min=0, max=120),
    active: bool = False,
    tags: list[str] = typer.Option([]),
    config: Optional[Path] = typer.Option(None, exists=True),
    created: datetime = typer.Option(...),
):
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"Active: {active}")
    print(f"Tags: {tags}")
    print(f"Config: {config}")
    print(f"Created: {created}")
```

## Best Practices

1. **Use explicit types** - Avoid `Any`, use specific types for validation
2. **Provide defaults** - Make common cases easy with sensible defaults
3. **Use Enums for choices** - Clearer than string validation
4. **Add help text** - Document what each parameter does
5. **Use Path/File types** - Leverage automatic validation
6. **Consider Optional** - When None is a valid value
7. **Custom types for validation** - Complex validation logic in one place
