from qibo import gates, models
import unittest
from CircuitTranspiler import CircuitTranspiler, dict_topology_tolist, string_gate
from typing import List, Dict
import networkx as nx


class TestCircuitTranspiler(unittest.TestCase):
    def test_generate_timesteps(self):
        circuit = models.Circuit(5)
        circuit.add(gates.CNOT(2, 0))
        circuit.add(gates.CNOT(3, 1))
        circuit.add(gates.X(0))
        circuit.add(gates.H(1))
        circuit.add(gates.CNOT(1, 4))
        circuit.add(gates.CNOT(0, 2))
        circuit.add(gates.H(3))
        circuit.add(gates.CNOT(4, 1))
        circuit.add(gates.X(2))
        circuit.add(gates.CNOT(1, 3))
        circuit.add(gates.H(0))
        circuit.add(gates.CNOT(0, 4))
        circuit.add(gates.CNOT(2, 3))
        circuit.add(gates.X(4))
        circuit.add(gates.CNOT(4, 0))
        circuit.add(gates.CNOT(1, 2))
        circuit.add(gates.H(2))
        circuit.add(gates.H(0))
        circuit.add(gates.CNOT(3, 4))
        circuit.add(gates.CNOT(3, 2))

        expected_timesteps = [
            [gates.CNOT(2, 0), gates.CNOT(3, 1)],
            [gates.X(0), gates.H(1)],
            [gates.CNOT(1, 4), gates.CNOT(0, 2), gates.H(3)],
            [gates.CNOT(4, 1), gates.X(2)],
            [gates.CNOT(1, 3), gates.H(0)],
            [gates.CNOT(0, 4), gates.CNOT(2, 3)],
            [gates.X(4)],
            [gates.CNOT(4, 0), gates.CNOT(1, 2)],
            [gates.H(2), gates.H(0), gates.CNOT(3, 4)],
            [gates.CNOT(3, 2)],
        ]

        circuit_transpiler = CircuitTranspiler()
        generated_timesteps = circuit_transpiler.generate_timesteps(circuit)

        for i, timestep in enumerate(expected_timesteps):
            for j, expected_gate in enumerate(timestep):
                self.assertEqual(expected_gate.name, generated_timesteps[i][j].name)
                self.assertEqual(expected_gate.qubits, generated_timesteps[i][j].qubits)

    def test_initial_mapping(self):
        timesteps = [
            [gates.CNOT(2, 0), gates.CNOT(3, 1)],
            [gates.X(0), gates.H(1)],
            [gates.CNOT(1, 4), gates.CNOT(0, 2), gates.H(3)],
            [gates.CNOT(4, 1), gates.X(2)],
            [gates.CNOT(1, 3), gates.H(0)],
            [gates.CNOT(0, 4), gates.CNOT(2, 3)],
            [gates.X(4)],
            [gates.CNOT(4, 0), gates.CNOT(1, 2)],
            [gates.H(2), gates.H(0), gates.CNOT(3, 4)],
            [gates.CNOT(3, 2)],
        ]

        circuit_transpiler = CircuitTranspiler()
        mapping = circuit_transpiler.initial_mapping(timesteps)

        expected_mapping = {2: 0, 0: 1, 4: 2, 1: 3, 3: 4}

        self.assertDictEqual(expected_mapping, mapping)

    def test_dict_topology(self):
        star_architecture: Dict[int, List[int]] = {0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}

        expected_edges = [(0, 2), (1, 2), (2, 3), (2, 4)]

        list_edges = dict_topology_tolist(star_architecture)

        graph = nx.Graph(list_edges)

        outcome_edges = [sorted(edge) for edge in graph.edges]

        for edge in expected_edges:
            self.assertIn(edge, outcome_edges)

    def test_routing(self):
        timesteps = [
            [gates.CNOT(2, 0), gates.CNOT(3, 1)],
            [gates.X(0), gates.H(1)],
            [gates.CNOT(1, 4), gates.CNOT(0, 2), gates.H(3)],
            [gates.CNOT(4, 1), gates.X(2)],
            [gates.CNOT(1, 3), gates.H(0)],
            [gates.CNOT(0, 4), gates.CNOT(2, 3)],
            [gates.X(4)],
            [gates.CNOT(4, 0), gates.CNOT(1, 2)],
            [gates.H(2), gates.H(0), gates.CNOT(3, 4)],
            [gates.CNOT(3, 2)],
        ]

        star_architecture: Dict[int, List[int]] = {0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}
        initial_mapping = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
