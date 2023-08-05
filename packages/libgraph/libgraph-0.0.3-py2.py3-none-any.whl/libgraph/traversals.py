
import itertools
from collections import deque

DISCOVERED = 0
PROCESSED = 1

class Traversal(object):
    """
    A class that provides delegate methods to assist in graph traversal.
    """
    def __init__(self, graph):
        self.graph = graph

        # Marks a node's state - can be missing (undiscovered), discovered (0) and processed (1)
        self.node_state = {}
        self.entry_times = {}
        self.exit_times = {}

        # The parent nodes for each of the nodes
        self.parents = {}

        # Set this flag to true if you want the traversal to stop
        self.terminated = False

        # Used to record the traversal "index" of a node
        self.curr_time = 0

    def get_node_state(self, node):
        return self.node_state.get(node, None)

    def set_node_state(self, node, state):
        self.node_state[node] = state

    def get_parent(self, node):
        return self.parents.get(node, None)

    def set_parent(self, node, parent):
        self.parents[node] = parent

    def should_process_children(self, node):
        """
        This method is called before a node is processed.  If this method
        returns a False then the node is not processed (and not marked as processed).
        If this method returns False, the success nodes of this node will also not be 
        visited.
        """
        return True

    def process_node(self, node):
        """
        This method is called when a node is ready to be processed (after it has been
        visited).  Only if this method returns True then the node is marked as "processed".
        """
        return True

    def process_edge(self, source, target, edge_data):
        """
        When a node is reached, process_edge is called on the edge that lead to
        the node.   If this method is returned False, then the node is no longer 
        traversed.
        """
        return True

    def select_children(self, node, reverse = False):
        """
        Called to select the children of the node that are up for traversal from the given node
        along with the order the children are to be traversed.

        By default returns all the children in no particular order.
        Returns an iterator of tuples - (node, edge_data)
        """
        return node.iter_neighbours(reverse = reverse)


def bfs(start_node, traversal):
    """
    Performs a breadth first traversal of a graph.
    """
    start_node = traversal.graph.nodes[start_node]
    queue = deque([(None, start_node)])

    while queue:
        parent, node = queue.popleft()
        if traversal.should_process_children(node) is False: continue

        traversal.entry_times[node] = traversal.exit_times[node] = traversal.curr_time
        traversal.curr_time += 1
        if traversal.terminated: return

        # Give a chance to terminate before marking as visited and reaching the children 
        traversal.set_node_state(node, PROCESSED)
        for n,edge in traversal.select_children(node):
            if traversal.get_node_state(n) != PROCESSED:
                queue.append((node,n))
                traversal.set_parent(n, node)

        # Called after all children are added to be processed
        traversal.process_node(node)

def dfs_iter(start_node, traversal):
    """
    Iterative version of the DFS algorithm to avoid stack overflows.
    """
    start_node = traversal.graph.nodes[start_node]
    stack = deque([(None, start_node)])
    while stack:
        parent, node = stack.pop()
        if traversal.process_node(node) is False: continue
        if traversal.terminated: return

        # Give a chance to terminate before marking as visited and reaching the children 
        traversal.set_node_state(node, PROCESSED)
        for n,edge in traversal.select_children(node, reverse = True):
            if traversal.get_node_state(n) != PROCESSED:
                stack.append((node,n))
                traversal.set_parent(n, node)
        traversal.children_added(node)

def dfs(node, traversal):
    """
    Recursive DFS traversal of a graph.
    """
    if traversal.terminated: return

    node = traversal.graph.nodes[node]
    traversal.set_node_state(node, DISCOVERED)
    traversal.entry_times[node] = traversal.curr_time
    traversal.curr_time += 1

    if traversal.should_process_children(node) is not False:
        # Now go through all children
        for n,edge in traversal.select_children(node, reverse = True):
            if traversal.get_node_state(n) == None: # Node has not even been discovered yet
                traversal.set_parent(n, node)
                traversal.process_edge(node, n, edge)
                dfs(n, traversal)
            elif traversal.get_node_state(n) == DISCOVERED or traversal.graph.is_directed:
                traversal.process_edge(node, n, edge)
        if traversal.process_node(node) is not False:
            traversal.set_node_state(node, PROCESSED)
            traversal.curr_time += 1
            traversal.exit_times[node] = traversal.curr_time

