import os
import networkx as nx
from .file_io import read_file, write_summary

def process_file_pipeline(filename: str) -> str:
    """
    Process an uploaded file in three steps:
      1. read
      2. count
      3. write
    The graph is built at runtime so we never pull in Pandas.
    """
    # Build graph
    G = nx.DiGraph()
    G.add_edge("read", "count")
    G.add_edge("count", "write")

    # Paths
    base_dir    = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    uploads_dir = os.path.join(base_dir, 'uploads')
    data: dict[str, any] = {}

    # Execute in topological order
    for step in nx.topological_sort(G):
        if step == "read":
            path = os.path.join(uploads_dir, filename)
            data['lines'] = read_file(path)

        elif step == "count":
            lines = data.get('lines', [])
            data['summary'] = (
                f"Processed '{filename}':\n"
                f"- Lines: {len(lines)}\n"
                f"- Words: {sum(len(line.split()) for line in lines)}\n"
            )

        elif step == "write":
            summary = data.get('summary', '')
            out_path = os.path.join(uploads_dir, f"{filename}.summary.txt")
            write_summary(out_path, summary)

    return data.get('summary', '')


