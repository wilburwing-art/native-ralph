---
description: "Run ADK multi-agent UI refinement pipeline"
argument-hint: "--url URL [--max-iterations N]"
allowed-tools: ["Bash(*)", "Read(*)", "Write(*)", "Edit(*)"]
hide-from-slash-command-tool: "true"
---

# ADK Multi-Agent UI Refinement Pipeline

Run an autonomous UI refinement loop powered by Google ADK agents.

## How It Works

The pipeline orchestrates 5 specialized agents in a SequentialAgent + LoopAgent architecture:

1. **ScreenshotAgent** — captures baseline screenshot and runs initial tests
2. **AnalyzerAgent** — reads test failures, identifies root causes (loop)
3. **FixerAgent** — applies targeted code fixes (loop)
4. **ValidatorAgent** — re-runs tests, exits loop when all pass (loop)
5. **ReporterAgent** — writes final summary report

Agents 2-4 repeat inside a LoopAgent until tests pass or max iterations reached.

## Usage

```bash
/adk-loop --url http://localhost:3000 --max-iterations 10
```

## Options

- `--url URL` — Target URL for browser tests (default: http://localhost:3000)
- `--max-iterations N` — Maximum refinement loop iterations (default: 5)

## Prerequisites

1. Ensure `GOOGLE_API_KEY` is set (for Gemini model)
2. Dev server running at the target URL
3. Playwright browsers installed: `cd browser-tests && npx playwright install chromium`

## Example

```bash
# Start dev server first
cd your-frontend && npm run dev

# Run the pipeline
/adk-loop --url http://localhost:3000 --max-iterations 8
```

## Under the Hood

This command runs `uv run -m adk_agents` which:
- Uses Google ADK's SequentialAgent and LoopAgent workflow primitives
- Bridges to existing Playwright infrastructure (screenshot.js, validate.js)
- Shares data between agents via ADK session state
- Defaults to Gemini 2.0 Flash (configurable via `ADK_MODEL` env var)
