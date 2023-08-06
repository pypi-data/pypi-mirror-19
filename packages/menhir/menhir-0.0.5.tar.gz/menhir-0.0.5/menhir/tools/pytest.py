# pytest based tool for menhir
import logging

import menhir.tool as mtool
from menhir.tool_utils import OK, FAIL, NOTHING_TO_DO

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
def execute_build_phase(tool, path, phase_name):
    """Execute a build phase."""
    import os
    import subprocess
    if phase_name == 'test':
        log.debug('pytest: test %s', path)
        owd = os.getcwd()
        try:
            os.chdir(path)
            res = subprocess.call(['pytest'])
            if res:
                return FAIL
            return OK
        finally:
            os.chdir(owd)
    else:
        return NOTHING_TO_DO
