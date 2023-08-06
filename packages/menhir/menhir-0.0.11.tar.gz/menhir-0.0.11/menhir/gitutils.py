# GIT utilities

from git import Repo


def find_root():
    """Based on the current directory, look for a .menhir_root.yaml file."""
    from os.path import dirname
    from .fileutils import find_file_in_parents
    root = find_file_in_parents(".git")
    if root is None:
        raise FileNotFoundError(
            'No git repository in parent directories',
            ".git"
        )
    return dirname(root)


def repo(base_dir=None):
    """Return a repository object."""
    base_dir = base_dir or find_root()
    return Repo(base_dir)


def commit(repo, commitish):
    """Return a commit object."""
    return repo.commit(commitish)


def head_commit(repo):
    """Return a commit object."""
    return repo.head.commit


def diff(start, end):
    """Diff for the commit range."""
    return diff_paths(start.diff(end))


def dirty_files(repo):
    return diff_paths(repo.index.diff(None))


def staged_files(repo):
    return diff_paths(repo.index.diff("HEAD"))


def uncommited_files(repo):
    dirty = repo.index.diff(None)
    dirty.extend(repo.index.diff("HEAD"))
    return diff_paths(dirty)


def diff_paths(diff):
    rpaths = [p.a_path for p in diff.iter_change_type('R')]
    rpaths.extend([p.b_path for p in diff.iter_change_type('R')])

    diffs = {
        'added': [p.b_path for p in diff.iter_change_type('A')],
        'deleted': [p.a_path for p in diff.iter_change_type('D')],
        'renamed': rpaths,
        'modified': [p.b_path for p in diff.iter_change_type('M')],
    }
    all_paths = []
    for i in ['added', 'deleted', 'renamed', 'modified']:
        all_paths.extend(diffs[i])
    diffs['all'] = all_paths
    return diffs


def changed_files(start, end):
    from menhir import gitutils
    repo = gitutils.repo()
    start_commit = gitutils.commit(repo, start)
    end_commit = gitutils.commit(repo, end)
    changed_files = gitutils.diff(start_commit, end_commit)
    return changed_files
