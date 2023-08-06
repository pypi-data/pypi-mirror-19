# pyenv based tool for menhir
import logging

import menhir.tool as mtool
from menhir.tool_utils import OK, FAIL, NOTHING_TO_DO, working_dir

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


def run(cmd, *args, **kwargs):
    import subprocess
    res = subprocess.call(cmd, *args, **kwargs)
    if res:
        return False, FAIL
    return True, OK


@mtool.execute_build_phase.register(Pyenv)
def execute_build_phase(
        tool, path, info, phase_name, args,
        only_if_changed=False,
        verbose=False,
):
    """Execute a build phase."""
    from os.path import basename
    import subprocess
    from menhir.tool_utils import package_script

    if phase_name == 'requirements':
        if (
                info.get('changed') or
                info.get('changed_dependents') or
                (info.get('changed_dependees') and not only_if_changed)
        ):
            if verbose:
                print('Running pyenv requirements in %s' % path)
            log.debug('pyenv requirements in %s', path)
            with package_script("/tools/pyenv/requirements.sh") as f:
                with working_dir(path):
                    res = subprocess.call([f.name, path, basename(path)])
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
