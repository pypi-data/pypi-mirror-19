
import ipdb
import unittest
from libgraph import graphs, traversals, algorithms

class Tests(unittest.TestCase):
    def test_basic(self):
        g = graphs.Graph()
        g.add_edges((1,2), (1,3), (1,4), (2,5), (5, 6))

        tr = traversals.Traversal(g)
        traversals.bfs(1, tr)
        self.assertEqual(tr.get_node_state(1), 1)
        self.assertEqual(tr.get_node_state(2), 1)
        self.assertEqual(tr.get_node_state(3), 1)
        self.assertEqual(tr.get_node_state(4), 1)
        self.assertEqual(tr.get_node_state(5), 1)
        self.assertEqual(tr.get_node_state(6), 1)

        self.assertEqual(tr.get_parent(1), None)
        self.assertEqual(tr.get_parent(2), 1)
        self.assertEqual(tr.get_parent(3), 1)
        self.assertEqual(tr.get_parent(4), 1)
        self.assertEqual(tr.get_parent(5), 2)
        self.assertEqual(tr.get_parent(6), 5)
