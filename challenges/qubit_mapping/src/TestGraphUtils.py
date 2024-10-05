import unittest

from challenges.qubit_mapping.src.GraphUtils import is_pair_present_in_graph


class TestCircuitTranspiler(unittest.TestCase):
    def test_is_pair_present_in_graph(self):
        graph = [(0, 1)]
        assert is_pair_present_in_graph(graph, (0, 1)) == True
        assert is_pair_present_in_graph(graph, (1, 0)) == True
        assert is_pair_present_in_graph(graph, (0, 2)) == False