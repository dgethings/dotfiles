# /// script
# dependencies = [
#   "typer >= 0.20",
#   "pyyaml>=6.0.0"
# ]
# ///
"""
Create Obsidian formatted markdown file summarising YouTube video.
"""

from datetime import date
from pathlib import Path
from typer import Typer, Argument, Option, Exit
from typing import Annotated
import yaml

app = Typer()


def parse_frontmatter(fm: str) -> str:
    """Takes a string in "key1:value1,key2:value2" and returns YAML frontmatter"""
    return yaml.dump(dict(kv.split(":") for kv in fm.split(",")))


@app.command()
def main(
    video_id: Annotated[str, Argument(help="YouTube video ID")],
    filename: Annotated[str, Argument(help="file name to write")],
    tags: Annotated[str, Argument(help="comma separated list of tags")],
    contents: Annotated[str, Argument(help="contents of the obsidian note")],
    frontmatter: Annotated[str, Argument(help="custom fronmatter fields to add")] = "",
    vault_dir: Annotated[
        Path, Argument(envvar="VAULT_DIR", help="Path to Obsidian vault")
    ] = Path.cwd(),
    overwrite: Annotated[
        bool,
        Option(help="whether or not to overwrite the existing file"),
    ] = True,
):
    tags_list = set(["youtube", "video"] + tags.split(","))
    file = vault_dir / Path(f"{filename}.md")
    today = date.today().isoformat()
    custom_fm = parse_frontmatter(frontmatter)

    if file.exists() and overwrite is False:
        print(f"{file.name} already exists and overwrite set to {overwrite}")
        raise Exit(code=2)

    ret_no = file.write_text(f"""---
title: "{filename}"
processed_date: "{today}"
tags: {tags_list}
{custom_fm}
---

{contents}
""")

    if ret_no < 1:
        raise RuntimeError(f"Failed to write any bytes to {file.name}")

    print(f"{file.name} written")


if __name__ == "__main__":
    app()
