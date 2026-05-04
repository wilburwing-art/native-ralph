# Native primitives for looping work

The 5 Anthropic-native primitives that native-ralph routes between, with their tradeoffs.

## Quick comparison

| Primitive | Where runs | Cadence | Stops when | Best for |
|---|---|---|---|---|
| Auto mode | This terminal session | Continuous | Task done or you take over | Multi-step local work end-to-end |
| `/loop` interval | This terminal session | Fixed (e.g. every 2 min) | You Ctrl-C or condition met | Babysitting a process, polling state |
| `/loop` dynamic | This terminal session | Self-paced via ScheduleWakeup | Skill returns no further wakeup | Step-away-and-come-back work |
| `/schedule` one-shot | Anthropic cloud (Cowork) | Once at time T | After single run | Deep evaluation at a future date |
| `/schedule` recurring | Anthropic cloud (Cowork) | Cron expression | Disabled manually or by failure | Daily/weekly maintenance + roadmap pickup |

Notably out of scope: local cron / launchd. Different kind of automation, machine-bound, not Claude-driven.

## Detailed tradeoffs

### Auto mode

**Pros**: Lowest friction (already in your session), no remote env to set up, full access to your local files and MCPs, can iterate fast.

**Cons**: Tied to this terminal staying open. Can't run while you're away from the machine. No history beyond this session.

**Failure mode**: If task is open-ended and lacks done criteria, Claude grinds indefinitely or stops early.

### `/loop` interval

**Pros**: Predictable cadence, simple to reason about, good for "show me state every N minutes."

**Cons**: Polls even when nothing's changing (cache cost adds up at short intervals). Doesn't actively make progress between checks.

**Failure mode**: Choosing interval shorter than the prompt-cache TTL (5 min) for non-active polling burns budget for nothing.

### `/loop` dynamic + ScheduleWakeup

**Pros**: Smart about when to wake up. Saves cache when nothing's happening. Can span hours/days with idle periods.

**Cons**: More cognitive load to write the wake conditions. Claude has to make judgment calls about when to wake.

**Failure mode**: Claude wakes too aggressively (cache burn) or too rarely (misses the moment). The brief needs to give clear cadence guidance.

### `/schedule` one-shot (Cowork)

**Pros**: Runs in isolated cloud env, can clone any repo, can attach MCPs, doesn't tie up your machine. Perfect for "evaluate X two weeks from now."

**Cons**: No interactive iteration. If the brief is wrong, you find out after the fact. Cold start can be slow (30-60s on top of the work).

**Failure mode**: Brief too narrow, or brief assumes context that the cold remote agent doesn't have.

### `/schedule` recurring (Cowork)

**Pros**: Set and forget. Runs while you sleep. Good for maintenance + opportunistic forward progress.

**Cons**: Same as one-shot, plus: failure modes accumulate silently. The formbook routine auto-disabled after 3 weeks because of a repo-access issue, and nobody noticed for ~10 days.

**Failure mode**: `auto_disabled_repo_access`. Solution: check `claude mcp list` and the routines page periodically; consider a meta-routine that monitors whether the other routines are still running.

## When to choose

Default to `/schedule` for code work in a specific repo unless one of these applies:
- Need real-time iteration in this session: Auto mode
- Need to access local files outside any repo: `/loop`
- Need MCPs that aren't Cowork-attachable: Auto mode or `/loop`
- Task is "watch a process I just started": `/loop` interval

When in doubt: `/schedule` one-shot is the lowest-risk way to test a brief, since it runs once and you see the result before committing to recurring.
