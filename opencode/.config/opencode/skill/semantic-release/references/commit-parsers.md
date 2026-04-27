# Commit Parser Reference

PSR parses commit messages to determine the type of version bump. Choose a parser that matches your team's commit convention.

## conventional (Recommended Default)

Based on Conventional Commits. This is the most common and the one PSR defaults to.

```toml
[tool.semantic_release]
commit_parser = "conventional"

[tool.semantic_release.commit_parser_options]
minor_tags = ["feat"]
patch_tags = ["fix", "perf"]
parse_squash_commits = true
ignore_merge_commits = true
```

**Commit message format:**
```
type(scope): description

body
```

**Types and their default bump levels:**
| Type | Bump | Example |
|------|------|---------|
| `feat` | minor | `feat(auth): add OAuth2 login flow` |
| `fix` | patch | `fix(api): correct pagination offset` |
| `perf` | patch | `perf(db): optimize query indexing` |
| `BREAKING CHANGE` | major | `feat(api): redesign response format\n\nBREAKING CHANGE: all endpoints now return JSON` |
| Other (`chore`, `ci`, `docs`, `style`, `refactor`, `test`) | none | `ci(github): update action versions` |

**Major bump via `!`:**
```
feat(api)!: redesign response format
```

## angular

Similar to conventional but uses a different parsing style.

```toml
[tool.semantic_release]
commit_parser = "angular"
```

## emoji

Emoji-prefixed commits.

```toml
[tool.semantic_release]
commit_parser = "emoji"

[tool.semantic_release.commit_parser_options]
major_tags = ["💥"]
minor_tags = ["✨"]
patch_tags = ["🐛", "🩹", "⚡"]
```

## scipy

Scipy-style commit messages.

```toml
[tool.semantic_release]
commit_parser = "scipy"
```

## Custom Parser

You can write your own parser as a Python module and reference it:

```toml
[tool.semantic_release]
commit_parser = "my_package.parser:parse_commit"
```

## Choosing the Right Parser

- **If the project already has a commit convention** — match the parser to it
- **If starting fresh** — use `conventional` and set up commitlint or a similar tool
- **Check existing commits** — run `git log --oneline -20` to see what style the project uses
