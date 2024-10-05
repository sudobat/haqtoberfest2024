from qibo import gates, models
import unittest

from qibo import gates, models

from CircuitTranspiler import CircuitTranspiler


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
            [('cx', (2, 0)), ('cx', (3, 1))],
            [('x', (0,)), ('h', (1,))],
            [('cx', (1, 4)), ('cx', (0, 2)), ('h', (3,))],
            [('cx', (4, 1)), ('x', (2,))],
            [('cx', (1, 3)), ('h', (0,))],
            [('cx', (0, 4)), ('cx', (2, 3))],
            [('x', (4,))],
            [('cx', (4, 0)), ('cx', (1, 2))],
            [('h', (2,)), ('h', (0,)), ('cx', (3, 4))],
            [('cx', (3, 2))]
        ]

        circuit_transpiler = CircuitTranspiler()
        generated_circuit = circuit_transpiler.generate_timesteps(circuit)

        self.assertListEqual(expected_timesteps, generated_circuit)
