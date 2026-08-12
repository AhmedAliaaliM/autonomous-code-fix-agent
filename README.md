# 🤖 Autonomous Code-Fix Agent

Autonomous AI coding agent that resolves real GitHub issues by analyzing
repositories, planning fixes, modifying code, and iterating with tests until
the issue is resolved. Evaluated with resolve rate, iterations, and
failure-mode analysis on a curated SWE-bench-style benchmark.

**Status:** 🚧 Week 1 — benchmark design + repo skeleton

---

## What it does

Given a GitHub issue and a snapshot of the repo it belongs to, the agent:

1. Indexes the repo (search + read tools)
2. Plans which files are relevant and what the fix should do
3. Edits code through a constrained edit tool
4. Runs the test suite in an isolated sandbox
5. Reads the test output and retries if it fails, up to a fixed iteration cap
6. Reports a patch, plus resolve/fail status and full run metrics

---

## Architecture

```
Issue + repo
   ↓
Repo indexing (search_code, read_file)
   ↓
Planning (LLM forms fix plan)
   ↓
┌─────────────────────────┐
│ Edit file → Run tests   │ ← retries on failure (capped)
└─────────────────────────┘
   ↓
Patch + eval metrics (resolve rate, iterations, tokens, latency, failure mode)
```

---

## Benchmark

Unlike full SWE-bench (2,000+ instances), this uses a small, hand-verified
set of **15–20 real, resolved GitHub issues** pulled from a handful of small
Python repos with clear test suites. Each task record stores the issue text,
the repo snapshot, and the test command that verifies a correct fix — see
[`data/tasks/`](data/tasks/).

Metrics logged per task, aggregated in the eval harness:

| Metric | What it captures |
| --- | --- |
| Resolve rate | Did the agent's patch make the target tests pass? |
| Iterations to resolution | How many edit→test cycles it took |
| Tokens used | Cost per issue |
| Wall-clock latency | Time per issue |
| Failure mode | Wrong file located / wrong fix logic / test flakiness / iteration cap hit |

---

## Tech stack

| Layer | Tool |
| --- | --- |
| Agent loop | Python, raw agent loop (no heavy framework) |
| LLM | Claude / GPT-4-class model, fixed per benchmark run |
| Sandbox | Docker (isolated repo copy per task) |
| Eval harness | Custom, JSON output |
| Task tracking | JSON task records under `data/tasks/` |

---

## Project structure

```
autonomous-code-fix-agent/
├── src/
│   ├── tools/
│   │   ├── read_file.py       # read a file from the sandboxed repo
│   │   ├── search_code.py     # grep-style search across the repo
│   │   ├── edit_file.py       # constrained find/replace or diff-apply edit
│   │   └── run_tests.py       # run the task's test command in sandbox
│   ├── agent.py                # planning + edit/test iteration loop
│   └── evaluate.py             # (week 4) benchmark runner + metrics
├── data/
│   └── tasks/                  # task records (issue, repo, gold test cmd)
├── docs/
│   └── architecture.md
├── tests/                      # tests for the agent's own code
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Run locally

```bash
git clone https://github.com/<your-username>/autonomous-code-fix-agent
cd autonomous-code-fix-agent
python -m venv venv
source venv/bin/activate   # venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env   # add your LLM API key

# Week 4+: run the benchmark
python src/evaluate.py --tasks data/tasks/
```

---

## Roadmap

- [x] Week 1 — Benchmark task set + repo skeleton
- [ ] Week 2 — Core agent loop (tools + single-shot patch generation)
- [ ] Week 3 — Sandboxed execution + edit/test retry loop
- [ ] Week 4 — Evaluation harness + full benchmark run
- [ ] Week 5 — Findings writeup + polished README

## What I'd improve next

- Multi-file, cross-cutting fixes (currently optimized for single/few-file issues)
- Semantic code search instead of grep-based search_code
- Parallel task execution for faster benchmark runs
- Cost-aware early stopping (bail before iteration cap if cost exceeds budget)
