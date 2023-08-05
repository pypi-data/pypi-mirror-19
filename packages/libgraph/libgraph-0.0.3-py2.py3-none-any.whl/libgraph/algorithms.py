
import ipdb
from traversals import *

def connected_components(graph):
    """
    Given a graph (directed or undirected) return its connected components.

    Input: A graph object.
    Output: A dictionary with the nodes as keys and the component index for 
            that node as the value.
    """

    class CCTraversal(Traversal):
        def __init__(self, graph):
            Traversal.__init__(self, graph)
            self.components = {}
            self.curr_component = 0

        def process_node(self, node):
            self.components[node] = self.curr_component

    traversal = CCTraversal(graph)
    for node in graph.nodes:
        if node not in traversal.components:
            # Node has already been assigned a component so dont bother with this
            bfs(node, traversal)
            traversal.curr_component += 1

    return traversal.components

def topo_sort(graph):
    """
    Given a directed graph, return an ordering of nodes ordered by when they can be processed.
    None if cycles exist or if graph is undirected.

    After a node is processed, push it onto a stack, and if at any time we have a BACK edge
    then terminate the process.  Note that the graph can be unconnected so run a DFS from
    all undiscovered nodes.
    """

    class TSTraversal(Traversal):
        def __init__(self, graph):
            Traversal.__init__(self, graph)
            self.stack = []

        def should_process_children(self, node):
            self.stack.append(node)

        def process_edge(self, source, target, edge):
            """
            When processing an edge ensure we have no back edges.
            """
            if self.get_node_state(target) == DISCOVERED:
                self.terminated = True

    traversal = TSTraversal(graph)
    for node in graph.nodes:
        if traversal.get_node_state(node) is None:
            dfs(node, traversal)
            if traversal.terminated:
                return False, None

    return True, traversal.stack
