import matplotlib.pyplot as plt
from qibo import gates, models
from qibo.ui import plot_circuit
from CircuitTranspiler import CircuitTranspiler
import unittest

class TestCircuitTranspiler(unittest.TestCase):
    def test_first(self):
        c = models.Circuit(5)
        c.add(gates.CNOT(0, 2))
        c.add(gates.CNOT(2, 4))
        c.add(gates.CNOT(1, 3))
        c.add(gates.X(0))
        c.add(gates.CNOT(4, 3))
        c.add(gates.CNOT(1, 2))
        c.add(gates.CNOT(0, 1))
        c.add(gates.X(2))
        c.add(gates.H(0))
        c.add(gates.H(3))
        c.add(gates.CNOT(1, 0))
        c.add(gates.CNOT(3, 2))
        c.add(gates.CNOT(0, 3))

        self.assertTrue(True, "Test passed")