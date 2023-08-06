# menhir configuration
import logging

log = logging.getLogger(__name__)
ROOT_FILE = 'menhir_root.yaml'


def find_root():
    """Based on the current directory, look for a .menhir_root.yaml file."""
    from .fileutils import find_file_in_parents
    root = find_file_in_parents(ROOT_FILE)
    if root is None:
        raise FileNotFoundError(
            'No root file found in parent directories',
            ROOT_FILE
        )
    return root


def root_config(root_file=ROOT_FILE):
    """Return the root menhir configuration."""
    from os.path import exists
    import yaml

    if exists(root_file):
        with open(root_file, 'r') as stream:
            config = yaml.load(stream)
    else:
        config = {
            'tools': default_tools(),
        }

    return parse_config(config)


def default_tools():
    from menhir.tools import all_tools
    return all_tools


def parse_config(config):
    """Parse the root menhir configuration."""
    import os
    from menhir import gitutils
    from menhir.graph import root_nodes
    tools = config.get('tools')
    if tools is None:
        raise Exception(
            'missing_configuration',
            'No tools specified in menhir root config')
    tool_impls = list(map(load_tool, tools))

    dirs = {}
    graph = {}
    roots = ['.']
    while roots:
        d = roots.pop()
        if d not in dirs:
            log.debug('Adding directory: %s', d)
            ds, g, e = dirs_and_graph(d, tool_impls)
            dirs.update(ds)
            graph.update(g)
            e = e.difference(set(dirs.keys()))
            log.debug('Adding discovered nodes: %s', e)
            roots.extend(list(e))

    roots = root_nodes(graph, dirs)
    log.debug('root_projects %s', roots)

    git_root = gitutils.find_root()
    cwd = os.getcwd()
    git_prefix = cwd[len(git_root)+1:]

    config['tool_impls'] = tool_impls
    config['project_infos'] = dirs
    config['dependencies'] = graph
    config['root_projects'] = roots
    config['git_root'] = git_root
    config['git_prefix'] = git_prefix
    return config


def dirs_and_graph(root, tool_impls):
    from menhir.graph import leaf_nodes
    dirs = project_infos(root, tool_impls)
    log.debug('project_infos %s', dirs)
    graph = project_graph(dirs)
    leaves = leaf_nodes(graph)
    extra_nodes = leaves.difference(dirs)
    return dirs, graph, extra_nodes


def load_tool(tool_name):
    """Load the tool implementation for the given tool name."""
    tool = \
        require_tool(tool_name) or \
        require_tool('menhir.tools.%s' % tool_name)
    if not tool:
        raise Exception('configuration_error', 'Tool not found %s', tool_name)
    return tool


def require_tool(tool_path):
    from importlib import import_module
    try:
        m = import_module(tool_path)
        return m.tool()
    except Exception as e:
        log.debug('Failed to import: %s, "%s"', tool_path, e)


def project_infos(base_dir, tools):
    """Return a map of project root path to project info dict."""
    from os import walk
    from os.path import normpath
    import menhir.tool as mtool
    roots = {}
    for root, subdirs, files in walk(base_dir):
        used = list(filter(lambda t: mtool.is_using_tool(t, root), tools))
        if len(used):
            roots[normpath(root)] = {'tools': used}
    return roots


def project_graph(roots):
    """Return a project dependency graph."""
    from functools import reduce
    import menhir.tool as mtools

    return {
        root: reduce(
            lambda x, y: x.union(y or set()),
            [
                set(mtools.dependencies(tool, root))
                for tool in info['tools']
            ],
            set()
        )
        for root, info in roots.items()
        }
