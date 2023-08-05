
import ipdb
import unittest
from libgraph import graphs, traversals, algorithms

class Tests(unittest.TestCase):
    def test_basic(self):
        g = graphs.Graph()
        g.add_edges((1,2), (1,3), (1,4), (2,5), (5, 6))

        comps = algorithms.connected_components(g)
        self.assertEqual(len(set(comps.values())), 1)

    def test_no_edges(self):
        g = graphs.Graph()
        g.add_nodes(1,2,3,4,5)

        comps = algorithms.connected_components(g)
        self.assertEqual(len(set(comps.values())), 5)

    def test_islands(self):
        g = graphs.Graph()
        g.add_edges((1,2), (2,3), (3,4))
        g.add_edges((10,20), (20,30), (30,40))
        g.add_edges((100,200), (200,300), (300,400))

        comps = algorithms.connected_components(g)
        self.assertEqual(len(set(comps.values())), 3)

    def test_topo_sort_no_cycles(self):
        g = graphs.Graph(directed = True)
        g.add_edges((1,2), (1,9), (2,9), (2,3), (9, 3), (3, 4), (4,5), (4,8), (5,6), (6,8), (6,7), (8,7))

        exists,path = algorithms.topo_sort(g)
        print "Path: ", path
        self.assertTrue(exists)
        self.assertEquals(path, list(xrange(1,10)))

    def test_topo_sort_no_cycles_disconnected(self):
        g = graphs.Graph(directed = True)
        g.add_edges((1,2), (1,3), (1,4))
        g.add_edges((10,20), (10,30), (10,40))

        exists,path = algorithms.topo_sort(g)
        print "Path: ", path
        self.assertTrue(exists)
        self.assertEquals(path, [1,4,3,2,40,10,30,20])
