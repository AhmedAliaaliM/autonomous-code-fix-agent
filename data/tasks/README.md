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

## Important: how "fail_to_pass" actually gets verified

Checking out `base_commit` alone and running `fail_to_pass_tests` is **not**
a valid check -- the test itself usually doesn't exist yet at `base_commit`
either (it was added BY the fix), so it will often just pass trivially or
error out as missing. Confirmed on `tqdm-0001`: running the target test at
`base_commit` gave a false pass because the test file hadn't been updated.

The correct check (what `scripts/verify_task.py` actually does):
1. Checkout `base_commit` (buggy source, old test file)
2. Pull forward *only the test file changes* from `fix_commit` (the "test
   patch") -- now the new test exists, but the source bug is still there
3. Run `fail_to_pass_tests` -> must FAIL
4. Checkout `fix_commit` in full -> run same tests -> must PASS

This is the same test-patch/gold-patch split SWE-bench itself uses, and
it's why every task record needs `fix_commit`, not just `base_commit`.

## Checklist per task

- [ ] `fix_commit` recorded, and it touches at least one file under `tests/`
- [ ] `scripts/verify_task.py data/tasks/<task_id>.json` passes cleanly
- [ ] `issue_body` copied verbatim from GitHub (this is literally what the
      agent reads — don't clean it up or add hints)
- [ ] `test_command` runs standalone without needing secrets/external services
- [ ] `difficulty_notes` filled in

## File naming

One JSON file per task: `data/tasks/<task_id>.json`
