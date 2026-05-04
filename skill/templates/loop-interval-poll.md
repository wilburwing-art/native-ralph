# Template: /loop interval poll

Use to babysit a process you started, watch a build, or wait for an external state change. Sweet spot: "I started X, ping me when it's done or every N minutes with status."

## Brief shape

Use the `/loop` skill with an explicit interval and a self-contained check command.

```
/loop {{interval}} {{check_command}}
```

The `check_command` should be self-contained: it runs, reports state, and the loop terminates when a condition is met (or you Ctrl-C).

## Examples

Watching a CI run:
```
/loop 2m gh run list --branch=feat/x --limit=1 --json status,conclusion --jq '.[0]'
```

Waiting for a deploy URL to return 200:
```
/loop 1m curl -s -o /dev/null -w "%{http_code}" https://staging.example.com/health
```

Watching a long-running build:
```
/loop 5m tail -n 20 /tmp/build.log
```

## Fields to fill

- `interval`: e.g. `30s`, `2m`, `10m`, `1h`. Match interval to expected change rate (don't poll a 30-min build every 30s).
- `check_command`: shell command that prints state. Should be fast (<5s ideally).

## Known failure modes

- Network commands can hang. Wrap with `timeout 10 <cmd>` if uncertain.
- Loop doesn't auto-terminate; you have to Ctrl-C unless the underlying skill has a stop condition.
- If watching a remote process, ensure auth/credentials don't expire mid-loop.

## When NOT to use this

- The check is slow (>30s): use `/loop` dynamic instead.
- The work needs to happen across days: use `/schedule`.
- You want Claude to make progress on a task between checks: this template is for passive observation only; if you want Claude to actively work, use Auto mode or `/loop` dynamic.
