# Architecture

```
Issue + repo
   |
   v
Repo indexing (search_code, read_file)
   |
   v
Planning (LLM forms fix plan)
   |
   v
+-------------------------+
| Edit file -> Run tests  |  <- retries on failure, capped at MAX_ITERATIONS
+-------------------------+
   |
   v
Patch + eval metrics (resolve rate, iterations, tokens, latency, failure mode)
```

## Tools (the agent's action space)

Kept deliberately narrow -- four tools, each with a small, structured
interface -- rather than raw shell access. This keeps every agent action
loggable and diffable, and makes failure-mode analysis meaningful (you can
say *which* tool call went wrong, not just that the agent "failed").

| Tool | Purpose |
| --- | --- |
| `search_code` | grep-style search across the repo, to locate relevant files |
| `read_file` | read a file's contents |
| `edit_file` | exact find/replace edit -- forces the agent to quote existing code back, which catches hallucinated line numbers/content early |
| `run_tests` | execute the task's test command inside the sandbox |

## Iteration loop

1. Agent proposes an edit via `edit_file`
2. `run_tests` executes the task's `test_command`
3. If tests pass -> done, resolved=True
4. If tests fail -> stdout/stderr fed back to the agent as context, loop to 1
5. If `MAX_ITERATIONS` reached without passing -> resolved=False, failure_mode logged

## Sandbox

Each task runs in its own isolated copy of the target repo inside the
Docker image defined in `Dockerfile`. The agent never touches the host
filesystem or any other task's repo copy. This also means task runs are
naturally parallelizable later (Week 4+ improvement).

## Eval metrics

See `data/tasks/schema.json` for what defines "resolved" (the
`fail_to_pass_tests` list). The eval harness (`src/evaluate.py`, Week 4)
aggregates per-task results into:

- Resolve rate (primary headline number)
- Iterations to resolution (distribution, not just mean)
- Tokens used / cost per task
- Wall-clock latency per task
- Failure mode breakdown, categorized manually after inspecting failed runs:
  wrong file located / correct file but wrong fix logic / test flakiness /
  hit iteration cap without converging
