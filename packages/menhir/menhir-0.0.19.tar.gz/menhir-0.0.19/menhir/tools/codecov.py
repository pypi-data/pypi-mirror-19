# codecov based tool for menhir
import logging

import menhir.tool as mtool
from menhir.tool_utils import OK, FAIL, NOTHING_TO_DO, tool_env, working_dir

log = logging.getLogger(__name__)


class Codecov():
    pass


def tool():
    return Codecov()


@mtool.name.register(Codecov)
def name(arg):
    return "codecov"


@mtool.is_using_tool.register(Codecov)
def is_using_tool(tool, path):
    from os.path import exists, join
    path = join(path, '.coverage')
    return exists(path)


@mtool.dependencies.register(Codecov)
def dependencies(tool, path):
    return []


@mtool.execute_build_phase.register(Codecov)
def execute_build_phase(
        tool, path, info, phase_name, args,
        only_if_changed=False,
        verbose=False,
):
    """Execute a build phase."""
    from os import getenv
    from os.path import exists, join
    from menhir.project import project_name_for_dir
    from menhir.tool_utils import call, package_script

    if phase_name == 'codecov':
        if (
                info.get('changed') or
                info.get('changed_dependents')
        ):
            if verbose:
                print('Running codecov requirements in %s' % path)
            log.debug('codecov requirements in %s', path)

            if not exists(join(path, '.coverage')):
                log.debug('No .coverage in %s', path)
                return OK

            env = tool_env()
            env['MENHIR_PROJECT'] = project_name_for_dir(path)
            env['CODECOV_TOKEN'] = getenv('CODECOV_TOKEN')

            with package_script("/tools/codecov/upload.sh") as f:
                with working_dir(path):
                    return call([f.name], env=env,)
        else:
            if verbose:
                print('Not running codecov in %s' % path)
            log.debug('not running codecov in %s', path)
            return OK
    else:
        return NOTHING_TO_DO
