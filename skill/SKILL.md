---
name: native-ralph
description: Route a "I want to loop on X" task to the right Anthropic-native primitive (Auto mode, /loop interval, /loop dynamic + ScheduleWakeup, /schedule one-shot Cowork, or /schedule recurring Cowork). Walks through an 8-step scoping interview, picks the primitive, fills a template, shows a Plan-Mode-style approval card with known failure modes for the target repo, then invokes the primitive. Trigger when the user says "loop on X", "schedule X", "kick off X recurring", "babysit X", "keep going on X until done", "set up a routine for X", or asks how to set up an iterative or recurring task. Replaces the old ralph-loop Stop-hook plugin.
---

# native-ralph

Route a looping task to one of 5 native Anthropic primitives, scaffold a brief in the right shape for that primitive, show an approval card, and kick it off.

## Step 1: Task Description

Ask: **What specifically needs to happen?**

Get a concrete description of the work. Push back on vague answers, "make it better" is not actionable. A good task description names the files, components, behaviors, or repos involved.

## Step 2: Judgment Check

Evaluate whether the task requires human design decisions (color choices, UX flows, copy tone, architecture tradeoffs with no clear winner).

- If yes, warn that loops work poorly for subjective decisions. Suggest breaking off the judgment-dependent parts for manual work and looping only the mechanical remainder.
- If no, continue.

## Step 3: Completion Criteria

Ask: **What measurable outcome defines done?**

Push for something concrete and machine-verifiable:
- Tests pass (`npm test`, `uv run pytest`, `npx playwright test`)
- Build succeeds (`npm run build`, `uv build`)
- Lint clean (`npx eslint . --max-warnings 0`, `uv run ruff check .`)
- Visual match (screenshot diff under threshold)
- Specific behavior observable in output
- For recurring tasks: cadence with no failure window (e.g. green build at end of every nightly run)

If the user can't name a verification command, help them write one or flag that the task may not be a good loop candidate.

## Step 4: Verification Command

Ask: **What command validates success?**

This becomes the command that runs each iteration (for self-paced loops) or at the end of each scheduled run.

If none exists, help the user create a minimal check.

## Step 5: Phase Breakdown

For complex tasks, ask: **Can this be split into sequential phases?**

Each phase should have its own checkpoint. Simple tasks skip this step.

## Step 6: Iteration / Cadence

For self-paced loops, ask: **How many iterations should this get?**

- 5-10: simple well-defined fixes
- 10-20: medium tasks
- 20-30: complex tasks
- 30+: only for well-understood patterns

For scheduled recurring tasks, ask: **What cadence?** (cron expression or natural-language convert via the schedule skill)

For one-shot scheduled tasks, ask: **When?** (specific date/time)

## Step 7: Escape Strategy

Ask: **What should happen if it gets stuck?**

- Document and stop (safest default)
- Try alternative approach after N consecutive failures
- Partial commit and stop

## Step 8: Primitive Selection

Based on everything gathered, pick the primitive. Auto-detect from phrasing where possible:

| Phrasing | Primitive |
|---|---|
| "every X minutes/hours/days", "daily/weekly", "nightly" | `/schedule` recurring (or `/loop` interval if local-only) |
| "once at <time>", "tomorrow morning", "next Monday" | `/schedule` one-shot |
| "keep going until done", "iterate until X", "finish this" | Auto mode |
| "babysit", "watch", "poll", "check on" | `/loop` interval |
| "self-paced", "step away and come back" | `/loop` dynamic + ScheduleWakeup |

Decision tree when not obvious:

```
Where should this run?
├── Remote (Anthropic cloud, isolated env, can clone repos)
│   └── /schedule
│       ├── Once at time T → run_once_at
│       └── Recurring cron → cron_expression
└── Local (this terminal, this machine)
    ├── Open-ended "keep going until done" → Auto mode
    ├── Recurring on fixed interval → /loop <interval>
    └── Self-paced → /loop dynamic + ScheduleWakeup
```

Default to remote (`/schedule`) for code work in a specific repo unless the user says they want it local. Local primitives (`/loop`, Auto mode) are for tasks that need access to this machine's state (running processes, local files outside any repo, MCPs that aren't Cowork-attachable).

## Step 9: Read prior failure modes

If a repo is involved, scan `~/.claude/projects/-Users-wilburpyn-repos/memory/` for any memory file mentioning failures, auto-disable, or "didn't work" notes related to that repo or pattern. Surface those as "Failure modes to expect" in the approval card.

Built-in failure catalog:
- `auto_disabled_repo_access`: Cowork lost access to a private repo. Reauth via https://claude.ai/code/routines.
- `npm install` taking >5 min in Cowork: flag as a slow-start risk; consider committing a `package-lock.json` or pinning Node version.
- Cowork not finding gh CLI: pre-install in the prompt or use the GitHub MCP.

## Step 10: Pick a template

Templates live in this skill's `templates/` dir:

| Template | When to use |
|---|---|
| `cowork-recurring-maintenance.md` | Daily/weekly maintenance + roadmap-task pickup pattern (formbook style) |
| `cowork-oneshot-deep-eval.md` | One-time deep evaluation against a repo (Wasatch Heatmap style) |
| `loop-interval-poll.md` | Babysit a process you started locally |
| `loop-dynamic-self-paced.md` | Step-away-and-come-back work via ScheduleWakeup |
| `auto-mode-until-done.md` | Continuous local autonomous work in this session |

Read the template, fill in the blanks based on the task description, present the result in the approval card.

## Step 11: Show approval card

Format the card as a code-fenced block:

```
native-ralph: <primitive>
─────────────────────────
Repo:        <repo or "none">
Cadence:     <human-readable schedule>
Model:       <model>
MCP:         <connectors or "none">

Task brief (editable):
  <filled-in template>

Success criteria:
  - <criterion 1>
  - <criterion 2>

Failure modes to expect:
  - <known mode 1>
  - <known mode 2>
```

Then ask via AskUserQuestion:
- approve: invoke and create
- edit: re-open the brief for editing
- cancel: stop here

## Step 12: Invoke

On approval, route to the right invocation:

- `/schedule` recurring or one-shot: invoke the schedule skill with the filled-in args (repo URL, cron or run_once_at, prompt body, MCP connections, model)
- `/loop` interval: invoke the loop skill with `interval prompt`
- `/loop` dynamic: invoke the loop skill with no interval; the loop skill will use ScheduleWakeup itself
- Auto mode: confirm auto mode is on, then start the work in this session

Report what was created (routine ID + claude.ai/code/routines URL, or just confirmation that the loop is running).

## Don't

- Don't invoke local cron / launchd. Out of scope; tell user to use a different tool.
- Don't push code or take destructive actions inside the kicked-off loop without explicit user approval baked into the brief.
- Don't reuse routine IDs across primitives.
- Don't skip the approval card. Even on auto mode, show it; users can approve fast.
