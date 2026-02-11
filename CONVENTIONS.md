# Conventions

## Plugin Structure

### Required files
```
.claude-plugin/
└── manifest.json          # Plugin metadata (required)

commands/
└── *.md                   # Slash command definitions

hooks/
└── *.sh                   # Lifecycle hooks
```

### Manifest format
```json
{
  "name": "ralph-loop",
  "version": "1.0.0",
  "description": "Iterative development loops"
}
```

## Slash Command Format

### Frontmatter
```markdown
---
name: ralph-loop
description: Start an iterative development loop
arguments:
  - name: prompt
    description: The task prompt
    required: true
  - name: max-iterations
    description: Maximum iterations
    required: false
    default: "50"
---
```

### Body
Command instructions in markdown, interpolated with `$ARGUMENTS`.

## Hook Conventions

### Input (stdin)
Hooks receive JSON:
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "hook_event_name": "Stop"
}
```

### Output (stdout)
Return JSON for hook-specific behavior:
```json
{
  "hookSpecificOutput": {
    "decision": "block",
    "message": "Loop not complete"
  }
}
```

### Exit codes
| Code | Meaning |
|------|---------|
| 0 | Allow/continue |
| 2 | Block/deny |

## State Management

### Location
```
~/.claude/ralph-state/
```

### Files
```
active                    # Empty file = loop active
prompt.txt               # Original prompt
completion-promise.txt   # Success string
max-iterations           # Limit
current-iteration        # Counter
```

### Atomic updates
```bash
# Use temp file + mv for atomic writes
echo "$value" > "$STATE_DIR/temp.$$"
mv "$STATE_DIR/temp.$$" "$STATE_DIR/current-iteration"
```

## Prompt Writing

### Include completion promise
```markdown
When complete, output: <promise>DONE</promise>
```

### Include escape hatch
```markdown
If blocked after 15 iterations:
- Document what's blocking
- List attempted solutions
- Output: <promise>BLOCKED</promise>
```

### Be specific about success criteria
```markdown
# BAD
Build a todo API

# GOOD
Build a REST API for todos:
- CRUD endpoints (GET/POST/PUT/DELETE)
- Input validation with Pydantic
- Tests passing (pytest)
- README with usage examples

Output <promise>COMPLETE</promise> when all criteria met.
```

## Shell Script Style

### Use bash strict mode
```bash
#!/bin/bash
set -euo pipefail
```

### Quote variables
```bash
# YES
echo "$STATE_DIR/prompt.txt"

# NO
echo $STATE_DIR/prompt.txt
```

### Check file existence
```bash
if [[ -f "$STATE_DIR/active" ]]; then
    # Loop is active
fi
```

## Documentation

### README.md must include
- What the plugin does
- Quick start example
- Command reference
- Prompt writing best practices
- When to use / not use

## Anti-Patterns (DO NOT)

- ❌ Use exact string matching for multiple conditions
- ❌ Skip max-iterations safety net
- ❌ Leave state files after deactivation
- ❌ Block exit without clear reason
- ❌ Use for tasks requiring human judgment
- ❌ Forget to document escape hatches
