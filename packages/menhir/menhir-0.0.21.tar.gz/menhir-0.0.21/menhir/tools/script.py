"""
Tool that invokes the named script from a project local bin directory.

The scripts are called with the project path as the first argument.
"""

import logging

import menhir.tool as mtool
from menhir.tool_utils import OK, FAIL, NOTHING_TO_DO, tool_env, working_dir

log = logging.getLogger(__name__)


class Script():
    pass


def tool():
    return Script()


@mtool.name.register(Script)
def name(arg):
    return "script"


@mtool.is_using_tool.register(Script)
def is_using_tool(tool, path):
    from os.path import exists, join
    return exists(join(path, 'bin'))


@mtool.dependencies.register(Script)
def dependencies(tool, path):
    return []


@mtool.add_arg_parser.register(Script)
def add_arg_parser(tool, parser):
    parser.description = "Invoke scripts from project bin sub-directory"
    parser.add_argument(
        'script_name',
        metavar='script-name',
        help='script to invoke from bin directory'
    )
    parser.add_argument('args', nargs='*', help='script arguments')


@mtool.execute_build_phase.register(Script)
def execute_build_phase(
        tool, path, info, args,
        only_if_changed=False,
        verbose=False,
):
    """Execute a build phase."""
    import os
    import os.path
    import subprocess

    with working_dir(path):
        script_file = os.path.join('bin', args.script_name)
        if os.access(script_file, os.X_OK):
            if verbose:
                print('Running script bin/%s in %s' % (args.script_name, path))

            if only_if_changed and not (
                    info.get('changed') or
                    info.get('changed_dependents')
            ):
                return OK

            env = tool_env()
            if info.get('changed'):
                env['MENHIR_CHANGED'] = "1"
            if info.get('changed_dependents'):
                env['MENHIR_CHANGED_DEPENDENTS'] = "1"
            if info.get('changed_dependees'):
                env['MENHIR_CHANGED_DEPENDEES'] = "1"

            result = subprocess.call(
                [script_file] + args.args,
                env=env,
            )
            log.debug('Script %s result: %s', args.script_name, result)
            if result:
                return FAIL
            return OK
        else:
            log.debug('No script for build phase %s', args.script_name)
            return NOTHING_TO_DO
