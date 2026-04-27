---
name: summarize-cli
description: Summarize web pages, YouTube videos, local files, and other content using the `summarize` CLI tool. Trigger when the user asks to summarize, extract, or analyze content from a URL (YouTube, website, etc.), a local file, or piped text. Also trigger for extracting slides, transcribing audio/video, or fetching raw content. Uses the ZAI provider (zai/glm-5.1) by default.
---

Use the `summarize` CLI to process and summarize content. The CLI is installed at `/opt/homebrew/bin/summarize`.

## Prerequisites

The ZAI API key is stored in `~/.summarize/config.json`. Always pass it via the `Z_AI_API_KEY` environment variable:

```bash
export Z_AI_API_KEY=$(python3 -c "import json; print(json.load(open('$HOME/.summarize/config.json')).get('zai_api_key',''))")
```

If the key is missing or empty, ask the user for their ZAI API key, save it to `~/.summarize/config.json`, and retry.

## Default Model

Always use `--model zai/glm-5.1` unless the user explicitly requests a different model.

## Common Commands

### Summarize a URL (website or YouTube)

```bash
Z_AI_API_KEY=<key> summarize "<URL>" --model zai/glm-5.1
```

### Summarize with custom length

Lengths: `short`, `medium`, `long`, `xl`, `xxl` (or `s`, `m`, `l`), or a character limit like `20000`.

```bash
Z_AI_API_KEY=<key> summarize "<URL>" --model zai/glm-5.1 --length medium
```

### Summarize YouTube video with timestamps

```bash
Z_AI_API_KEY=<key> summarize "<YOUTUBE_URL>" --model zai/glm-5.1 --timestamps
```

### Extract raw content without LLM summary

```bash
Z_AI_API_KEY=<key> summarize "<URL>" --extract --format md
```

### Extract YouTube transcript as formatted markdown

```bash
Z_AI_API_KEY=<key> summarize "<YOUTUBE_URL>" --extract --format md --markdown-mode llm --model zai/glm-5.1
```

### Summarize with inline slides (YouTube)

```bash
Z_AI_API_KEY=<key> summarize "<YOUTUBE_URL>" --model zai/glm-5.1 --slides
```

### Summarize a local file or stdin

```bash
Z_AI_API_KEY=<key> summarize "/path/to/file" --model zai/glm-5.1
echo "text to summarize" | Z_AI_API_KEY=<key> summarize - --model zai/glm-5.1
```

### Output in a specific language

```bash
Z_AI_API_KEY=<key> summarize "<URL>" --model zai/glm-5.1 --language en
```

### Get JSON output (structured, includes metrics)

```bash
Z_AI_API_KEY=<key> summarize "<URL>" --model zai/glm-5.1 --json
```

### Custom prompt override

```bash
Z_AI_API_KEY=<key> summarize "<URL>" --model zai/glm-5.1 --prompt "Focus on technical implementation details"
```

## Workflow

1. Parse the user's request to determine:
   - Input source: URL, local file, or text
   - Desired output: summary, extraction, slides, transcript
   - Length preference (default: `xl`)
   - Language preference (default: `auto`)
   - Any custom prompt guidance
2. Construct the `summarize` command with appropriate flags.
3. Run the command and return the output to the user.
4. If the command fails, check for common issues (network, API key, timeout) and retry with `--retries 2` if appropriate.

## YouTube-Specific Options

- `--youtube auto` — auto-select transcript source (default)
- `--youtube web` — use web-based transcript extraction
- `--youtube yt-dlp` — use yt-dlp for audio extraction
- `--timestamps` — include timestamps in output
- `--slides` — extract and render slides inline
- `--slides-ocr` — run OCR on extracted slides
- `--slides-max <count>` — max slides to extract (default: 6)

## Other Useful Options

- `--timeout <duration>` — e.g., `2m`, `30s` (default: 2m)
- `--retries <count>` — retry attempts on timeout (default: 1)
- `--verbose` — show detailed progress
- `--no-cache` — bypass LLM cache for fresh results
- `--stream off` — disable streaming for cleaner output capture
