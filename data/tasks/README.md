# Benchmark task set

This folder holds the 15–20 hand-picked, resolved GitHub issues the agent
will be evaluated against. See `schema.json` for the record format and
`example_task.json` for a filled-in sample.

## How to pick good issues

**What makes a repo a good source:**
- Small-to-medium Python codebase (a few thousand LOC, not a monorepo)
- Has an actual test suite that runs with a single `pytest` command
- Active enough to have real, merged bugfix PRs with linked issues
- Not so large/complex that a human would need days to orient — you want
  the agent's failures to be informative, not just "codebase too big"

Good places to look: mid-size CLI tools, small libraries, Flask/FastAPI
utility packages. Avoid ML repos with GPU-dependent tests (sandbox can't
run them) and anything with heavy external service dependencies (databases,
paid APIs) unless you're prepared to mock them.

**How to find a candidate issue:**
1. On the repo, filter closed issues/PRs by label like `bug` or `fix`
2. Find one where the PR that closed it also **added or modified a test**
   — this is essential, since that test becomes your `fail_to_pass` check
3. Note the commit *before* the fix was merged as `base_commit`
4. Confirm: checking out `base_commit` and running the new test should FAIL;
   checking out the fix commit should PASS. Verify this manually before
   adding the task — a task with a flaky or already-passing test is worse
   than no task at all, since it silently inflates your resolve rate

**Difficulty spread:** aim for a mix — some single-file/single-function
fixes (sanity checks that a working agent should mostly solve), some
multi-file or logic-heavy fixes (the ones that actually differentiate a
good agent from a mediocre one). Note this in `difficulty_notes` — it
feeds directly into the failure-mode breakdown in Week 4.

## Checklist per task

- [ ] `base_commit` checked out and confirmed to FAIL `fail_to_pass_tests`
- [ ] Fix commit checked out and confirmed to PASS the same tests
- [ ] `issue_body` copied verbatim from GitHub (this is literally what the
      agent reads — don't clean it up or add hints)
- [ ] `test_command` runs standalone without needing secrets/external services
- [ ] `difficulty_notes` filled in

## File naming

One JSON file per task: `data/tasks/<task_id>.json`
