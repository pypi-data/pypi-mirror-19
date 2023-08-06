from __future__ import print_function  # NOQA

import logging

log = logging.getLogger(__name__)


def main():
    args = parser().parse_args()
    logging.basicConfig(level=args.log_level)
    if args.phase:
        exec_phase(args.phase, args.verbose, args.commit, args.circleci)


def parser():
    import argparse
    parser = argparse.ArgumentParser(description='Menhir monorepo build tool.')
    parser.add_argument("--commit")
    parser.add_argument("-v", "--verbose", default=False,
                        action='store_const', const=True)
    parser.add_argument("--circleci", default=False,
                        action='store_const', const=True)
    parser.add_argument("--log-level", default='WARNING')
    subparsers = parser.add_subparsers(help='sub-commands')
    parser_exec = subparsers.add_parser('exec', help='execute a build phase')
    parser_exec.add_argument('phase')
    return parser


def exec_phase(phase, verbose, commit, circleci):
    import sys
    from menhir import (
        apply_phase,
        update_for_changed_files,
        root_config,
    )

    config = root_config()

    project_infos = config['project_infos']
    dependencies = config['dependencies']
    root_projects = config['root_projects']
    git_prefix = config['git_prefix']

    if verbose:
        print_project_infos(project_infos)
        print_dependencies(dependencies)
        print_git_info(config['git_root'], git_prefix)

    files = changed_files(config, circleci, commit, verbose)
    if verbose:
        print_changed_files(files)

    changed_projects = update_for_changed_files(
        dependencies, project_infos, root_projects, git_prefix, files
    )
    if verbose:
        print_changed_projects(changed_projects)
        print_project_info(project_infos)

    res = apply_phase(
        dependencies,
        project_infos,
        root_projects,
        phase,
        verbose=verbose,
    )

    if res.get('failed'):
        print('Build phase "%s" failed' % phase, file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)


def print_project_infos(project_infos):
    print('Project dirs:')
    for p in project_infos:
        print('    ', p)


def print_dependencies(dependencies):
    print('Dependencies Graph:')
    for p in dependencies.items():
        print('    ', p)


def print_git_info(git_root, git_prefix):
    print("Git root:", git_root)
    print("Git prefix:", git_prefix)


def print_changed_files(files):
    print('Changed files')
    for i in files:
        print('  ', i)


def print_changed_projects(changed_projects):
    print('Changed projects')
    for i in changed_projects:
        print('  ', i)


def print_project_info(project_infos):
    print('Project info')
    for k, v in project_infos.items():
        v = v.copy()
        v.pop('tools')
        print('  ', k, v)


def changed_files(config, circleci, commit, verbose):
    from menhir.gitutils import changed_files, repo, uncommited_files
    git_repo = repo(config['git_root'])
    uncommited = uncommited_files(git_repo)['all']
    if uncommited and not commit:
        files = uncommited
        if verbose:
            print("Uncommited files")
    else:
        from_commit, to_commit = commit_range(
            commit, circleci, config['git_root'], verbose
        )
        if verbose:
            print("Commit range: %s..%s" % (from_commit, to_commit))

        files = changed_files(from_commit, to_commit)['all']

    return files


def commit_range(commit_arg, circleci, root, verbose):
    import os
    from menhir.gitutils import head_commit, repo
    if commit_arg:
        return commits_from_range(commit_arg)
    if circleci:
        compare_url = os.getenv('CIRCLE_COMPARE_URL')
        log.debug('Deriving commit range from %s', compare_url)
        if compare_url:
            commit_range = compare_url.rsplit('/', maxsplit=1)[1]
            return commits_from_range(commit_range)
        sha = os.getenv('CIRCLE_SHA1')
        return sha+"^", sha

    r = repo(root)
    commit = head_commit(r)
    return str(commit)+"^", str(commit)


def commits_from_range(commit_range):
    log.debug('commits_from_range: %s', commit_range)
    commits = commit_range.split('..')
    if len(commits) == 2:
        from_commit = commits[0].replace('.', '')
        to_commit = commits[1].replace('.', '')
        log.debug('commits_from_range: from %s to %s', from_commit, to_commit)
        return from_commit, to_commit
    log.debug('commits_from_range: single commit %s', commit_range)
    return commit_range+"^", commit_range
