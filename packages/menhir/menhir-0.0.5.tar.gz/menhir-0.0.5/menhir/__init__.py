# Build tools that menhir knows how to use.  This is a mapping from
# name to namespace used to implement the support.
import logging

from menhir.config import root_config
from menhir.tool_utils import OK

log = logging.getLogger(__name__)


def execute_phase(build_order, dirs, phase_name):
    """For the given build order, invoke build tools for phase_name."""
    import menhir.tool as mtool
    for projects in build_order:
        for path in reversed(projects):
            for tool in dirs[path]:
                res = mtool.execute_build_phase(tool, path, phase_name)
                log.debug('Execute tool %s phase %s in %s returns %s',
                          mtool.name(tool), phase_name, path, res)
                if res['status'] == 'fail':
                    log.debug('Tool %s phase %s in %s failed %s',
                              mtool.name(tool), phase_name, path, res)
                    res['tool'] = mtool.name(tool)
                    res['phase'] = phase_name
                    res['path'] = path
                    return res
    return OK


def build_order(
        dependencies, project_dirs, root_projects, files, root_prefix
):
    from menhir.graph import dfs_paths
    g = changed_graph(
        dependencies, project_dirs, root_projects, files, root_prefix
    )
    roots = [node for node in root_projects if node in g]
    paths = [node for node in dfs_paths(g, roots)]
    log.debug('paths: %s', paths)
    return filtered_build_order(paths)


def not_in(x, y):
    """Remove all of the elements in the set y from the list x."""
    return list(filter(lambda z: z not in y, x))


def filtered_build_order(build_order):
    """Remove the tails of build_order elements containing earlier elements."""
    x = [set([])]  # nothing has initially been build
    x.extend(build_order)
    seen = list(reductions(set.union, map(set, x), set()))
    seen.pop()  # last element contains every project
    return list(map(not_in, build_order, seen))


def reductions(f, lst, init):
    """Like reduce, but returns all intermediate values as a sequence."""
    prev = init
    for i in lst:
        prev = f(prev, i)
        yield prev


def changed_graph(
        dependencies, project_dirs, root_projects, files, root_prefix
):
    from menhir.graph import build_graph
    projs = projects_with_files(project_dirs, files, root_prefix)
    log.debug('Projects to build: %s', projs)
    return build_graph(dependencies, projs, root_projects)


def projects_with_files(roots, files, root_prefix):
    """Filter roots that contain any of files paths.

    The roots are each prefixed with root_prefix, before comparison.
    """
    from os.path import join, normpath
    log.debug('projects_with_files:')
    log.debug(' roots: %s', roots)
    log.debug(' files: %s', files)
    roots = set(roots)
    changed_roots = set()
    for path in files:
        if len(roots):
            for root in roots.copy():
                prefix = normpath(join(root_prefix, root))
                log.debug('prefix: %s, path: %s', prefix, path)
                if path.startswith(prefix):
                    changed_roots.add(root)
                    roots.remove(root)
        else:
            break
    return changed_roots


__all__ = [
    'root_config',
    'build_order',
    'execute_phase'
]
