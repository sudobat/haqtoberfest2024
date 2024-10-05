import unittest
from typing import List, Dict

from challenges.qubit_mapping.src.GraphUtils import get_highest_degree_node, remove_edge, get_max_degree_neighbor, \
    get_subgraphs

class TestCircuitTranspiler(unittest.TestCase):
    def test_get_highest_degree_node(self):
        star_architecture: Dict[int, List[int]] = {
            0: [1, 2, 3, 4],
            1: [0],
            2: [0],
            3: [0],
            4: [0]
        }
        self.assertEqual(0, get_highest_degree_node(star_architecture))

        t_architecture:  Dict[int, List[int]] = {
            0: [1],
            1: [0, 2],
            2: [1, 3, 4],
            3: [2],
            4: [2]
        }
        self.assertEqual(2, get_highest_degree_node(t_architecture))

    def test_remove_edge(self):
        graph: Dict[int, List[int]] = {
            0: [1, 2, 3, 4],
            1: [0],
            2: [0],
            3: [0],
            4: [0]
        }
        edge = (0, 1)
        new_graph = {
            0: [2, 3, 4],
            2: [0],
            3: [0],
            4: [0]
        }
        self.assertDictEqual(new_graph, remove_edge(graph, edge))

        small_graph: Dict[int, List[int]] = {
            0: [1],
            1: [0]
        }
        edge = (0, 1)
        new_graph = {}
        self.assertDictEqual(new_graph, remove_edge(small_graph, edge))

    def test_get_max_degree_neighbor(self):
        t_architecture:  Dict[int, List[int]] = {
            0: [1],
            1: [0, 2],
            2: [1, 3, 4],
            3: [2],
            4: [2]
        }
        self.assertEqual(1, get_max_degree_neighbor(t_architecture, 2))
        self.assertEqual(2, get_max_degree_neighbor(t_architecture, 1))

    def test_get_subgraphs(self):
        q_architecture:  Dict[int, List[int]] = {
            0: [1],
            1: [0, 2, 4],
            2: [1, 3],
            3: [2, 4],
            4: [3, 1]
        }
        self.assertListEqual([1, 2, 3, 4, 0], get_subgraphs(q_architecture))

        t_architecture:  Dict[int, List[int]] = {
            0: [1],
            1: [0, 2],
            2: [1, 3, 4],
            3: [2],
            4: [2]
        }

        star_architecture: Dict[int, List[int]] = {
            0: [1, 2, 3, 4],
            1: [0],
            2: [0],
            3: [0],
            4: [0]
        }
        self.assertListEqual([0,1,2,3,4], get_subgraphs(star_architecture))
