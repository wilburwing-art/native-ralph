# Template: Cowork one-shot deep evaluation

Use for a one-time deep look at a feature, system, or migration after some elapsed time. Sweet spot: "X weeks after launch, evaluate Y, and either remediate or expand based on what you find." This is the Wasatch Heatmap pattern.

## Brief shape

```
You are evaluating {{feature_name}} in this repo ({{repo}}), {{elapsed_window}} after {{milestone}}.

## Step 1: Health check

{{health_check_section}}

Report any non-OK rows or anomalies. Compare metrics from the last {{window_a}} against the {{window_b}} prior. Flag any >2x change in critical numbers.

## Step 2: Decision

If health is GOOD (no recent errors, metrics in expected range, freshness on track), proceed to Step 3.

If health is BAD, open a DRAFT PR titled '{{feature_slug}} diagnosis: <one-line summary>' with:
- a markdown report at docs/{{feature_slug}}-evaluation-{{eval_date}}.md documenting findings
- the raw outputs from Step 1
- proposed remediation steps
- DO NOT change production code in this PR

## Step 3 (only if healthy): {{expansion_workstream_summary}}

{{expansion_details}}

## PR description must include
- What you found in Step 1 (paste the outputs)
- Files changed and why
- Test plan: how to manually verify each new piece after deploy
- Explicit notes on what is deferred to follow-up sprints

## Constraints (read these BEFORE editing)
- Read `.claude/rules/` files and follow them.
- Language strict mode for any code edits.
- Zero self-attribution: no 'Generated with Claude' / 'Co-Authored-By: Claude' anywhere, not in commits, not in PR descriptions.
- If you hit a real blocker (missing data, ambiguous decision, broken assumption from this prompt), open the PR as draft and explain. Don't guess.
- Verify before reporting done: run `{{verify_cmd}}`.

Open the PR(s) when complete and report the URL(s).
```

## Fields to fill

- `feature_name`: e.g. "Wasatch Heatmap"
- `feature_slug`: e.g. "heatmap"
- `repo`: GitHub `org/name`
- `elapsed_window`: e.g. "two weeks", "one month"
- `milestone`: e.g. "launch", "merge to main", "production deploy"
- `eval_date`: target date (YYYY-MM-DD)
- `window_a`, `window_b`: comparison windows e.g. "7 days" vs "7 prior"
- `health_check_section`: SQL queries, curl commands, or similar concrete checks
- `expansion_workstream_summary`: one-line summary of the v2 work
- `expansion_details`: numbered workstreams with concrete file paths and acceptance criteria
- `verify_cmd`: e.g. `npx tsc --noEmit`, `uv run pytest`, `bun test`

## Known failure modes

- Cowork can't reach a private MCP (e.g. Supabase). Confirm the MCP is attached in the routine config.
- SQL queries against tables that don't exist yet. Run a quick `\dt` or equivalent first if uncertain.
- The evaluation date is in the past at run time. Use `run_once_at` and pick a future timestamp.

## Real-world example

This template was extracted from the Wasatch Heatmap routine: `trig_01KQ2eL3wX9xW1WPR53DEVcS` in the user's Cowork account, scheduled for 2026-05-15. See `gh api` or the routine browser for the full prompt as actually deployed.
