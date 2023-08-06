"""
The pytest tool invokes pytest based tests.
"""
import logging

import menhir.tool as mtool
from menhir.tool_utils import (
    OK,
    FAIL,
    NOTHING_TO_DO,
    package_script,
    tool_env,
    working_dir,
)

log = logging.getLogger(__name__)


class Pytest():
    pass


def tool():
    return Pytest()


@mtool.name.register(Pytest)
def name(arg):
    return "pytest"


@mtool.is_using_tool.register(Pytest)
def is_using_tool(tool, path):
    from os.path import exists, join
    path = join(path, 'setup.cfg')
    if exists(path):
        with open(path, "r") as file:
            data = file.read()
            return 'pytest' in data


@mtool.dependencies.register(Pytest)
def dependencies(tool, path):
    return []


@mtool.add_arg_parser.register(Pytest)
def add_arg_parser(tool, parser):
    parser.description = "Invoke pytest based tests"
    parser.add_argument('args', nargs='*', help='pytest arguments')


@mtool.execute_build_phase.register(Pytest)
def execute_build_phase(
        tool, path, info, args,
        only_if_changed=False,
        verbose=False,
):
    """Execute a build phase."""
    import subprocess
    from menhir.project import project_name_for_dir

    log.info('pytest: %s %s %s', path, info, args)
    if info.get('changed') or info.get('changed_dependents'):
        if verbose:
            print('Running pytest in %s' % path)
        project_name = project_name_for_dir(path)
        env = tool_env()
        env['MENHIR_PROJECT'] = project_name
        with package_script("/tools/pytest/test.sh") as f:
            with working_dir(path):
                res = subprocess.call([f.name] + args.args, env=env)
                if res:
                    return FAIL
                return OK
    else:
        return NOTHING_TO_DO
