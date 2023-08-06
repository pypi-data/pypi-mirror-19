# Tool that invokes a script in a project local bin directory.
#
# The scripts are called with the project path as the first argument.
import logging

import menhir.tool as mtool
from menhir.tool_utils import OK, FAIL, NOTHING_TO_DO

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


@mtool.execute_build_phase.register(Script)
def execute_build_phase(tool, path, info, phase_name, verbose=False):
    """Execute a build phase."""
    import os
    import os.path
    import subprocess

    script_file = os.path.join(path, 'bin', phase_name)
    if os.access(script_file, os.X_OK):
        if verbose:
            print('Running script bin/%s in %s' % (phase_name, path))
        result = subprocess.call(
            [
                script_file,
                path,
                "1" if info.get('changed') else "0",
                "1" if info.get('changed_dependents') else "0",
                "1" if info.get('changed_dependees') else "0",
            ])
        log.debug('Script %s result: %s', phase_name, result)
        if result:
            return FAIL
        return OK
    else:
        log.debug('No script for build phase %s', phase_name)
        return NOTHING_TO_DO
