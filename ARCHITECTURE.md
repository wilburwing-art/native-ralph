# Architecture

## Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│                     SELF-REFERENTIAL LOOP                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌─────────┐     ┌─────────┐     ┌─────────┐                 │
│    │  START  │────▶│  WORK   │────▶│  EXIT?  │                 │
│    │         │     │         │     │         │                 │
│    └─────────┘     └─────────┘     └────┬────┘                 │
│                          ▲              │                       │
│                          │              ▼                       │
│                          │       ┌─────────────┐               │
│                          │       │ Stop Hook   │               │
│                          │       │ Intercepts  │               │
│                          │       └──────┬──────┘               │
│                          │              │                       │
│                          │     ┌────────▼────────┐             │
│                          │     │ Promise Found?  │             │
│                          │     └────────┬────────┘             │
│                          │              │                       │
│                          │    NO        │        YES            │
│                          │◀─────────────┴──────────────▶EXIT   │
│                          │                                      │
│                    Re-inject                                    │
│                    same prompt                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Plugin Structure

```
ralph-loop/
├── .claude-plugin/
│   └── manifest.json       # Plugin metadata
├── commands/
│   ├── ralph-loop.md       # /ralph-loop slash command
│   └── cancel-ralph.md     # /cancel-ralph command
├── hooks/
│   └── stop-hook.sh        # Intercepts session exit
├── scripts/
│   └── ralph-state.sh      # State management utilities
└── README.md
```

## Hook Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        stop-hook.sh                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Read stdin (JSON with session state)                        │
│                                                                  │
│  2. Check: Is ralph-loop active?                                │
│     └─▶ NO  → Exit 0 (normal exit allowed)                      │
│     └─▶ YES → Continue...                                       │
│                                                                  │
│  3. Check: Completion promise found in output?                  │
│     └─▶ YES → Deactivate loop, exit 0                          │
│     └─▶ NO  → Continue...                                       │
│                                                                  │
│  4. Check: Max iterations reached?                              │
│     └─▶ YES → Deactivate loop, exit 0                          │
│     └─▶ NO  → Continue...                                       │
│                                                                  │
│  5. Increment iteration counter                                 │
│                                                                  │
│  6. Output JSON to re-inject original prompt                    │
│                                                                  │
│  7. Exit 2 (block normal exit, continue loop)                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## State Management

```
~/.claude/ralph-state/
├── active                  # Empty file = loop is active
├── prompt.txt              # Original prompt (re-injected each iteration)
├── completion-promise.txt  # String to detect completion
├── max-iterations          # Iteration limit
└── current-iteration       # Counter
```

## Iteration Model

```
Iteration 1:                 Iteration 2:                 Iteration N:
┌─────────────┐             ┌─────────────┐             ┌─────────────┐
│ Read prompt │             │ Read prompt │             │ Read prompt │
│     │       │             │     │       │             │     │       │
│     ▼       │             │     ▼       │             │     ▼       │
│ Create      │             │ See files   │             │ See all     │
│ initial     │────────────▶│ from iter 1 │────────────▶│ previous    │
│ files       │             │ Improve     │             │ work        │
│     │       │             │     │       │             │     │       │
│     ▼       │             │     ▼       │             │     ▼       │
│ [no promise]│             │ [no promise]│             │ [PROMISE!]  │
└─────────────┘             └─────────────┘             └─────────────┘
    │                           │                           │
    └───────────────────────────┴───────────────────────────┘
              Filesystem is the persistent memory
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Stop hook (not bash loop) | Loop happens inside Claude session, preserves context |
| Exact string matching | Simple, reliable promise detection |
| Filesystem as memory | Claude sees git history, file changes between iterations |
| max-iterations required | Safety net for impossible tasks |
| State in ~/.claude/ | Persists across session restarts |
