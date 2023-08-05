
import ipdb
from collections import defaultdict
import itertools

class Node(object):
    def __init__(self, key, **properties):
        self._key = key
        self._properties = properties
        self._neighbours = {}

    def __repr__(self):
        return repr(self._key)

    @property
    def neighbours(self):
        """
        A list of neighbour nodes.
        """
        return self._neighbours

    def iter_neighbours(self):
        """
        A list of neighbour nodes.
        """
        return self._neighbours.iteritems()

    def ensure_neighbour(self, node, default_data):
        if node not in self._neighbours:
            self._neighbours[node] = default_data
        return self._neighbours[node]

    def add_neighbour(self, node, data):
        self._neighbours[node] = data

    def del_neighbour(self, node):
        if node in self._neighbours:
            del self._neighbours[node]

    @property
    def key(self):
        return self._key

    @property
    def properites(self):
        return self._properties

    def __hash__(self):
        return hash(self._key)

    def __cmp__(self, another):
        if hasattr(another, "key"):
            return cmp(self._key, another._key)
        else:
            return cmp(self._key, another)

class Edge(object):
    def __init__(self, source, target, directed = False, **properties):
        self._source = source
        self._target = target
        self._directed = directed
        self._properties = properties

    def __repr__(self):
        if self._directed:
            return "Edge<%s --> %s>" % (repr(self.source), repr(self.target))
        else:
            return "Edge<%s <-> %s>" % (repr(self.source), repr(self.target))

    @property
    def is_directed(self):
        return self._directed

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def properites(self):
        return self._properties

class Graph(object):
    """
    Implementation of an undirected graph.
    """
    def __init__(self, multi = False, directed = False):
        self.nodes = {}
        self._is_directed = directed
        self._is_multi = multi

    @property
    def is_multi(self):
        return self._is_multi

    @property
    def is_directed(self):
        return self._is_directed

    def add_node(self, node):
        """
        Adds or update a node in the graph.  A node is any hashable object (or even a Node object).
        """
        if node not in self.nodes:
            # All the edges of the given node
            if not isinstance(node, Node):
                node = Node(node)
            self.nodes[node] = node
        return self.nodes[node]

    def add_nodes(self, *nodes):
        return [self.add_node(node) for node in nodes]

    def add_edges(self, *source_target_pairs):
        for source, target in source_target_pairs:
            self.add_edge(source, target)

    def get_edge(self, source, target):
        return self.nodes[source].neighbours[target]

    def add_edge(self, source, target, **properties):
        """
        Add a new Edge object into the graph.  If the edge's source and target nodes do not exist
        then new nodes are added implicitly.  Returns an Edge object whose properties can be set.  
        Optionally the properties can be passed to this method and they will be set in the returned 
        Edge object.
        """
        source, target = self.add_nodes(source, target)
        newedge = Edge(source, target, directed = self.is_directed, **properties)
        if self.is_multi:
            self.nodes[source].ensure_neighbour(target, []).append(newedge)
            if not self.is_directed:
                self.nodes[target].ensure_neighbour(source, []).append(newedge)
        else:
            self.nodes[source].add_neighbour(target, newedge)
            if not self.is_directed:
                self.nodes[target].add_neighbour(source, newedge)

    def iter_node_edges(self, nodekey):
        """
        Returns an iterator over all edges for a given node.  The ordering of edges is unspecified.
        """
        if self.is_multi:
            return itertools.chain(itertools.imap(iter, self.nodes[nodekey]))
        else:
            return self.nodes[nodekey].neighbours.itervalues()

    def iter_edges(self, nodekey):
        """
        Returns an iterator over all edges in the graph.  The ordering of edges is unspecified.
        """
        for source in self.nodes.iterkeys():
            for target, edge in self.nodes[node].neighbours.iteritems():
                # Only yield the edge if it originates form here, 
                # this would take care of the case of both directed
                # and undirected edges
                if self.is_multi:
                    for e in edges:
                        if e.source == source:
                            yield e
                elif edge.source == source:
                    yield edge

    def del_node(self, node):
        """
        Delete a node in the graph.  This also removes all of the nodes incident edges.
        """
        targets = self.nodes[node][:]
        for t in targets:
            self.nodes[t].del_neighbour(node)
        del self.nodes[node]

    def del_edge(self, source, target):
        """
        Delete all edge between two nodes.
        """
        if source in self.nodes and target in self.nodes:
            self.nodes[source].del_neighbour(target)
            if not self.is_directed:
                self.nodes[target].del_neighbour(source)

