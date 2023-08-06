# pytest based tool for menhir
import logging

import menhir.tool as mtool
from menhir.tool_utils import (
    OK,
    FAIL,
    NOTHING_TO_DO,
    package_script,
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


@mtool.execute_build_phase.register(Pytest)
def execute_build_phase(
        tool, path, info, phase_name, args,
        only_if_changed=False,
        verbose=False,
):
    """Execute a build phase."""
    import subprocess
    log.info('pytest: %s %s', phase_name, info)
    if phase_name == 'test' and (
            info.get('changed') or info.get('changed_dependents')
    ):
        if verbose:
            print('Running pytest in %s' % path)
        with package_script("/tools/pytest/test.sh") as f:
            with working_dir(path):
                res = subprocess.call([f.name] + args)
                if res:
                    return FAIL
                return OK
    else:
        return NOTHING_TO_DO
