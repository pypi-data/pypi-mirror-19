
import itertools
from collections import deque

class Traversal(object):
    """
    A class that provides delegate methods to assist in graph traversal.
    """
    def __init__(self, graph):
        self.graph = graph

        # Marks a node's state - can be missing (undiscovered), discovered (0) and processed (1)
        self.node_state = {}

    def get_node_state(self, node):
        return self.node_state.get(node, None)

    def set_node_state(self, node, state):
        self.node_state.get[node] = state

    def process_node(self, parent, node):
        """
        Override this method to process node upon its discovery (but 
        before its children are added to the candidate list for visiting).
        If this method returns False or None then its children are not 
        considered.

        Also note that if this method returns False for a node, it wont be marked
        as visited in the DFS and its children wont be visited.  However it is 
        possible that the same node could be reached from another path and 
        processed (since visited is False).
        """
        return True

    def process_edge(self, source, target, edge_data):
        """
        When a node is reached, process_edge is called on the edge that lead to
        the node.   If this method is returned False, then the node is no longer 
        traversed.
        """
        return True

    def select_children(self, node):
        """
        Called to select the children of the node that are up for traversal from the given node
        along with the order the children are to be traversed.

        By default returns all the children in no particular order.
        Returns an iterator of tuples - (node, edge_data)
        """
        return node.iter_neighbours()

    def children_added(self, node):
        """
        Called after all the selected successor nodes of a node have been enqueued
        in the traversal algorithm
        """
        pass

def bfs(start_node, traversal):
    """
    Performs a breadth first traversal of a graph.
    """
    queue = deque([(None, start_node)])
    parents = {start_node: None}

    PROCESSED = 1
    while queue:
        parent, node = queue.popleft()
        if traversal.process_node(parent, node) is True:
            # Give a chance to terminate before marking as visited and reaching the children 
            traversal.set_node_state(node, PROCESSED)
            for n,edge in traversal.select_children(node):
                if traversal.get_node_state(node) != PROCESSED:
                    queue.append((node,n))
                    parents[n] = node
            traversal.children_added(node)
    return parents

def dfs(start_node, traversal):
    stack = deque([(None, start_node)])
    PROCESSED = 1
    parents = {start_node: None}
    while stack:
        parent, node = stack.pop()
        if traversal.process_node(parent, node) is True:
            # Give a chance to terminate before marking as visited and reaching the children 
            traversal.set_node_state(node, PROCESSED)
            for n,edge in traversal.select_children(node):
                if traversal.get_node_state(node) != PROCESSED:
                    stack.append((node,n))
                    parents[n] = node
            traversal.children_added(node)
    return parents

