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
    import yaml

    with open(root_file, 'r') as stream:
        config = yaml.load(stream)
    return parse_config(config)


# def extend_list(x, y):
#     if y:
#         x.extend(y)
#     return x


def parse_config(config):
    """Parse the root menhir configuration."""
    from menhir.graph import root_nodes
    tools = config.get('tools')
    if tools is None:
        raise Exception(
            'missing_configuration',
            'No tools specified in menhir root config')
    tool_impls = list(map(load_tool, tools))
    config['tool_impls'] = tool_impls
    dirs = project_dirs('.', config['tool_impls'])
    config['project_dirs'] = dirs
    graph = project_graph(dirs, tool_impls)
    config['dependencies'] = graph
    config['root_projects'] = root_nodes(graph, dirs)
    return config


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


def project_dirs(base_dir, tools):
    """Return a map of project root path to tool list."""
    from os import walk
    from os.path import normpath
    import menhir.tool as mtool
    roots = {}
    for root, subdirs, files in walk(base_dir):
        used = list(filter(lambda t: mtool.is_using_tool(t, root), tools))
        if len(used):
            roots[normpath(root)] = used
    return roots


def project_graph(roots, tool_impls):
    """Return a project dependency graph."""
    from functools import reduce
    import menhir.tool as mtools

    return {
        root: reduce(
            lambda x, y: x.union(y or set()),
            [
                set(mtools.dependencies(tool, root))
                for tool in tool_impls
            ],
            set()
        )
        for root in roots
        }


# {
#     root: reduce(
#         set_union,
#         [
#             set(mtools.dependencies(tool, root))
#             for tool in tool_impls
#         ],
#         set()
#     )
#     for root in roots
#     }

# config['dependencies'] = {
# root: reduce(
#     extend_list,
#     [
#         mtools.dependencies(tool, root)
#         for tool in tool_impls
#     ],
#     []
# )
# for root in roots
# }
