"""Tool: read a file from the sandboxed target repo."""


def read_file(repo_path: str, file_path: str) -> str:
    """
    Args:
        repo_path: absolute path to the sandboxed repo checkout
        file_path: path relative to repo_path

    Returns:
        File contents as a string, or a clear error string if not found.
    """
    raise NotImplementedError("Implemented in Week 2")
