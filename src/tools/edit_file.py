"""
Tool: apply a constrained edit to a file in the sandboxed repo.

Deliberately narrow interface (find/replace on an exact string match,
not free-text patching) so agent edits stay interpretable and easy to
log/diff -- mirrors the "Agent-Computer Interface" idea from SWE-agent.
"""


def edit_file(repo_path: str, file_path: str, old_str: str, new_str: str) -> dict:
    """
    Args:
        repo_path: absolute path to the sandboxed repo checkout
        file_path: path relative to repo_path
        old_str: exact existing text to replace (must match uniquely)
        new_str: replacement text

    Returns:
        {"success": bool, "error": str | None} -- error set if old_str
        wasn't found or matched more than once.
    """
    raise NotImplementedError("Implemented in Week 2")
