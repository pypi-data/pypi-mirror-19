# GIT utilities

from git import Repo


def repo(base_dir=None):
    """Return a repository object."""
    import os
    base_dir = base_dir or os.getcwd()
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


def diff_paths(diff):
    diffs = {
        'added': [p.b_path for p in diff.iter_change_type('A')],
        'deleted': [p.a_path for p in diff.iter_change_type('D')],
        'renamed': [p.b_path for p in diff.iter_change_type('R')],
        'modified': [p.b_path for p in diff.iter_change_type('M')],
    }
    all_paths = []
    for i in ['added', 'deleted', 'renamed', 'modified']:
        all_paths.extend(diffs[i])
    diffs['all'] = all_paths
    return diffs
