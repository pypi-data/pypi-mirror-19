
import ipdb
from traversals import Traversal, bfs

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

        def process_node(self, parent, node):
            self.components[node] = self.curr_component

    ipdb.set_trace()
    traversal = CCTraversal(graph)
    for node in graph.nodes:
        if node not in traversal.components:
            traversal.curr_component += 1
            # Node has already been assigned a component so dont bother with this
            bfs(node, traversal)

    return traversal.components

