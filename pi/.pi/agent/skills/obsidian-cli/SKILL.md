---
name: obsidian-cli
description: Interacts with Obsidian vaults via obsidian-cli. Use for creating, searching, opening, listing, and managing notes in Obsidian.
---

# Obsidian CLI

This skill provides integration with `obsidian-cli` for interacting with your Obsidian vault directly from pi.

## Setup

Ensure `obsidian-cli` is installed:
```bash
brew install obsidian-cli
```

Set your default vault:
```bash
obsidian-cli set-default <vault-name>
```

To find available vaults:
```bash
obsidian-cli print-default
```

## Common Commands

### Create a Note
```bash
obsidian-cli create <note-name>
```
Creates a new note in the default vault.

### Create a Daily Note
```bash
obsidian-cli daily
```
Opens or creates today's daily note.

### Search Notes
```bash
obsidian-cli search <query>
```
Fuzzy search for notes by filename/title.

### Search Note Content
```bash
obsidian-cli search-content <query>
```
Search within note contents for text.

### Open a Note
```bash
obsidian-cli open <note-name>
```
Opens a specific note by name.

### Print Note Contents
```bash
obsidian-cli print <note-name>
```
Outputs the contents of a note to stdout.

### List Files and Folders
```bash
obsidian-cli list [path]
```
Lists files and folders in the vault (optionally within a subfolder).

### Delete a Note
```bash
obsidian-cli delete <note-name>
```
Deletes a note from the vault.

### Move/Rename a Note
```bash
obsidian-cli move <old-name> <new-name>
```
Moves or renames a note and updates all internal links.

### View or Modify Frontmatter
```bash
obsidian-cli frontmatter <note-name>
```
View the YAML frontmatter of a note.
```bash
obsidian-cli frontmatter <note-name> --set key=value
```
Set or update frontmatter fields.

## Usage Tips

- When creating content for Obsidian, consider using Markdown formatting with frontmatter
- Tags in frontmatter should be formatted as: `tags: [tag1, tag2, tag3]`
- Use the search commands to find existing notes before creating new ones
- The `move` command automatically updates links, making it safer than manual renaming