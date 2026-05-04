# Template: Auto mode until done

Use for continuous local autonomous work in this terminal session. Sweet spot: a multi-step task you want Claude to grind through end-to-end without confirming each step. Auto mode is the "just keep going" primitive.

## Brief shape

Auto mode is a session-level setting, not a separate skill invocation. The chooser confirms it's on, then starts the work in this session.

```
{{task_description}}

## Boundaries

- Make reasonable assumptions on routine decisions
- Pause and ask only for: destructive operations (rm -rf, dropping data, force push), external messaging (Slack, email, GitHub PR comments), anything that touches production
- When done, report what was changed and what's next

## Done criteria

{{done_criteria}}

## Failure mode

If you hit a real blocker (genuinely ambiguous decision, missing context, broken external dependency), stop and ask. Don't guess.
```

## Fields to fill

- `task_description`: the full multi-step task in clear language. Include file paths and concrete actions where possible.
- `done_criteria`: machine-verifiable end state (tests pass, build green, file exists, X PRs opened, etc.)

## When to use vs alternatives

| Want | Use |
|---|---|
| Multi-step local work, terminal stays open, you watch | Auto mode |
| Same but you want to step away | `/loop` dynamic |
| Same but on a remote sandbox with isolated env | `/schedule` one-shot |
| Recurring version of any of the above | `/schedule` recurring |

## Known failure modes

- Auto mode is OFF: the chooser must verify the user has it on before starting. If off, prompt them to enable via `/auto` or the appropriate toggle.
- Task description too vague: Claude makes wrong assumptions and grinds in the wrong direction. Front-load specificity.
- "Done" undefined: Claude either stops too early or never. Always include explicit done criteria.
