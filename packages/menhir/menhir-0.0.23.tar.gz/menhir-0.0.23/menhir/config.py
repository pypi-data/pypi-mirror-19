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
        config = default_root_config()
    return parse_root_config(config)


def parse_root_config(config):
    tools = config.get('tools')
    config['tools'] = {tool: load_tool(tool) for tool in tools}
    return config


def default_root_config():
    return {
        'tools': default_tools(),
    }


def default_tools():
    from menhir.tools import all_tools
    return all_tools


def describe_repository(config):
    """Parse the root menhir configuration."""
    import os
    from os.path import relpath
    from menhir import gitutils
    from menhir.fileutils import directory_graph
    from menhir.graph import root_nodes

    git_root = gitutils.find_root()
    rel_git_root = relpath(git_root)

    tool_impls = config['tools'].values()

    # build the dependency graph
    fs_graph = directory_graph(rel_git_root)
    infos = project_infos(fs_graph, rel_git_root, tool_impls)
    graph = project_graph(infos)
    roots = root_nodes(graph, infos)

    load_project_config(fs_graph, rel_git_root, infos)

    def is_child(x, y):
        from os.path import abspath, normpath
        return normpath(abspath(y)).startswith(normpath(abspath(x)))

    roots = set(filter(lambda x: is_child('.', x), roots))

    cwd = os.getcwd()
    git_prefix = cwd[len(git_root)+1:]

    config['tool_impls'] = tool_impls
    config['project_infos'] = infos
    config['dependencies'] = graph
    config['root_projects'] = roots
    config['git_root'] = git_root
    config['git_prefix'] = git_prefix
    return config


def defaults_config(dir_path):
    """Return the defaults configuration in dir_path."""
    from os.path import join
    from menhir.fileutils import load_yaml
    return load_yaml(join(dir_path, 'menhir-defaults.yaml')) or {}


def project_config(dir_path):
    """Return the project configuration in dir_path."""
    from os.path import join
    from menhir.fileutils import load_yaml
    return load_yaml(join(dir_path, 'menhir-config.yaml')) or {}


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


def project_infos(graph, root, tools):
    """Return a map of project root path to project info dict."""
    from menhir.graph import dfs_visit

    infos = {}

    def pre_f(state, path):
        used = list(filter(lambda t: t.is_using_tool(path), tools))
        if len(used):
            infos[path] = infos.get(path, {})
            infos[path]['tools'] = used
        return state

    def post_f(state, path, child_states):
        return state

    state = {}
    dfs_visit(graph, root, state, pre_f, post_f,)

    return infos


def load_project_config(graph, root, infos):
    """Load project configuration."""
    from menhir.graph import dfs_visit
    from menhir.utils import deep_merge

    def pre_f(defaults, path):
        from copy import deepcopy
        defaults = deep_merge(defaults, defaults_config(path))
        config = deepcopy(defaults)
        config = deep_merge(config, project_config(path))
        if path in infos:
            infos[path]['config'] = config
        return defaults

    def post_f(defaults, path, child_defaults):
        return defaults

    defaults = {}
    dfs_visit(graph, root, defaults, pre_f, post_f,)

    return infos


def infos_config(base_dir, tools):
    """Return a map of project root path to project info dict."""
    from menhir.fileutils import directory_graph
    from menhir.graph import dfs_visit

    infos = {}

    def config_with_defaults(defaults, path):
        from copy import deepcopy
        defaults.update(defaults_config(path))
        config = deepcopy(defaults)
        config.update(project_config(path))
        if path in infos:
            infos[path]['config'] = config
        return defaults

    def tooling(path):
        used = list(filter(lambda t: t.is_using_tool(path), tools))
        if len(used):
            infos[path] = infos.get(path, {})
            infos[path]['tools'] = used

    def pre_f(state, path):
        tooling(path)
        state = config_with_defaults(state, path)
        return state

    def post_f(state, path, child_states):
        return state

    graph = directory_graph(base_dir)
    state = {}
    dfs_visit(graph, base_dir, state, pre_f, post_f,)

    return infos


def project_graph(roots):
    """Return a project dependency graph."""
    from functools import reduce

    return {
        root: reduce(
            lambda x, y: x.union(y or set()),
            [
                set(tool.dependencies(root))
                for tool in info['tools']
            ],
            set()
        )
        for root, info in roots.items()
        }
