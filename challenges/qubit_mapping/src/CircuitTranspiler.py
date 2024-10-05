# We assume non-directed star topology and that the qubit 2 is the center of the star
from typing import List, Tuple, Dict

from qibo import Circuit, models


class CircuitTranspiler:
    def transpile(self, circuit: models.Circuit) -> Circuit:
        timesteps = self.generate_timesteps(circuit)
        mapping = self.initial_mapping(timesteps)
        non_optimized_circuit = self.routing(timesteps, mapping)
        optimized_circuit = self.optimize_circuit(non_optimized_circuit)

        return optimized_circuit

    def generate_timesteps(circuit: models.Circuit) -> List[List[Tuple[int, int]]]:
        """
        Function to determine the timesteps of a given circuit

        Args:
        circuit (Qibo circuit): qibo circuit to determine the timesteps

        Returns:
        timesteps (list): list of timesteps with the qubits involved in each timestep
        """
        # your code here
        return []

    def initial_mapping(timesteps: List[List[Tuple[int, int]]]) -> Dict[int, int]:
        """
        Function to determine the initial mapping of the qubits to the architecture.

        Args:
        timesteps (list): list of timesteps with the qubits involved in each timestep

        Returns:
        dict: dictionary with the initial mapping of virtual qubits (referred to as qubits) to physical qubits (referred to as nodes)
        """
        # your code here
        return {}

    def routing(timesteps: List[List[Tuple[int, int]]], initial_mapping: Dict[int, int]) -> models.Circuit:
        """
        Function that takes as input the timesteps and the initial mapping and outputs the final circuit.

        Args:
        timesteps (List[List[Tuple[int, int]]]): A list of timesteps, where each timestep is a list of tuples representing
                                                 the qubits involved in two-qubit gates at that timestep.

        initial_mapping (Dict[int, int]): A dictionary representing the initial mapping of virtual qubits (keys) to
                                          physical qubits (values).

        Returns:
        models.Circuit: A Qibo circuit object representing the final quantum circuit after applying the routing algorithm.
        """
        return models.Circuit(5)

    def optimize_circuit(circuit: models.Circuit) -> models.Circuit:
        """
        Function that takes as input the circuit and outputs the optimized circuit

        Args:
        circuit (models.Circuit): The circuit to be optimized.

        Returns:
        models.Circuit: The optimized circuit.
        """
        return circuit
