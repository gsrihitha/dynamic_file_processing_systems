import os
import networkx as nx # type: ignore

from .file_io import read_file, write_summary # type: ignore

# 1️⃣ Build a simple directed workflow: read → count → write
WORKFLOW = nx.DiGraph()
WORKFLOW.add_edge("read", "count")
WORKFLOW.add_edge("count", "write")

def process_with_graph(filename):
    """
    Process a file by:
      1. reading its lines,
      2. counting lines & words,
      3. writing a summary file,
      and returning the summary text.
    """
    # Locate the uploads directory (sibling to this app/ folder)
    base = os.path.dirname(__file__)
    uploads_dir = os.path.abspath(os.path.join(base, '..', 'uploads'))

    data = {}
    input_path = os.path.join(uploads_dir, filename)

    # Execute steps in topological (dependency) order
    for step in nx.topological_sort(WORKFLOW):
        if step == "read":
            data["lines"] = read_file(input_path)

        elif step == "count":
            lines = data.get("lines", [])
            line_count = len(lines)
            word_count = sum(len(line.split()) for line in lines)
            data["summary"] = (
                f"Processed '{filename}':\n"
                f"- Lines: {line_count}\n"
                f"- Words: {word_count}\n"
            )

        elif step == "write":
            summary_path = os.path.join(uploads_dir, f"{filename}.summary.txt")
            write_summary(summary_path, data["summary"])

    return data.get("summary", "")




# # app/processing.py

# import os
# import networkx as nx # type: ignore

# # Import your file I/O helpers
# from .file_io import read_file, write_summary # type: ignore

# # Build the workflow graph once at import time
# WORKFLOW = nx.DiGraph()
# WORKFLOW.add_edge("read", "count")
# WORKFLOW.add_edge("count", "write")

# def process_with_graph(filename):
#     """
#     Process the uploaded file through a 3-step workflow:
#       1) read  - load all lines
#       2) count - compute line & word counts
#       3) write - emit a summary file
#     Returns the summary string.
#     """
#     # 1. Locate the uploads directory relative to this script
#     base_dir = os.path.dirname(__file__)
#     uploads_dir = os.path.abspath(os.path.join(base_dir, "../uploads"))

#     # 2. Build full path to the input file
#     input_path = os.path.join(uploads_dir, filename)

#     # 3. Walk the workflow in topological order
#     data = {}
#     for step in nx.topological_sort(WORKFLOW):
#         if step == "read":
#             # Read the file’s lines into data['lines']
#             data["lines"] = read_file(input_path)

#         elif step == "count":
#             # Count lines and words, store formatted summary in data['summary']
#             lines = data.get("lines", [])
#             line_count = len(lines)
#             word_count = sum(len(line.split()) for line in lines)
#             data["summary"] = (
#                 f"Processed '{filename}':\n"
#                 f"- Lines: {line_count}\n"
#                 f"- Words: {word_count}\n"
#             )

#         elif step == "write":
#             # Write the summary out to uploads/<filename>.summary.txt
#             summary_path = os.path.join(uploads_dir, f"{filename}.summary.txt")
#             write_summary(summary_path, data["summary"])

#     # 4. Return the summary text for immediate display
#     return data.get("summary", "")
