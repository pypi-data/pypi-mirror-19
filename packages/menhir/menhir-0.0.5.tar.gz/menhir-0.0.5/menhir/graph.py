# Graph functions

# Graphs are modelled as a dict of edges from source node to a set of
# child nodes.


def root_nodes(graph, nodes):
    """Return the set of all nodes that are not dependencies of other nodes."""
    from functools import reduce
    nodes = set(nodes)
    return reduce(set.difference, graph.values(), nodes)


def leaf_nodes(graph):
    """Return the set of all nodes that are not dependencies of other nodes."""
    from functools import reduce
    return reduce(set.union, map(set, graph.values()), set())


def dfs_paths(graph, root_nodes):
    stack = [(node, [node]) for node in root_nodes]
    while stack:
        (vertex, path) = stack.pop()
        next_vertices = graph.get(vertex, set()) - set(path)
        for next in next_vertices:
            stack.append((next, path + [next]))
        if not next_vertices:
            yield path


def build_graph(graph, changed, root_nodes):
    stack = [(node, [node]) for node in root_nodes]
    res = {}
    while stack:
        (vertex, path) = stack.pop()
        next_vertices = graph[vertex] - set(path)
        for next in next_vertices:
            stack.append((next, path + [next]))
        if not next_vertices:
            i = len(path)
            while i:
                i = i - 1
                if path[i] not in changed:
                    path.pop()
                else:
                    break
            while i > 0:
                from_node = path[i - 1]
                s = graph[from_node] or set()
                s.add(path[i])
                res[from_node] = s
                i = i - 1
            if len(path):
                from_node = path[0]
                res[from_node] = res.get(from_node) or set()
    return res
