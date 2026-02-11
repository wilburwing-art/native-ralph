# Install plugin

Install ralph-loop to Claude Code plugins directory.

## Steps

1. Check if plugins directory exists:
```bash
ls -la ~/.claude/plugins/ 2>/dev/null || echo "Creating plugins directory"
mkdir -p ~/.claude/plugins/
```

2. Create symlink:
```bash
ln -sf "$(pwd)" ~/.claude/plugins/ralph-loop
```

3. Verify installation:
```bash
ls -la ~/.claude/plugins/ralph-loop/
```

4. Report: Plugin installed. Restart Claude Code to activate.
