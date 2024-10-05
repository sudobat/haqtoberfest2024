# We assume non-directed star topology and that the qubit 2 is the center of the star
from typing import List, Tuple, Dict
from qibo import Circuit, models, gates

import GraphUtils

STAR_ARCHITECTURE: Dict[int, List[int]] = {
    0: [1, 2, 3, 4],
    1: [0],
    2: [0],
    3: [0],
    4: [0]
}

class CircuitTranspiler:
    def transpile(self, circuit: models.Circuit) -> Circuit:
        timesteps = self.generate_timesteps(circuit)
        mapping = self.initial_mapping(timesteps)
        non_optimized_circuit = self.routing(timesteps, mapping)
        optimized_circuit = self.optimize_circuit(non_optimized_circuit)

        return optimized_circuit

    def generate_timesteps(self, circuit: models.Circuit) -> List[List[Tuple[str, Tuple[int, int]]]]:
        """
        Function to determine the timesteps of a given circuit

        Args:
        circuit (Qibo circuit): qibo circuit to determine the timesteps

        Returns:
        timesteps (list): list of timesteps with the qubits involved in each timestep
        """

        circuit_gates: List[gates.Gate] = circuit.queue

        # (name, (qubit1, [qubit2]))
        timesteps: List[List[Tuple[str, Tuple[int, int]]]] = []
        current_timestep: List[Tuple[str, Tuple[int, int]]] = []

        qubits_used_in_current_timestep = []

        for gate in circuit_gates:
            if gate.qubits[0] in qubits_used_in_current_timestep or (len(gate.qubits) > 1 and gate.qubits[1] in qubits_used_in_current_timestep):
                timesteps.append(current_timestep.copy())
                current_timestep = [(gate.name, gate.qubits)]
                qubits_used_in_current_timestep = [gate.qubits[0]]
                if len(gate.qubits) > 1:
                    qubits_used_in_current_timestep.append(gate.qubits[1])
            else:
                current_timestep.append((gate.name, gate.qubits))
                qubits_used_in_current_timestep.append(gate.qubits[0])
                if len(gate.qubits) > 1:
                    qubits_used_in_current_timestep.append(gate.qubits[1])

        timesteps.append(current_timestep.copy())

        return timesteps

    def initial_mapping(self, timesteps: List[List[Tuple[str, int, int]]]) -> Dict[int, int]:
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

        # Create subgraphs from highest degree node
        subgraphs: List[int] = GraphUtils.get_subgraphs(architecture)

        # Map the list of qubits to the architecture nodes
        mapping = {}
        for qubit in list_of_qubits:
            mapping[qubit] = subgraphs.pop(0)

        return mapping

    def routing(self, timesteps: List[List[Tuple[str, int, int]]], initial_mapping: Dict[int, int]) -> models.Circuit:
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

    def optimize_circuit(self, circuit: models.Circuit) -> models.Circuit:
        """
        Function that takes as input the circuit and outputs the optimized circuit

        Args:
        circuit (models.Circuit): The circuit to be optimized.

        Returns:
        models.Circuit: The optimized circuit.
        """
        return circuit
