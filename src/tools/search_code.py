"""Tool: search across the target repo for a pattern (grep-style)."""


def search_code(repo_path: str, query: str, max_results: int = 20) -> list[dict]:
    """
    Args:
        repo_path: absolute path to the sandboxed repo checkout
        query: text or regex pattern to search for
        max_results: cap on returned matches

    Returns:
        List of {"file": str, "line": int, "text": str} matches.
    """
    raise NotImplementedError("Implemented in Week 2")
