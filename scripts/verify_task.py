"""
verify_task.py

Sanity-checks a candidate benchmark task BEFORE you commit it to
data/tasks/.

Important methodology note (learned the hard way -- see docs/architecture.md):
checking out base_commit alone is NOT enough to reproduce the bug, because
the test file at base_commit doesn't contain the new assertion either --
it was added BY the fix. So the correct check is:

  1. Checkout base_commit (buggy source)
  2. Apply ONLY the test-file changes from fix_commit on top (this is the
     "test patch" -- it makes the new test exist, but the source is still
     buggy) -> run fail_to_pass_tests -> MUST FAIL
  3. Checkout fix_commit fully (source + tests) -> run the same tests
     -> MUST PASS

This mirrors how SWE-bench itself separates the "test patch" from the
"gold patch": the eval harness applies the test patch before the agent
starts, so fail_to_pass_tests genuinely fail at t=0, and the agent's job
is only to fix the source.

Usage:
    python scripts/verify_task.py data/tasks/tqdm-0001.json

Requires: git installed locally. Clones into a throwaway temp dir, never
touches your actual repo.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def install_deps(clone_dir):
    run(["pip", "install", "--quiet", "--break-system-packages", "-e", "."], cwd=clone_dir)
    for candidate in ("requirements-dev.txt", "requirements-test.txt",
                       ".meta/requirements-test.txt", "test-requirements.txt"):
        if (Path(clone_dir) / candidate).exists():
            run(["pip", "install", "--quiet", "--break-system-packages", "-r", candidate], cwd=clone_dir)


def run_tests(clone_dir, test_command):
    result = subprocess.run(test_command, cwd=clone_dir, shell=True, capture_output=True, text=True)
    return result.returncode == 0, (result.stdout[-2000:] + result.stderr[-2000:])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task_file", help="Path to a task JSON file")
    args = parser.parse_args()

    task = json.loads(Path(args.task_file).read_text())
    repo_url = task["repo_url"]
    base_commit = task["base_commit"]
    fix_commit = task["fix_commit"]
    test_command = task["test_command"]

    print(f"Verifying task: {task['task_id']}")
    print(f"  repo: {repo_url}")
    print(f"  base_commit: {base_commit}")
    print(f"  fix_commit: {fix_commit}")
    print(f"  test_command: {test_command}\n")

    workdir = tempfile.mkdtemp(prefix="task_verify_")
    clone_dir = str(Path(workdir) / "repo")
    try:
        print("Cloning...")
        clone = run(["git", "clone", "--quiet", repo_url, clone_dir], cwd=workdir)
        if clone.returncode != 0:
            print(f"FAILED: clone failed: {clone.stderr}")
            sys.exit(1)

        # --- Step 1: checkout base_commit (buggy source) ---
        run(["git", "checkout", "--quiet", base_commit], cwd=clone_dir)

        # --- Step 2: pull ONLY test files forward from fix_commit ---
        diff_files = run(
            ["git", "diff", "--name-only", base_commit, fix_commit, "--", "tests/", "test/"],
            cwd=clone_dir,
        )
        test_files = [f for f in diff_files.stdout.strip().splitlines() if f]
        if not test_files:
            print("FAILED: fix_commit doesn't touch any file under tests/ or test/.")
            print("This task doesn't qualify -- the fix has no accompanying test.")
            print("Pick a different issue (see data/tasks/README.md checklist).")
            sys.exit(1)

        print(f"Test files changed by fix: {test_files}")
        run(["git", "checkout", fix_commit, "--"] + test_files, cwd=clone_dir)

        install_deps(clone_dir)

        print("\n[1/2] Buggy source + new test -- expect FAIL...")
        passed, output = run_tests(clone_dir, test_command)
        if passed:
            print("  UNEXPECTED: tests PASSED with buggy source.")
            print("  Either the bug doesn't reproduce this way, or test_command is wrong.")
            print(output)
            sys.exit(1)
        print("  OK: fails as expected with buggy source + new test.\n")

        # --- Step 3: full fix commit -- expect PASS ---
        run(["git", "checkout", "--quiet", "--force", fix_commit], cwd=clone_dir)
        install_deps(clone_dir)

        print("[2/2] Full fix commit -- expect PASS...")
        passed, output = run_tests(clone_dir, test_command)
        if not passed:
            print("  UNEXPECTED: tests still FAIL on the fix commit.")
            print(output)
            sys.exit(1)
        print("  OK: passes on fix commit.\n")

        print(f"Task '{task['task_id']}' is valid. Safe to keep in data/tasks/.")

    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
