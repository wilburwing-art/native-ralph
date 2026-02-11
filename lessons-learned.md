# Lessons Learned

Project-specific discoveries and insights for ralph-loop.

---

## Loop Design

### YYYY-MM-DD: Filesystem as memory
**Context**: [Describe situation]
**Learning**: Claude doesn't remember between iterations, but it can read files. Write everything to disk.
**Impact**: Core design principle: persist all work to files.

### YYYY-MM-DD: Exact string matching limits
**Context**: [Describe situation]
**Learning**: Can't use completion promise for multiple exit conditions (SUCCESS vs BLOCKED). Exact match only.
**Impact**: Rely on max-iterations for safety, not conditional promises.

### YYYY-MM-DD: Stop hook vs bash loop
**Context**: [Describe situation]
**Learning**: External bash loop loses Claude's context. Stop hook keeps the session alive.
**Impact**: Implemented as stop hook, not external wrapper.

---

## Prompt Engineering

### YYYY-MM-DD: Clear success criteria
**Context**: [Describe situation]
**Learning**: Vague goals = infinite loops. "Make it good" never terminates. "All tests pass" terminates.
**Impact**: Added prompt writing guidelines.

### YYYY-MM-DD: Phased approaches
**Context**: [Describe situation]
**Learning**: Breaking large tasks into phases helps Claude track progress and not repeat work.
**Impact**: Recommend phase structure in documentation.

### YYYY-MM-DD: Escape hatches
**Context**: [Describe situation]
**Learning**: Some tasks are impossible. Need instructions for what to do when stuck.
**Impact**: Added "if stuck after N iterations" pattern.

---

## State Management

### YYYY-MM-DD: Atomic file writes
**Context**: [Describe situation]
**Learning**: Writing directly to state files can corrupt on interrupt. Use temp file + mv.
**Impact**: Refactored state updates to be atomic.

### YYYY-MM-DD: State cleanup
**Context**: [Describe situation]
**Learning**: Leftover state from previous runs causes confusing behavior. Clean state on start.
**Impact**: Added state reset logic.

---

## Safety

### YYYY-MM-DD: max-iterations is essential
**Context**: [Describe situation]
**Learning**: Without a limit, impossible tasks run forever (and burn credits).
**Impact**: Made max-iterations effectively required.

### YYYY-MM-DD: [Title]
**Context**: [Describe situation]
**Learning**: [What you learned]
**Impact**: [How it changed the project]

---

## Integration

### YYYY-MM-DD: Docker sandbox synergy
**Context**: [Describe situation]
**Learning**: Ralph + sandbox = fully autonomous development. Good for greenfield projects.
**Impact**: Documented sandbox integration.

### YYYY-MM-DD: [Title]
**Context**: [Describe situation]
**Learning**: [What you learned]
**Impact**: [How it changed the project]

---

## Template

<!--
### YYYY-MM-DD: Brief title
**Context**: What were you trying to do?
**Learning**: What did you discover?
**Impact**: How did this change the project?
-->
