# Setup.py based tool for menhir
import re

import menhir.tool as mtool

DEP_PATTERN = re.compile('file:(.*)#egg=.*')


class SetupPy():
    pass


def tool():
    return SetupPy()


@mtool.name.register(SetupPy)
def name(arg):
    return "setup_py"


@mtool.is_using_tool.register(SetupPy)
def is_using_tool(tool, path):
    from os.path import exists, join
    return exists(join(path, 'setup.py'))


@mtool.dependencies.register(SetupPy)
def dependencies(tool, path):
    from os.path import join, normpath
    requirements_path = join(path, 'requirements.txt')
    requirements, dependency_links = read_requirements(requirements_path)
    return [
        normpath(join(path, DEP_PATTERN.match(l).group(1)))
        for l in dependency_links
        if l.startswith('file:')
    ]


def read_requirements(path):
    with open(path, 'r') as f:
        return process_requirements(f)


def process_requirements(f):
    requirements = []
    dependency_links = []
    for line in f.read().split():
        if '#egg=' in line:
            package_name = line.rsplit('#egg=', 1).pop()
            requirements.append(package_name)
            dependency_links.append(line)
        else:
            requirements.append(line)
    return requirements, dependency_links


@mtool.execute_build_phase.register(SetupPy)
def execute_build_phase(tool, path, phase_name):
    """Execute a build phase."""
    return {
        'status': 'nothing_to_do'
    }
