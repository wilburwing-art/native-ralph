# Ralph Loop

Claude Code plugin for self-referential AI development loops + ADK multi-agent pipeline for autonomous UI refinement.

## Two Systems

### 1. Bash Plugin (Stop Hook Loop)

The core loop uses a Stop hook (`hooks/stop-hook.sh`) to intercept exit, re-inject prompts, and iterate via filesystem state.

- `/ralph-loop` — start a loop with completion promise
- `/cancel-ralph` — cancel active loop
- `/browser-loop` — loop with Playwright browser test validation
- State stored in `.claude/ralph-loop.local.md` (YAML frontmatter + markdown)

### 2. ADK Multi-Agent Pipeline (Python)

5 LlmAgents wired into `SequentialAgent` + `LoopAgent` for autonomous UI refinement:

```
SequentialAgent("ui_refinement_pipeline")
├── ScreenshotAgent     → baseline screenshot + initial tests
├── LoopAgent("refinement_loop")
│   ├── AnalyzerAgent   → reads failures, identifies root causes
│   ├── FixerAgent      → applies targeted code changes
│   └── ValidatorAgent  → re-runs tests, exit_loop when passing
└── ReporterAgent       → final summary
```

- `/adk-loop` — run ADK pipeline via slash command
- CLI: `uv run -m adk_agents --url <URL> --max-iterations N`
- Tools bridge to existing Node.js Playwright scripts (no reimplementation)
- Requires `GOOGLE_API_KEY` for Gemini model

## Project Structure

```
ralph-loop/
├── commands/             # Slash commands (/ralph-loop, /adk-loop, etc.)
├── hooks/                # Stop hook (bash loop core)
├── scripts/              # Setup + bridge scripts
├── adk_agents/           # ADK multi-agent pipeline (Python)
│   ├── agents/           # 5 specialized LlmAgents
│   ├── tools/            # Playwright bridge, file ops, loop control
│   ├── agent.py          # Pipeline assembly
│   └── runner.py         # CLI entry point
├── test/                 # BATS tests (bash)
├── tests/                # pytest tests (Python)
└── browser-tests/        # Playwright test infrastructure (Node.js)
```

## Development

```bash
# Bash tests
bats test/*.bats

# Python tests
uv run pytest tests/ -v

# Browser tests
cd browser-tests && npm test
```

## Conventions

- Python managed by `uv` — no pip/poetry
- ADK agents use `output_key` to share state between pipeline steps
- Tools that need Playwright shell out to `browser-tests/scripts/` Node.js scripts
- `exit_loop` tool uses `tool_context.actions.escalate = True` to break LoopAgent
- Config via env vars: `ADK_TARGET_URL`, `ADK_MAX_ITERATIONS`, `ADK_MODEL`, `GOOGLE_API_KEY`
