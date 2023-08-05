import logging

log = logging.getLogger(__name__)


def main():
    import sys
    args = parser().parse_args()
    logging.basicConfig(level=args.log_level)
    if args.phase:
        from menhir import build_order, execute_phase, root_config
        from_commit, to_commit = commit_range(
            args.commit, args.circleci, args.verbose
        )
        if args.verbose:
            print("Commit range: %s..%s" % (from_commit, to_commit))
        config = root_config()
        project_dirs = config['project_dirs']
        dependencies = config['dependencies']
        root_projects = config['root_projects']
        g = build_order(
            dependencies, project_dirs, root_projects,
            from_commit, to_commit,
        )
        if args.verbose:
            print('Build phase:', args.phase)
        res = execute_phase(g, config['tool_impls'], args.phase)
        if res['status'] == 'fail':
            print('Build phase "%s" failed' % args.phase, file=sys.stderr)
            sys.exit(1)
        else:
            sys.exit(0)


def parser():
    import argparse
    parser = argparse.ArgumentParser(description='Menhir monorepo build tool.')
    parser.add_argument("--commit")
    parser.add_argument("-v", "--verbose", default=False,
                        action='store_const', const=True)
    parser.add_argument("--circleci", default=False,
                        action='store_const', const=True)
    parser.add_argument("--log_level", default='WARNING')
    subparsers = parser.add_subparsers(help='sub-commands')
    parser_exec = subparsers.add_parser('exec', help='execute a build phase')
    parser_exec.add_argument('phase')
    return parser


def commit_range(commit_arg, circleci, verbose):
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
    commit = head_commit(repo())
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
