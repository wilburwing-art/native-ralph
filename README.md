# native-ralph

A single Claude Code skill that routes "I want to loop on X" tasks to the right Anthropic-native primitive, scaffolds a brief in the right shape, and kicks it off after an approval card.

The 5 primitives:

| Primitive | Sweet spot |
|---|---|
| Auto mode | Multi-step local work end-to-end in this session |
| `/loop` interval | Babysit a process, poll state |
| `/loop` dynamic + ScheduleWakeup | Self-paced step-away-and-come-back work |
| `/schedule` one-shot (Cowork) | Deep evaluation at a future date |
| `/schedule` recurring (Cowork) | Daily/weekly maintenance + roadmap pickup |

See `docs/primitive-comparison.md` for tradeoffs per primitive.

## What replaced

This repo started as `ralph-loop`, a plugin implementing the Ralph Wiggum technique (continuous prompt loops via Stop hook + ADK multi-agent pipeline). That work is preserved in git history. As of 2026-05-03, the implementation is replaced with the native-ralph skill because the official Anthropic primitives (`/loop`, `/schedule`, ScheduleWakeup, Auto mode, Cowork routines) now cover what the Ralph Stop-hook was solving for.

The skill is the answer to "which native primitive should I use for this loop, and what's the right brief shape." It is NOT a new looping primitive itself.

## Install

The skill lives at `skill/SKILL.md`. Symlink it into your Claude Code skills dir:

```bash
ln -s "$(pwd)/skill" ~/.claude/skills/native-ralph
```

Then `/native-ralph` is available in any Claude Code session.

## Usage

Trigger by saying things like:

- "loop on this until tests pass"
- "set up a daily routine for repo X"
- "schedule a heatmap evaluation for May 15"
- "babysit this build, ping me every 2 min"
- "keep going on this refactor until done"

The skill will walk you through 8 scoping questions, pick the primitive, fill a template, show an approval card, and kick it off.

## Layout

```
native-ralph/
├── README.md                     # this file
├── CLAUDE.md                     # repo conventions
├── skill/                        # symlink target for ~/.claude/skills/native-ralph
│   ├── SKILL.md                  # chooser logic + 12 steps
│   └── templates/                # prompt scaffolds per primitive
│       ├── cowork-recurring-maintenance.md
│       ├── cowork-oneshot-deep-eval.md
│       ├── loop-interval-poll.md
│       ├── loop-dynamic-self-paced.md
│       └── auto-mode-until-done.md
└── docs/
    └── primitive-comparison.md   # tradeoffs table, expanded
```
