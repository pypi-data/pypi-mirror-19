# pyenv based tool for menhir
import re

import menhir.tool as mtool


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
    res = subprocess.run(cmd, *args, *kwargs)
    if res.returncode:
        return False, {
            'status': 'fail'
        }
    return True, {
        'status': 'ok',
    }


@mtool.execute_build_phase.register(Pyenv)
def execute_build_phase(tool, path, phase_name):
    """Execute a build phase."""
    from os import chmod, remove
    from os.path import basename
    import stat
    import subprocess
    import tempfile
    import pkg_resources

    print('exec', path, phase_name)
    if phase_name == 'requirements':
        resource_package = "menhir"
        resource_path = "/tools/pyenv/requirements.sh"
        script = pkg_resources.resource_string(resource_package, resource_path)
        fname = None
        try:
            with tempfile.NamedTemporaryFile("xb", delete=False) as f:
                fname = f.name
                f.write(script)
            chmod(fname, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            res = subprocess.run([f.name, path, basename(path)])
        finally:
            remove(fname)

        if res.returncode:
            return {
                'status': 'fail'
            }
        return {
            'status': 'ok'
        }
    else:
        return {
            'status': 'nothing_to_do'
        }
