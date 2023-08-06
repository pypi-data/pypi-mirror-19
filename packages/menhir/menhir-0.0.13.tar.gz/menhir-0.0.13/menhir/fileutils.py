def find_file_in_parents(file_name, base_dir=None):
    """From base_dir, look for a file in parent directories.

    Returns the full oath to the file found.

    `base_dir` defaults to the current directory.
    """
    import os
    import os.path

    dir = base_dir or os.getcwd()
    while True:
        f = os.path.join(dir, file_name)
        if os.path.exists(f):
            return f
        else:
            parent_dir = os.path.dirname(dir)
            if dir == parent_dir:  # if dir is root dir
                return None
            else:
                dir = parent_dir
