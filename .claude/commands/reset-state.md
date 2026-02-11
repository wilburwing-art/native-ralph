# Reset ralph-loop state

Clear all ralph-loop state files.

## Steps

1. Check current state:
```bash
ls -la ~/.claude/ralph-state/ 2>/dev/null || echo "No state directory"
```

2. Clear state:
```bash
rm -rf ~/.claude/ralph-state/*
```

3. Verify:
```bash
ls -la ~/.claude/ralph-state/ 2>/dev/null
```

4. Report: State cleared. Ready for new ralph-loop session.
