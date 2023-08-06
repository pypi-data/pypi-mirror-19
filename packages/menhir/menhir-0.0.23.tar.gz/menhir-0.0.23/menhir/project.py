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


@lru_cache()
def sha():
    from menhir.gitutils import head_commit, sha
    return sha(head_commit(repo()))


@lru_cache()
def branch():
    from menhir.gitutils import branch
    return branch(repo())


@lru_cache()
def repo():
    from menhir.gitutils import repo
    return repo()


def image(info):
    repo = info.get('config', {}).get('docker', {}).get('repository')
    if repo:
        return '%s/%s:%s' % (
            repo,
            project_name(),
            sha()
        )
