def read_file(path):
    """Read and return all lines from a file."""
    try:
        # Open the file at `path` in read mode with UTF-8 encoding,
        # ensuring it’s automatically closed afterwards
        with open(path, 'r', encoding='utf-8') as f:
            # Read all lines into a list of strings (one per line)
            return f.readlines()
    except OSError as e:
        # If anything goes wrong (e.g. missing file, permissions), log the error
        print(f"Error reading {path}: {e}")
        # Return an empty list so calling code can continue safely
        return []

def write_summary(path, text):
    """Write summary text to a new file."""
    try:
        # Open (or create) the file at `path` in write mode with UTF-8 encoding,
        # automatically closing it when done
        with open(path, 'w', encoding='utf-8') as f:
            # Write the entire `summary` string into the file
            f.write(text)
    except OSError as e:
        # If writing fails (e.g. disk full, bad path), log the error
        print(f"Error writing {path}: {e}")


if __name__ == '__main__': # Ensures this block only runs if you execute the script directly
    lines = read_file('../uploads/example.txt') # calls read files that is on the upload , and stores the returnes list into the lines
    summary = f"File has {len(lines)} lines.\n" # counts the number of lines read and prints
    write_summary('../uploads/summary.txt', summary) # Saves the summary text into a new file summary.txt, overwrites if already exists
    print("Done.") # A message to confirm that the execution has finished

    
