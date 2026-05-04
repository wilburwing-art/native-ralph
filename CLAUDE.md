# native-ralph

Single-skill repo. The skill at `skill/SKILL.md` routes "I want to loop on X" tasks to one of 5 Anthropic-native primitives, scaffolds a brief, and kicks it off.

## Stack

Pure markdown. No code. Skill is loaded by Claude Code's skill system; templates are filled in by the skill at invocation time.

## Layout

- `skill/SKILL.md`: chooser logic, 12 steps from scoping through invocation
- `skill/templates/*.md`: per-primitive prompt scaffolds with field placeholders
- `docs/primitive-comparison.md`: detailed tradeoffs table

## Conventions

- The skill MUST be invoked via the `/native-ralph` slash command, not invented from training data
- Template field placeholders use `{{field_name}}` (Mustache-style). Skill fills these from scoping answers
- Failure modes per template are real, observed failures from the user's history (not hypotheticals)
- Zero self-attribution: nothing in commits, PRs, or code refers to AI authorship
- Updates to the skill propagate via the symlink at `~/.claude/skills/native-ralph`. Edit in this repo, no copy step needed

## When updating templates

Each template has 3 sections:
1. Brief shape (the prompt scaffold itself)
2. Fields to fill (what the chooser asks the user)
3. Known failure modes (real prior incidents)

If you observe a new failure mode in production, add it to the template's failure-mode section. The skill reads these at invocation time to pre-warn the user.

## Relationship to other repos

- `routines`: separate user-owned routine system. native-ralph delegates to `/schedule` (Cowork) when routing recurring work; routines repo holds the actual long-running rotation infrastructure.
- `voice-squad`: orthogonal. Voice-driven multi-session control, not single-task scoping.

## Pre-2026-05-03 history

This repo started as `ralph-loop`, a Stop-hook + ADK plugin. The pivot to native-ralph happened on 2026-05-03 when the Anthropic-native primitives matured to cover the Ralph use case. Prior implementation is in git history.
