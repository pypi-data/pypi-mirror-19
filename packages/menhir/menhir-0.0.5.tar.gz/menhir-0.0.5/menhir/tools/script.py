# Tool that invokes a script in a project local bin directory.
#
# The scripts are called with the project path as the first argument.
import logging

import menhir.tool as mtool

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
def execute_build_phase(tool, path, phase_name):
    """Execute a build phase."""
    import os
    import os.path
    import subprocess

    script_file = os.path.join(path, 'bin', phase_name)
    if os.access(script_file, os.X_OK):
        result = subprocess.run([script_file, path])
        if result.returncode:
            return {
                'status': 'fail',
            }
        return {
            'status': 'ok',
        }
    else:
        log.debug('No script for build phase %s', phase_name)
        return {
            'status': 'nothing_to_do'
        }
