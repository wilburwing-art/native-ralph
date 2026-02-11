# Ralph Loop Plugin

Claude Code plugin implementing the Ralph Wiggum technique for autonomous iterative development.

## What It Does

Creates a self-referential feedback loop inside Claude Code:
1. You provide a task prompt with completion criteria
2. Claude works on it
3. Stop hook intercepts exit attempts
4. Same prompt fed back automatically
5. Loop continues until completion promise detected or max iterations reached

## Quick Start

```bash
# Start a ralph loop
/ralph-loop "Build a REST API for todos. Output <promise>DONE</promise> when complete." --max-iterations 20

# Cancel active loop
/cancel-ralph
```

## File Structure

```
ralph-loop/
├── .claude-plugin/       # Plugin manifest
├── commands/             # Slash command definitions
│   ├── ralph-loop.md     # /ralph-loop command
│   └── cancel-ralph.md   # /cancel-ralph command
├── hooks/
│   └── stop-hook.sh      # Intercepts exit, creates feedback loop
└── scripts/
    └── ralph-state.sh    # State management utilities
```

## Writing Good Prompts

**Include:**
- Clear completion criteria
- Incremental/phased goals
- Self-correction instructions (TDD approach)
- Completion promise: `<promise>COMPLETE</promise>`

**Example:**
```markdown
Implement feature X following TDD:
1. Write failing tests
2. Implement feature
3. Run tests
4. If any fail, debug and fix
5. Repeat until all green
6. Output: <promise>COMPLETE</promise>
```

## Safety

- **Always set `--max-iterations`** as escape hatch
- Completion promise uses exact string matching
- Include "if stuck after N iterations" instructions in prompt

## When to Use

**Good for:**
- Well-defined tasks with clear success criteria
- Tasks with automatic verification (tests, linters)
- Greenfield projects
- Iterative refinement

**Avoid for:**
- Tasks requiring human judgment
- Unclear success criteria
- Production debugging

## How It Works

The Stop hook (`hooks/stop-hook.sh`) intercepts Claude's session exit:
- Checks if completion promise present in output
- If not, blocks exit and re-injects the original prompt
- Claude sees its previous file changes and continues

This creates "iteration via filesystem" - each loop iteration sees the accumulated work from prior iterations.

## References

- Original technique: https://ghuntley.com/ralph/
- Ralph Orchestrator: https://github.com/mikeyobrien/ralph-orchestrator
