import unittest
from typing import List, Tuple, Dict

from challenges.qubit_mapping.src.GraphUtils import get_highest_degree_node


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
            0: [1, 2, 3, 4],
            1: [0],
            2: [0],
            3: [0],
            4: [0]
        }
        self.assertEqual(2, get_highest_degree_node(t_architecture))

    def test_