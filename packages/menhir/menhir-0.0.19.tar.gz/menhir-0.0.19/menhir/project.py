try:
    from functools import lru_cache
except:
    from functools32 import lru_cache


def project_name():
    """Return the name of the project in the current directory."""
    from os import getcwd
    return project_name_for_dir(getcwd())


@lru_cache()
def project_name_for_dir(path):
    """Return the name of the project in the current directory."""
    from os.path import abspath, basename, exists, join
    fname = join(path, '.project-name')
    if exists(fname):
        with open(fname, 'r') as f:
            return f.read().strip()
    return basename(abspath(path))
