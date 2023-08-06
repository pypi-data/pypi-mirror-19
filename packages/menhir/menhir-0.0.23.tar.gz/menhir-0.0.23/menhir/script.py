"""Menhir command line script.

The script is the main user interface for menhir.
"""
from __future__ import print_function  # NOQA

import logging

from menhir import __version__
from menhir.config import default_root_config, parse_root_config
from menhir.utils import multi, method


log = logging.getLogger(__name__)


def main():
    from menhir import root_config
    config = root_config()
    args = parser(config).parse_args()

    if args.verbose and args.log_level != 'DEBUG':
        args.log_level = 'INFO'
    logging.basicConfig(level=args.log_level)

    write_version()
    if args.version:
        print('Menhir %s' % __version__)
    elif args.menhir_command:
        command(config, args,)


def parser(config=parse_root_config(default_root_config())):
    import argparse
    parser = argparse.ArgumentParser(description="""
Menhir is an extensible build tool, that recognises dependencies
between sub-projects in a repository.
""")
    parser.add_argument(
        "--version",
        default=False,
        action='store_const',
        const=True,
        help="Print menhir version and exit",
    )
    parser.add_argument("--commit", help="""
Specify commit range to work on.
This can be specifed as a single commit or a commit range, e.g.
3f8e5bb, 3f8e5bb..cfa3762, 3f8e5bb^..head.
""")
    parser.add_argument(
        "-v", "--verbose",
        default=False,
        action='store_const', const=True,
        help='Provide verbose output (shortcut for log-levl INFO)',
    )
    parser.add_argument("--circleci", default=False,
                        action='store_const', const=True)
    parser.add_argument(
        "--log-level", default='WARNING',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="Set the log level to output"
    )

    subparsers = parser.add_subparsers(
        help='sub-commands',
        dest='menhir_command'
    )

    parser_exec = subparsers.add_parser(
        'info',
        help="Print project information")

    parser_exec = subparsers.add_parser('exec', help='execute a build tool')
    parser_exec.add_argument("--only-if-changed", default=False,
                             action='store_const', const=True)

    tool_parsers = parser_exec.add_subparsers(help='tools', dest='tool')
    for tool_name, tool in config['tools'].items():
        tool_parser = tool_parsers.add_parser(
            tool_name,
        )
        tool.add_arg_parser(tool_parser)

    return parser


@multi
def command(root_config, args):
    return args.menhir_command


@method(command, 'info')
def info(root_config, args):
    from pprint import pprint
    from menhir import describe_repository
    config = describe_repository(root_config)
    pprint(config)


@method(command, 'exec')
def exec_tool(root_config, args):
    import sys
    from menhir import (
        apply_tool,
        describe_repository,
        update_for_changed_files,
    )

    config = describe_repository(root_config)
    tool = root_config['tools'][args.tool]

    project_infos = config['project_infos']
    dependencies = config['dependencies']
    root_projects = config['root_projects']
    git_prefix = config['git_prefix']

    files = changed_files(config, args.circleci, args.commit)
    update_for_changed_files(
        dependencies, project_infos, root_projects, git_prefix, files
    )

    res = apply_tool(
        dependencies,
        project_infos,
        root_projects,
        tool,
        args,
    )

    if res.get('failed'):
        print('Build tool "%s" failed' % args.tool, file=sys.stderr)
        sys.exit(1)


def changed_files(config, circleci, commit):
    from menhir.gitutils import changed_files, repo, uncommited_files
    git_repo = repo(config['git_root'])
    uncommited = uncommited_files(git_repo)['all']
    if uncommited and not commit:
        files = uncommited
        log.info("Uncommited files")
    else:
        from_commit, to_commit = commit_range(
            commit, circleci, config['git_root']
        )
        log.info("Commit range: %s..%s", from_commit, to_commit)

        files = changed_files(from_commit, to_commit)['all']

    return files


def commit_range(commit_arg, circleci, root):
    import os
    from menhir.gitutils import head_commit, repo
    if commit_arg:
        return commits_from_range(commit_arg)
    if circleci:
        compare_url = os.getenv('CIRCLE_COMPARE_URL')
        log.debug('Deriving commit range from %s', compare_url)
        if compare_url:
            commit_range = compare_url.rsplit('/', 1)[1]
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


def write_version():
    from menhir import __version__
    with open('.menhir-version', 'w+') as f:
        f.write(__version__)
