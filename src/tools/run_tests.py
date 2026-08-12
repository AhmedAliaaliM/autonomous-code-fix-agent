"""Tool: run a task's test command inside the sandbox and parse the result."""


def run_tests(repo_path: str, test_command: str) -> dict:
    """
    Args:
        repo_path: absolute path to the sandboxed repo checkout
        test_command: shell command from the task record, e.g.
                       "pytest tests/test_config.py -k test_empty_config"

    Returns:
        {"passed": bool, "stdout": str, "stderr": str, "duration_seconds": float}
    """
    raise NotImplementedError("Implemented in Week 3 (sandbox wiring)")
