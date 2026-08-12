"""
Core agent loop -- planning, editing, and test-driven iteration.

Week 1: stub only. Real implementation starts Week 2.
"""


class CodeFixAgent:
    """Given a task record, produces a patch that (hopefully) resolves it."""

    def __init__(self, model: str, max_iterations: int = 6):
        self.model = model
        self.max_iterations = max_iterations

    def run(self, task: dict) -> dict:
        """
        Args:
            task: a task record matching data/tasks/schema.json

        Returns:
            dict with at least: task_id, resolved (bool), iterations (int),
            patch (str), tokens_used (int), latency_seconds (float)
        """
        raise NotImplementedError("Implemented in Week 2-3")
