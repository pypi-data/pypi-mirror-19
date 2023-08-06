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
    from menhir import build_order, execute_phase, root_config
    from menhir.gitutils import changed_files
    config = root_config()

    project_dirs = config['project_dirs']
    if verbose:
        print('Project dirs:')
        for p in project_dirs:
            print('    ', p)

        print('Dependencies Graph:')
        for p in config['dependencies'].items():
            print('    ', p)

    if verbose:
        print("Git root:", config['git_root'])
        print("Git prefix:", config['git_prefix'])

    from_commit, to_commit = commit_range(
        commit, circleci, config['git_root'], verbose
    )
    if verbose:
        print("Commit range: %s..%s" % (from_commit, to_commit))

    files = changed_files(from_commit, to_commit)['all']

    g = build_order(
        config['dependencies'],
        config['project_dirs'],
        config['root_projects'],
        files,
        config['git_prefix'],
    )

    if verbose:
        print('build_order:', g)
        print('Build phase:', phase)
    res = execute_phase(g, config['project_dirs'], phase)

    if res['status'] == 'fail':
        print('Build phase "%s" failed' % phase, file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)


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
