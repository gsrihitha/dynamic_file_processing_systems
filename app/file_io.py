import os

def read_file(path: str) -> list[str]:
    """Read all lines from a text file; return [] on error."""
    try:
        with open(path, 'r') as f:
            return f.readlines()
    except Exception:
        return []

def write_summary(path: str, summary: str) -> None:
    """Write summary text to a file, creating directories if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(summary)




