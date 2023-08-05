#!/usr/bin/env python

import unittest
import test_graph

suite = unittest.TestLoader().loadTestsFromTestCase(test_graph.TestGraph)
unittest.TextTestRunner(verbosity=2).run(suite)
