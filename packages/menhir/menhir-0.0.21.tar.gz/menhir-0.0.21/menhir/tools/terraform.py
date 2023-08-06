"""Terraform commands.

Provides ``plan``, ``apply`` and ``destroy`` tasks for terrform, managing
remote-state.

Configuration is under the ``terraform`` key.

The ``targets`` key contains a dict for each target directory.  Each
infra directory is configured as a dict under the directory's name.

Arguments
---------

A directory can be configures with ``args``, a list containing the names
of values it expects to be passed on the command line.


Vars passed to Terraform
------------------------

The ``values`` key configures a list of names for values to be passed
to terraform.

``values`` can contain names from ``args`` and the following:

project        the name of the project
branch         the current branch name
branch-slug    the current branch name, sanitised
sha            the current commit sha as a hex string
sha-mod-1024   the current as a decimal modulo 1024

The ``values`` list can also contain items of the form ``name=value``,
which will pass the var ``name`` to terraform, with the value
calculated according to ``value`` from the list above.

Remote Config
-------------

The remote state is configured independently of the target direcotry
using the `remote-config` key.  The value contains a `backend` string
specifying the terraform backend, and a `backend-config` dict
specifying the backend specific configuration.

The `remote-config` key is also supported at the target directory
level.  For consistency, usage at this level is not recommended.

The only supported backend at present is ``s3``.  It expects
``bucket``, ``key`` and ``region`` values.  The `key`
configuration value is a format string, with can use ``project`` and
``component`` arguments.

In each target directory config, the ``component`` list of values is
used to construct a string to identify the remote state configuration.
``component`` defaults to ``args``.

"""
import logging

import menhir.tool as mtool
from menhir.tool_utils import FAIL, NOTHING_TO_DO, OK, tool_env, working_dir
from menhir.utils import multi, method

log = logging.getLogger(__name__)


class Terraform():
    def __str__(self):
        return "<%s>" % type(self).__name__

    def __repr__(self):
        return "<%s>" % type(self).__name__


def tool():
    return Terraform()


@mtool.name.register(Terraform)
def name(arg):
    return "terraform"


@mtool.is_using_tool.register(Terraform)
def is_using_tool(tool, path):
    from os.path import exists, join
    path = join(path, 'infra')
    return exists(path)


@mtool.dependencies.register(Terraform)
def dependencies(tool, path):
    return []


@mtool.add_arg_parser.register(Terraform)
def add_arg_parser(tool, parser):
    parsers = parser.add_subparsers(help="Terraform commands", dest='phase')
    p = parsers.add_parser(
        'apply',
        help='Apply a terraform infrastructure directory'
    )
    p.add_argument('directory', nargs=1)
    p.add_argument('args', nargs="*")
    p = parsers.add_parser(
        'plan',
        help='Plan a terraform infrastructure directory'
    )
    p.add_argument('directory', nargs=1)
    p.add_argument('args', nargs="*")
    p = parsers.add_parser(
        'destroy',
        help='Destroy a terraform infrastructure directory'
    )
    p.add_argument('directory', nargs=1)
    p.add_argument('args', nargs="*")


@mtool.execute_build_phase.register(Terraform)
def execute_build_phase(tool, path, info, args, **kwargs):
    """Execute a build phase."""
    from os.path import exists, join

    config = info['config'].get('terraform', {})
    log.debug('terraform config: %(config)s', {'config': config})
    infra_dir = join(path, config.get('source-dir', 'infra'))

    if not exists(infra_dir):
        log.debug('No infra directory in %(path)s', {'path': path})
        return NOTHING_TO_DO

    return task(path, info, config, args)


def task(path, info, config, args):
    """Execute a task."""
    return action(args.phase, path, info, config, args)


def action(action, path, info, config, args):
    """Invoke a terraform action on the given path."""
    from functools import reduce
    from os.path import exists, join
    from menhir.project import project_name_for_dir
    from menhir.tool_config import aliased_value_array, value_array
    from menhir.tool_utils import call
    from menhir.utils import deep_merge

    directory = args.directory[0]
    changed = info.get('changed') or info.get('changed_dependents')
    project_dir = join(path, 'infra', args.directory[0])
    project_dir_exists = exists(project_dir)

    run = project_dir_exists and (changed or action == 'destroy')
    log_run(run, args.phase, directory, path)

    if not run:
        return NOTHING_TO_DO

    dconfig = config.get('targets', {}).get(directory, {})
    dargs = dconfig.get('args', [])
    dcomponent = dconfig.get('component', dargs)
    dvalues = dconfig.get('values', [])
    remote_config = config.get('remote-config')
    dremote_config = dconfig.get('remote-config', {})
    remote_config = deep_merge(remote_config, dremote_config)

    if len(args.args or []) < len(dargs):
        log.error(
            'Not enough arguments to terraform apply %(directory)s: '
            'expected: %(expected)s, got: %(got)s',
            {
                'directory': directory,
                'expected': dargs,
                'got': args.args,
            }
        )
        return FAIL

    arg_dict = dict(zip(dargs, args.args))

    component = "-".join(value_array(dcomponent, info, path, arg_dict))

    def format_value(x):
        return '%s="%s"' % x

    values = list(map(
        format_value,
        aliased_value_array(dvalues, info, path, arg_dict),
    ))

    def extend_var(x, y):
        x.extend(['-var', y])
        return x

    var_args = reduce(extend_var, values, [],)

    project_name = project_name_for_dir(path)

    env = tool_env()

    with working_dir(project_dir):
        print('rc')
        if remote_state(remote_config, project_name, component):
            return FAIL
        print('get')
        res = call(["terraform", "get"], env=env,)
        if res != OK:
            return res
        log.info("terraform %s %s", action, var_args)
        print(action)
        return call(["terraform", action] + var_args, env=env,)


def log_run(cond, task, directory, path):
    txt = None
    if cond:
        txt = 'Run %(task)s in %(path)s'
    else:
        txt = 'Not run %(task)s in %(path)s'

    log.info(txt, {'task': task, 'directory': directory, 'path': path})


def remote_state(remote_config, project, component):
    import shutil
    if not remote_config:
        return None

    backend = remote_config.get('backend')
    if not backend:
        log.warning('remote-state configured, but no backend specified')
        return None

    backend_config = remote_config.get('backend-config')
    if not backend_config:
        log.warning('remote-state configured, but no backend_config specified')
        return None

    shutil.rmtree('.terraform', ignore_errors=True)
    return remote_state_backend(backend, backend_config, project, component)


@multi
def remote_state_backend(backend, backend_config, project, component):
    """Configure a remote backend."""
    return backend


@method(remote_state_backend, 's3')
def remote_state_s3(backend, backend_config, project, component):
    from os import getenv
    from os.path import join
    from subprocess import call

    bucket = backend_config.get('bucket')
    if not bucket:
        log.warning('terraform remote-state s3: no bucket specified')
        return None

    key = backend_config.get('key', "%(project)-%(component)")

    component = component or 'config'
    key = key % {'project': project, 'component': component}
    key = join(key, "terraform.tfstate")
    region = backend_config.get('region', "us-east-1")

    log.info(
        'State from s3://%(bucket)s/%(key)s in %(region)s',
        {
            'bucket': bucket,
            'key': key,
            'region': region,
        }
    )

    env = tool_env()

    tf_log = getenv('TF_LOG')
    if tf_log:
        env['TF_LOG'] = tf_log

    cmd = [
            "terraform", "remote", "config",
            "-backend=s3",
            "-backend-config=bucket=%s" % bucket,
            "-backend-config=key=%s" % key,
            "-backend-config=region=%s" % region,
        ]

    return call(cmd, env=env)
