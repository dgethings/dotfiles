# Progress Bars and Spinners

Show progress feedback to users during long-running operations.

## Rich Progress Bars

Rich provides beautiful, feature-rich progress displays.

### Basic Progress Bar

```python
import time
import typer
from rich.progress import track

app = typer.Typer()

@app.command()
def process():
    """Process items with progress bar."""
    for item in track(range(100), description="Processing..."):
        time.sleep(0.05)
        # Your processing logic

if __name__ == "__main__":
    app()
```

Usage: `python main.py process`

Output:
```
Processing... ████████████░░░░░░░░░░░░░░░░  50% 0:00:02
```

### Multiple Progress Bars

Track multiple tasks simultaneously:

```python
from rich.progress import Progress
from rich.console import Console

app = typer.Typer()

@app.command()
def process():
    """Process with multiple progress bars."""
    console = Console()
    with Progress() as progress:
        task1 = progress.add_task("[red]Downloading...", total=100)
        task2 = progress.add_task("[green]Processing...", total=100)

        while not progress.finished:
            progress.update(task1, advance=1)
            time.sleep(0.02)
            progress.update(task2, advance=1)
            time.sleep(0.01)
```

### Custom Progress Display

```python
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

@app.command()
def process():
    """Custom progress bar layout."""
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("Processing...", total=100)
        for _ in range(100):
            time.sleep(0.05)
            progress.update(task, advance=1)
```

### Spinners

Use spinners for indeterminate progress:

```python
from rich.progress import Progress, SpinnerColumn, TextColumn

@app.command()
def load():
    """Show spinner while loading."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Loading...", total=None)
        time.sleep(3)
    typer.echo("Done!")
```

Output (animation):
```
⠋ Loading...
```

### Multiple Spinners

```python
@app.command()
def multi_load():
    """Multiple simultaneous spinners."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task1 = progress.add_task("Downloading...", total=None)
        task2 = progress.add_task("Parsing...", total=None)
        task3 = progress.add_task("Processing...", total=None)
        time.sleep(3)
    typer.echo("All done!")
```

## Typer Progress Bar

Simple progress bar using Click (less feature-rich but simpler):

### Basic Usage

```python
import time
import typer

app = typer.Typer()

@app.command()
def process():
    """Process items with simple progress bar."""
    total = 0
    with typer.progressbar(range(100), label="Processing") as progress:
        for item in progress:
            time.sleep(0.05)
            total += 1
    typer.echo(f"Processed {total} items.")
```

### Explicit Length

When iterable length is unknown (e.g., generator):

```python
def fetch_items():
    """Simulate fetching items from API."""
    for i in range(100):
        yield i

@app.command()
def fetch():
    """Fetch items with explicit length."""
    with typer.progressbar(fetch_items(), length=100) as progress:
        for item in progress:
            time.sleep(0.05)
```

### Manual Updates

Update progress irregularly:

```python
@app.command()
def process_batches():
    """Process in batches with manual updates."""
    total = 1000
    with typer.progressbar(length=total) as progress:
        for batch in range(4):
            time.sleep(1)
            progress.update(250)
    typer.echo(f"Processed {total} items in batches.")
```

### Label

Add a custom label:

```python
@app.command()
def download():
    """Download with custom label."""
    with typer.progressbar(range(100), label="Downloading") as progress:
        for item in progress:
            time.sleep(0.05)
```

## Rich vs Typer Progress Bars

| Feature | Rich | Typer (Click) |
|---------|-------|----------------|
| Visual quality | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Multiple bars | ✅ Yes | ❌ No |
| Custom layouts | ✅ Yes | ❌ No |
| Spinners | ✅ Yes | ✅ Yes |
| Dependencies | `rich` | Built-in |
| Complexity | Medium | Low |

**Recommendation**: Use Rich progress bars when possible for better UX.

## Real-World Examples

### File Download

```python
import requests
from rich.progress import download

@app.command()
def download_file(url: str, output: str):
    """Download a file with progress."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with download(url, total=total_size) as progress:
        with open(output, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                progress.update(len(chunk))
```

### Database Migration

```python
from rich.progress import Progress, TaskID

@app.command()
def migrate():
    """Migrate database with progress."""
    records = fetch_records()  # Your function
    total = len(records)

    with Progress() as progress:
        task = progress.add_task("Migrating...", total=total)
        for record in records:
            migrate_record(record)  # Your function
            progress.update(task, advance=1)
```

### Batch Processing

```python
from rich.progress import track
from rich.console import Console

console = Console()

@app.command()
def process_files(directory: str):
    """Process all files in directory."""
    files = list(Path(directory).glob("*.txt"))

    for file in track(files, description="Processing files"):
        with open(file) as f:
            content = f.read()
            # Process content
        console.print(f"[green]Processed:[/green] {file.name}")
```

### Staged Progress

```python
from rich.progress import Progress, BarColumn, TextColumn

@app.command()
def staged_process():
    """Multi-stage process with progress."""
    stages = ["Extracting", "Transforming", "Loading"]

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        for stage in stages:
            task = progress.add_task(stage, total=100)
            for _ in range(100):
                time.sleep(0.02)
                progress.update(task, advance=1)
```

## Colors and Styling

### Colored Progress Bars

```python
from rich.progress import Progress, BarColumn
from rich.color import Color

@app.command()
def colorful_progress():
    """Progress with custom colors."""
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, complete_style="green", finished_style="bright_green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("Processing...", total=100)
        for _ in range(100):
            time.sleep(0.05)
            progress.update(task, advance=1)
```

### Rainbow Progress

```python
from rich.progress import Progress
from rich.style import Style

@app.command()
def rainbow_progress():
    """Rainbow progress bar."""
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, style=Style(color=colors[0])),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("Processing...", total=100)
        for i in range(100):
            progress.update(task, advance=1, description=f"Processing... {colors[i % 6]}")
```

## Error Handling

```python
from rich.progress import Progress
import typer

@app.command()
def safe_process():
    """Process with error handling."""
    items = list(range(100))

    with Progress() as progress:
        task = progress.add_task("Processing...", total=len(items))
        errors = 0

        for item in items:
            try:
                process_item(item)
            except Exception as e:
                errors += 1
                progress.console.print(f"[red]Error:[/red] {e}")
            finally:
                progress.update(task, advance=1)

        if errors:
            typer.echo(f"Completed with {errors} errors", err=True)
        else:
            typer.echo("Completed successfully")
```

## Best Practices

1. **Always show progress** - Users need feedback for operations > 1 second
2. **Use Rich when possible** - Better visual experience
3. **Provide description** - Tell users what's happening
4. **Handle errors gracefully** - Don't crash on individual item failures
5. **Estimate time** - Rich shows ETA automatically
6. **Consider stages** - Break long operations into phases
7. **Use appropriate visual** - Spinners for indeterminate, bars for known size
