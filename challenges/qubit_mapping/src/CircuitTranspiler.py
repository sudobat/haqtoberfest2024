# We assume non-directed star topology and that the qubit 2 is the center of the star

import qibo
from qibo import gates, models


class CircuitTranspiler:
    def __init__(self, circuit):
        self._circuit = circuit
        self._centre = 2
        self._qdict = {i: i for i in range(5)}
        self._gatelist = [(i, i.name, i.qubits) for i in self._circuit.queue]
        self._outputcirc = qibo.models.Circuit(5)

    def transpile(self):
        self._adapt()
        self._optimize()
        pass

    def _adapt(self):
        # for gate, info in self._gatelist:
        pass

    def _optimize(self):
        pass
