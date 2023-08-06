# Setup.py based tool for menhir
from __future__ import print_function  # NOQA

import logging
import re
import sys

import menhir.tool as mtool
from menhir.tool_utils import OK, FAIL, NOTHING_TO_DO, tool_env, working_dir

DEP_PATTERN = re.compile('file:(.*)#egg=.*')

log = logging.getLogger(__name__)


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
    log.debug('setup.py dependencies in %s', path)
    try:
        requirements_path = join(path, 'requirements.txt')
        requirements, dependency_links = read_requirements(requirements_path)
        return [
            normpath(join(path, DEP_PATTERN.match(l).group(1)))
            for l in dependency_links
            if l.startswith('file:')
        ]
    except:
        print('Failed to infer dependencies in for setup_py %s' % path,
              file=sys.stderr)
        raise


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
def execute_build_phase(
        tool, path, info, phase_name, args,
        only_if_changed=False,
        verbose=False,
):
    """Execute a build phase."""
    if phase_name == 'sdist' and (
            info.get('changed') or info.get('changed_dependents')
    ):
        if verbose:
            print('Running sdist in %s' % path)
        with working_dir(path):
            return sdist(path)
    elif phase_name == 'lambda-package' and (
            info.get('changed') or info.get('changed_dependents')
    ):
        if verbose:
            print('Running lambda-package in %s' % path)
        with working_dir(path):
            return lambda_package(path)
    return NOTHING_TO_DO


def sdist(pdir):
    """Package python project at path, including relative requirements."""
    import os.path as path
    import shutil
    import subprocess
    from os import mkdir, walk

    log.debug('Running sdist in %s', pdir)
    res = subprocess.call(["python", "setup.py", "sdist"], env=tool_env())
    if res:
        return FAIL

    dist_reqs = path.join(pdir, 'dist-requirements')
    if not path.exists(dist_reqs):
        mkdir(dist_reqs)

    reqs = "requirements.txt"
    if path.exists(reqs):
        with open(reqs) as f:
            for line in f.read().splitlines():
                match = DEP_PATTERN.match(line)
                if match:
                    dir = match.group(1)
                    with working_dir(dir):
                        log.debug('Running sdist for %s', dir)
                        res = subprocess.call(
                            ["python", "setup.py", "sdist"],
                            env=tool_env(),
                        )
                        if res:
                            return False
                    for root, dirs, files in walk(path.join(dir, 'dist')):
                        for f in files:
                            shutil.copyfile(
                                path.join(root, f),
                                path.join(dist_reqs, f))

    log.debug('Completed sdist in %s', pdir)
    return OK


def lambda_package(path):
    """Package python project at path, including relative requirements.

    Only packages projects that contain a .lambda-package file.
    """
    import subprocess
    from os.path import exists
    from menhir.tool_utils import package_script

    marker = '.lambda-package'
    if not exists(marker):
        print('Not a lambda project (no %s)' % marker)
        return NOTHING_TO_DO

    with package_script("/tools/setup_py/lambda-package.sh") as f:
        res = subprocess.call([f.name], env=tool_env())
        if res:
            return FAIL
    return OK
