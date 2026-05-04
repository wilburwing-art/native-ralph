# Template: Cowork recurring maintenance

Use for daily/weekly maintenance + roadmap-task pickup. Sweet spot: a repo that has a `ROADMAP.md` (or similar) where some tasks are tagged `[auto]` for autonomous pickup, and where you want a baseline build/test/lint pass plus opportunistic forward progress every run.

## Brief shape

```
You are a {{cadence}} maintenance and feature agent for {{repo_name}}.

Read CLAUDE.md first for project context and constraints.

## Maintenance (do first)

1. Run `{{install_cmd}}` then `{{build_cmd}}`. If it fails, fix the errors and commit the fix on a `fix/<short-name>` branch with PR.
2. Run `{{test_cmd}}`. If any tests fail, fix them and commit the fix on a `fix/<short-name>` branch with PR.
3. Check for obvious dead code, unused imports, or type issues in recently changed files (last 5 commits). Clean up and commit if found.
4. Run `git log --oneline -10` and summarize recent project momentum.

## Feature work (do second)

5. Read `{{roadmap_file}}`. Pick the top `[auto]` task that is not `[in-progress]`. Implement it on a feature branch (`git checkout -b roadmap/<short-name>`) and open a PR using `gh pr create`. Only pick ONE task per run. If all `[auto]` tasks are `[in-progress]` or done, skip this step.

## Boundaries

Do NOT: make product decisions, push to main, start tasks marked `[needs-input]` or `[blocked]`, refactor working code that isn't broken, or change behavior beyond what the roadmap task specifies.

## Zero self-attribution

No "Generated with Claude" / "Co-Authored-By: Claude" anywhere. Not in commits, not in PR descriptions.

## At the end, write a summary

- What maintenance was done
- Which roadmap task was picked and the PR link
- What still needs the user's attention
```

## Fields to fill

- `cadence`: "daily" or "weekly"
- `repo_name`: e.g. "formbook"
- `install_cmd`: `npm install`, `uv sync`, `bun install`
- `build_cmd`: `npm run build`, `uv build`, `bun run build`
- `test_cmd`: `npx vitest run`, `uv run pytest`, `bun test`
- `roadmap_file`: usually `ROADMAP.md`

## Known failure modes

- `auto_disabled_repo_access`: if the repo is private, ensure Cowork has reauthenticated access. Re-enable at https://claude.ai/code/routines after fixing.
- Slow `npm install` (>5 min): pre-commit a `package-lock.json` and pin Node version in `.nvmrc`.
- Missing `gh` CLI in Cowork env: include `gh auth status` early in the prompt to surface this fast; consider GitHub MCP as alternative.
