# Error Documentation

Known issues and fixes for ralph-loop plugin.

---

## Loop Not Starting

### "Command not found: /ralph-loop"
**Symptoms**: Slash command doesn't work
**Cause**: Plugin not loaded
**Fix**:
```bash
# Verify plugin is in correct location
ls ~/.claude/plugins/ralph-loop/

# Check manifest exists
cat ~/.claude/plugins/ralph-loop/.claude-plugin/manifest.json

# Restart Claude Code
```

### Loop starts but exits immediately
**Symptoms**: First iteration completes, then stops
**Cause**: Completion promise found in initial output
**Fix**: Make sure your prompt doesn't contain the completion promise text

---

## Loop Not Stopping

### Infinite loop (ignores max-iterations)
**Symptoms**: Keeps iterating past limit
**Cause**: State file not being read correctly
**Fix**:
```bash
# Check state
cat ~/.claude/ralph-state/max-iterations
cat ~/.claude/ralph-state/current-iteration

# Force stop
rm ~/.claude/ralph-state/active
```

### Completion promise not detected
**Symptoms**: Loop continues even after outputting promise
**Cause**: Exact string matching failed
**Fix**:
- Ensure promise is on its own line
- Check for extra whitespace
- Verify exact match: `<promise>DONE</promise>` not `<promise>Done</promise>`

---

## State Issues

### "State directory not found"
**Symptoms**: Hook script errors
**Cause**: State directory doesn't exist
**Fix**:
```bash
mkdir -p ~/.claude/ralph-state
```

### Stale state from previous run
**Symptoms**: Loop behaves unexpectedly
**Cause**: Didn't clean up after last run
**Fix**:
```bash
# Clean all state
rm -rf ~/.claude/ralph-state/*
```

### Wrong prompt being re-injected
**Symptoms**: Claude working on old task
**Cause**: prompt.txt from previous session
**Fix**:
```bash
cat ~/.claude/ralph-state/prompt.txt  # Check content
rm ~/.claude/ralph-state/prompt.txt   # Clear it
```

---

## Hook Issues

### "Permission denied" on hook script
**Symptoms**: Hook fails to execute
**Cause**: Script not executable
**Fix**:
```bash
chmod +x ~/.claude/plugins/ralph-loop/hooks/stop-hook.sh
```

### Hook output not parsed
**Symptoms**: Hook runs but behavior wrong
**Cause**: Invalid JSON output
**Fix**: Ensure hook outputs valid JSON:
```bash
# Test hook manually
echo '{}' | ~/.claude/plugins/ralph-loop/hooks/stop-hook.sh
```

### Hook not firing
**Symptoms**: Exit proceeds without hook check
**Cause**: Hook not registered in settings
**Fix**: Verify `.claude-plugin/manifest.json` has correct hook definitions

---

## Prompt Issues

### Task never completes
**Symptoms**: Loops forever, never outputs promise
**Cause**: Task is impossible or unclear
**Fix**:
- Add clearer success criteria
- Add escape hatch instructions
- Reduce scope

### Work not persisting between iterations
**Symptoms**: Claude starts fresh each iteration
**Cause**: Files not being saved
**Fix**:
- Ensure prompt instructs to save work to files
- Check that files are being written

### Quality degrades over iterations
**Symptoms**: Later iterations worse than earlier
**Cause**: Context pollution or confusion
**Fix**:
- Use clearer phase structure in prompt
- Add explicit "do not undo previous work" instruction

---

## Docker Sandbox Issues

### Plugin not found in sandbox
**Symptoms**: /ralph-loop not available in container
**Cause**: Volume mount missing
**Fix**: Check docker-compose.yml:
```yaml
volumes:
  - ../ralph-loop:/root/.claude/plugins/ralph-loop:ro
```

### State not persisting in sandbox
**Symptoms**: Loop resets on container restart
**Cause**: State in /root/.claude not mounted
**Fix**: Ensure claude-data volume is mounted

---

## Add your own errors below

<!-- Template:
### Error title
**Symptoms**: What you see
**Cause**: Why it happens
**Fix**:
```bash
commands to fix
```
-->
