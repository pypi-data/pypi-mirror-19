# Build tools that menhir knows how to use.  This is a mapping from
# name to namespace used to implement the support.
import logging

from menhir.config import root_config

log = logging.getLogger(__name__)

tools = {
    'setup.py': 'menhir.tools.setup_py'
}


def execute_phase(build_order, tool_impls, phase_name):
    import menhir.tool as mtool
    for projects in build_order:
        for path in reversed(projects):
            for tool in tool_impls:
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
    return {
        'status': 'ok'
    }


def build_order(dependencies, project_dirs, root_projects, start, end):
    from menhir.graph import dfs_paths
    g = changed_graph(dependencies, project_dirs, root_projects, start, end)
    roots = [node for node in root_projects if node in g]
    paths = [node for node in dfs_paths(g, roots)]
    return filtered_build_order(paths)


def filtered_build_order(build_order):
    x = [set()]
    x.extend(build_order)
    rs = reductions(set.union, map(set, x), set())
    return list(map(
        lambda x, y: list(filter(lambda z: z not in y, x)),
        build_order,
        rs
    ))


def reductions(f, lst, init):
    prev = init
    for i in lst:
        prev = f(prev, i)
        yield prev


def changed_graph(dependencies, project_dirs, root_projects, start, end):
    from menhir.graph import build_graph
    projs = changed_projects(project_dirs, start, end)
    return build_graph(dependencies, projs, root_projects)


def changed_projects(roots, start, end):
    """Find the set of projects that contain changed files."""
    files = changed_files(start, end)['all']
    return projects_with_files(roots, files)


def projects_with_files(roots, files):
    roots = set(roots)
    changed_roots = set()
    log.debug('roots: %s', roots)
    log.debug('files: %s', files)
    for path in files:
        if len(roots):
            for root in roots.copy():
                if path.startswith(root):
                    changed_roots.add(root)
                    roots.remove(root)
        else:
            break
    return changed_roots


def changed_files(start, end):
    from menhir import gitutils
    repo = gitutils.repo()
    start_commit = gitutils.commit(repo, start)
    end_commit = gitutils.commit(repo, end)
    changed_files = gitutils.diff(start_commit, end_commit)
    return changed_files


__all__ = [
    'root_config',
    'changed_files',
]
