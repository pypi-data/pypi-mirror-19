# Utilities for use in tools
from contextlib import contextmanager

OK = {
    'status': 'ok'
}

FAIL = {
    'status': 'fail'
}

NOTHING_TO_DO = {
    'status': 'nothing_to_do'
}


@contextmanager
def package_script(resource_path, resource_package="menhir"):
    """Execute a block of code with the given script from the package.

    Yields a file like object that is the script written onto the filesystem.
    """
    import tempfile
    import pkg_resources
    import stat
    from os import chmod, remove

    script = pkg_resources.resource_string(resource_package, resource_path)
    fname = None
    try:
        with tempfile.NamedTemporaryFile("wb", delete=False) as f:
            fname = f.name
            f.write(script)
        chmod(fname, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        yield f
    finally:
        remove(fname)


@contextmanager
def working_dir(path):
    """Execute a block of code within the given working dir."""
    import os
    dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(dir)


def tool_env():
    """Return the default tool environment dict."""
    import os
    import os.path
    default_pyenv_root = os.path.join(os.getenv("HOME"), ".pyenv")
    env = {
        "HOME": os.getenv("HOME"),
        "PATH": os.getenv("PATH"),
        "PYENV_ROOT": os.getenv("PYENV_ROOT", default_pyenv_root),
    }
    v = os.getenv("AWS_DEFAULT_REGION")
    if v:
        env["AWS_DEFAULT_REGION"] = v
    return env
