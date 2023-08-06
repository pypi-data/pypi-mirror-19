# pytest based tool for menhir
import menhir.tool as mtool


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
            data = file.readlines()
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
        owd = os.getcwd()
        try:
            os.chdir(path)
            res = subprocess.run(['pytest'])
            if res.returncode:
                return {
                    'status': 'fail'
                }
            return {
                'status': 'ok',
            }
        finally:
            os.chdir(owd)
    else:
        return {
            'status': 'nothing_to_do'
        }
