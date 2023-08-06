"""
Pyenv based tool for menhir.

The ``pyenv`` tool provides the ``virtualenv`` target to create a
virtualenv for each of the repository's projects.  The virtualenv is
loaded with all the project's dependencies as specified in
``requirements*.txt``.
"""
import logging

import menhir.tool as mtool
from menhir.tool_utils import OK, FAIL, NOTHING_TO_DO, tool_env, working_dir

log = logging.getLogger(__name__)


class Pyenv():
    pass


def tool():
    return Pyenv()


@mtool.name.register(Pyenv)
def name(arg):
    return "pyenv"


@mtool.is_using_tool.register(Pyenv)
def is_using_tool(tool, path):
    from os.path import exists, join
    path = join(path, 'requirements.txt')
    return exists(path)


@mtool.dependencies.register(Pyenv)
def dependencies(tool, path):
    return []


@mtool.add_arg_parser.register(Pyenv)
def add_arg_parser(tool, parser):
    parser.description = "Manage project specific pyenv virtualenvs"
    parsers = parser.add_subparsers(help="pyenv commands", dest='phase')
    parsers.add_parser(
        'virtualenv',
        help='Build a pyenv virtualenv with the projects dependencies'
    )


def run(cmd, *args, **kwargs):
    import subprocess
    res = subprocess.call(cmd, *args, **kwargs)
    if res:
        return False, FAIL
    return True, OK


@mtool.execute_build_phase.register(Pyenv)
def execute_build_phase(
        tool, path, info, args,
        only_if_changed=False,
        verbose=False,
):
    """Execute a build phase."""
    import subprocess
    from menhir.tool_utils import package_script
    from menhir.project import project_name_for_dir

    if args.phase == 'virtualenv':
        if (
                info.get('changed') or
                info.get('changed_dependents') or
                (info.get('changed_dependees') and not only_if_changed)
        ):
            if verbose:
                print('Running pyenv requirements in %s' % path)
            log.debug('pyenv requirements in %s', path)

            env = tool_env()

            with package_script("/tools/pyenv/requirements.sh") as f:
                with working_dir(path):
                    res = subprocess.call(
                        [f.name, path, project_name_for_dir(path)],
                        env=env,
                    )
                    if res:
                        return FAIL
                    return OK
        else:
            if verbose:
                print('Not running pyenv requirements in %s' % path)
            log.debug('not running pyenv requirements in %s', path)
            return OK
    else:
        return NOTHING_TO_DO
