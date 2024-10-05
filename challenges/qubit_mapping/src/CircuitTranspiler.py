# We assume non-directed star topology and that the qubit 2 is the center of the star

class CircuitTranspiler:
    def __init__(self, circuit):
        self._circuit = circuit

    def transpile(self):
        self._adapt()
        self._optimize()
        pass

    def _adapt(self):
        pass

    def _optimize(self):
        pass

