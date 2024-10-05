# We assume non-directed star topology and that the qubit 2 is the center of the star
from typing import List, Tuple, Dict

import qibo.gates
from qibo import Circuit, models

import GraphUtils

STAR_ARCHITECTURE: List[Tuple] = [
    (0,1),(0,2),(0,3),(0,4),
    (1,0),(2,0),(3,0),(4,0)
]

class CircuitTranspiler:
    def transpile(self, circuit: models.Circuit) -> Circuit:
        timesteps = self.generate_timesteps(circuit)
        mapping = self.initial_mapping(timesteps)
        non_optimized_circuit = self.routing(timesteps, mapping)
        optimized_circuit = self.optimize_circuit(non_optimized_circuit)

        return optimized_circuit

    def generate_timesteps(circuit: models.Circuit) -> List[List[Tuple[str, int, int]]]:
        """
        Function to determine the timesteps of a given circuit

        Args:
        circuit (Qibo circuit): qibo circuit to determine the timesteps

        Returns:
        timesteps (list): list of timesteps with the qubits involved in each timestep
        """
        # your code here
        timesteps: List[List[Tuple[str, int, int]]] = [
            [('CNOT',2,0), ('CNOT',3,1)],
            [('X',0,), ('H',1,)],
            [('CNOT',1,4), ('CNOT',0,2), ('H',3,)],
            [('CNOT',4,1), ('X',2,)],
            [('CNOT',1,3), ('H',0,)],
            [('CNOT',0,4), ('CNOT',2,3)],
            [('X',4,)],
            [('CNOT',4,0), ('CNOT',1,2)],
            [('H',0,), ('H',2,), ('CNOT',3,4)],
            [('CNOT',3,2)]
        ]
        return timesteps

    def initial_mapping(timesteps: List[List[Tuple[str, int, int]]]) -> Dict[int, int]:
        """
        Function to determine the initial mapping of the qubits to the architecture.

        Args:
        timesteps (list): list of timesteps with the qubits involved in each timestep

        Returns:
        dict: dictionary with the initial mapping of virtual qubits (referred to as qubits) to physical qubits (referred to as nodes)
        """

        architecture = STAR_ARCHITECTURE
        graph: Dict[int, List[int]] = {}

        # Generate the graph containing connections from each qubit.
        for step in timesteps:
            for gate in step:
                if gate[1] in graph and len(graph[gate[1]]) < 2:
                    graph[gate[1]].append(gate[2])
                else:
                    graph[gate[1]] = [gate[2]]

                if gate[2] in graph and len(graph[gate[2]]) < 2:
                    graph[gate[2]].append(gate[1])
                else:
                    graph[gate[2]] = [gate[1]]

        # Generate the list of qubits
        list_of_qubits = []
        first_qubit = list(graph.keys())[0]

        list_of_qubits.append(first_qubit)
        next_qubit = graph[first_qubit][0]
        while next_qubit is not None and next_qubit is not first_qubit:
            list_of_qubits.append(next_qubit)
            next_qubit = graph[first_qubit][0]

        # Map the list of qubits to the architecture nodes

        return {}

    def routing(timesteps: List[List[Tuple[str, int, int]]], initial_mapping: Dict[int, int]) -> models.Circuit:
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
