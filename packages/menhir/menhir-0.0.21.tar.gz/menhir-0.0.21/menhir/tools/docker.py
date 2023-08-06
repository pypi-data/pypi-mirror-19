"""
The docker tool provides ``build``, ``push`` and ``publish`` commands.
"""

import logging

import menhir.tool as mtool
from menhir.tool_utils import OK, FAIL, NOTHING_TO_DO, tool_env, working_dir

log = logging.getLogger(__name__)


class Docker():
    def __str__(self):
        return "<%s>" % type(self).__name__

    def __repr__(self):
        return "<%s>" % type(self).__name__


def tool():
    return Docker()


@mtool.name.register(Docker)
def name(arg):
    return "docker"


@mtool.is_using_tool.register(Docker)
def is_using_tool(tool, path):
    from os.path import exists, join
    path = join(path, 'Dockerfile')
    return exists(path)


@mtool.dependencies.register(Docker)
def dependencies(tool, path):
    return []


@mtool.add_arg_parser.register(Docker)
def add_arg_parser(tool, parser):
    parser.description = "Commands to build and push docker images."
    parsers = parser.add_subparsers(help="Docker commands", dest='phase')
    parsers.add_parser(
        'build',
        help='Build a docker image from a Dockerfile'
    )
    parsers.add_parser(
        'push',
        help='Push a docker image to a remote repository'
    )
    parsers.add_parser(
        'publish',
        help='Build and push a docker image to a remote repository'
    )


@mtool.execute_build_phase.register(Docker)
def execute_build_phase(
        tool, path, info, args,
        only_if_changed=False,
        verbose=False,
):
    """Execute a build phase."""
    from os.path import exists, join
    from menhir.tool_utils import run_if

    phase_name = args.phase

    dockerfile = join(path, 'Dockerfile')
    repo = info['config'].get('docker', {}).get('repository')

    if not exists(dockerfile):
        log.debug('No Dockerfile %(dockerfile)s', {'dockerfile': dockerfile})
        return NOTHING_TO_DO

    changed = info.get('changed') or info.get('changed_dependents')

    if phase_name == 'build':
        with run_if(changed, phase_name, path, verbose) as flag:
            if flag:
                return docker_build(path, args, verbose)
            return OK

    elif phase_name == 'push':
        with run_if(changed, phase_name, path, verbose) as flag:
            if flag:
                return docker_push(repo, path, info, args, verbose)
            return OK

    elif phase_name == 'publish':
        with run_if(changed, phase_name, path, verbose) as flag:
            if flag:
                res = docker_build(path, args, verbose)
                if res != OK:
                    return res
                return docker_push(repo, path, info, args, verbose)
            return OK
    else:
        return NOTHING_TO_DO


def docker_build(path, args, verbose):
    from menhir.project import project_name_for_dir
    from menhir.tool_utils import call, package_script
    if verbose:
        print('Running docker-build in %s' % path)
    log.debug('docker-build in %s', path)

    project_name = project_name_for_dir(path)

    env = tool_env()
    env['MENHIR_TAG'] = project_name

    with package_script("/tools/docker/docker-build.sh") as f:
        with working_dir(path):
            return call([f.name], env=env,)


def docker_push(repo, path, info, args, verbose=False):
    from menhir.project import branch, project_name_for_dir, image
    from menhir.tool_utils import call, package_script, slugify
    if verbose:
        print('Running docker-push in %s' % path)
    log.debug('docker-push in %s', path)

    project_name = project_name_for_dir(path)
    current_branch = branch()
    tag = project_name
    sha_tag = image(info)
    if not sha_tag:
        log.error('No remote repository configured to push to.')
        return FAIL
    branch_tag = "%s:%s" % (
        sha_tag.split(':')[0],
        slugify(current_branch, length=40),
    )

    env = tool_env()
    env['MENHIR_TAG'] = tag
    env['MENHIR_BRANCH_TAG'] = branch_tag
    env['MENHIR_SHA_TAG'] = sha_tag

    with package_script("/tools/docker/docker-push.sh") as f:
        with working_dir(path):
            return call([f.name], env=env,)
