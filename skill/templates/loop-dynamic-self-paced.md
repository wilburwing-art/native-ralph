# Template: /loop dynamic + ScheduleWakeup

Use when work has natural pauses (waiting for a build, a deploy, a reply, a slow remote process) and you want Claude to make judgment calls on cadence rather than running on a fixed clock. Sweet spot: a task that could span hours or days with idle periods, where waking too often burns the prompt cache and waking too rarely misses the moment.

## Brief shape

Use the `/loop` skill with NO interval. Claude self-paces via `ScheduleWakeup`.

```
/loop {{task_prompt}}
```

The `task_prompt` should describe the work AND the conditions for waking up next:

```
{{what_to_do_now}}

Wake up again when {{wake_condition}}, or in {{idle_default}} if nothing changes.

Stop when {{done_condition}}.
```

## Example

Watching a multi-hour Bun build cluster:
```
/loop Check the Bun build cluster status via `bun build:status`. If still running, wake up in 270s (stay in cache). If failed, run `bun build:debug` and report findings. Stop when `bun build:status` reports DONE.
```

Waiting for a PR review:
```
/loop Check `gh pr view 42 --json reviews,state` for new reviews or merge readiness. Wake up every 30 min if no change, or immediately if you see a state change. Stop when the PR is merged or closed.
```

## Cadence guidance for Claude

The Anthropic prompt cache has a 5-minute TTL. The `/loop` skill knows this and recommends:
- Under 5 min (60-270s): cache stays warm, good for active polling
- 5 min to 1 hour (300-3600s): pay the cache miss, good for "no point checking sooner"
- Don't pick exactly 300s (worst-of-both)
- For idle ticks with no signal: 1200-1800s (20-30 min)

Build this into the brief so Claude picks intervals intentionally.

## Fields to fill

- `task_prompt`: the full prompt including what to do and when to wake
- `wake_condition`: what observable change triggers an immediate wake-up
- `idle_default`: how long to wait if nothing observable changes
- `done_condition`: how Claude knows to exit the loop

## Known failure modes

- Claude wakes too aggressively, burning prompt cache. Bake the cache-window guidance into the brief.
- Claude forgets to schedule the next wake-up. The `/loop` skill helps but the brief should remind explicitly.
- Wake-up condition never fires because the underlying state never changes (e.g. a stuck process). Include a max total runtime in the brief: "If still running after 6 hours, escalate."
