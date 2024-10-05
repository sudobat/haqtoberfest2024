# We assume non-directed star topology and that the qubit 2 is the center of the star
from typing import List, Tuple, Dict

import networkx as nx
from networkx import astar_path
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

    def generate_timesteps(self, circuit: models.Circuit) -> List[List[gates.Gate]]:
        """
        Function to determine the timesteps of a given circuit

        Args:
        circuit (Qibo circuit): qibo circuit to determine the timesteps

        Returns:
        timesteps (list): list of timesteps with the qubits involved in each timestep
        """

        circuit_gates: List[gates.Gate] = circuit.queue

        # (name, (qubit1, [qubit2]))
        timesteps: List[List[gates.Gate]] = []
        current_timestep: List[gates.Gate] = []

        qubits_used_in_current_timestep = []

        for gate in circuit_gates:
            if gate.qubits[0] in qubits_used_in_current_timestep or (len(gate.qubits) > 1 and gate.qubits[1] in qubits_used_in_current_timestep):
                timesteps.append(current_timestep.copy())
                current_timestep = [gate]
                qubits_used_in_current_timestep = [gate.qubits[0]]
                if len(gate.qubits) > 1:
                    qubits_used_in_current_timestep.append(gate.qubits[1])
            else:
                current_timestep.append(gate)
                qubits_used_in_current_timestep.append(gate.qubits[0])
                if len(gate.qubits) > 1:
                    qubits_used_in_current_timestep.append(gate.qubits[1])

        timesteps.append(current_timestep.copy())

        return timesteps

    def initial_mapping(self, timesteps: List[List[gates.Gate]]) -> Dict[int, int]:
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
                if gate.qubits[0] in graph and len(graph[gate.qubits[0]]) < 2:
                    graph[gate.qubits[0]].append(gate.qubits[1])
                else:
                    graph[gate.qubits[0]] = [gate.qubits[1]]

                if gate.qubits[1] in graph and len(graph[gate.qubits[1]]) < 2:
                    graph[gate.qubits[1]].append(gate.qubits[0])
                else:
                    graph[gate.qubits[1]] = [gate.qubits[0]]

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

    def routing(self, timesteps: List[List[gates.Gate]], initial_mapping: Dict[int, int]) -> models.Circuit:
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
        # (name, (qubit1, qubit2))
        # Run over all timesteps and gates in the timesteps
        output_circuit = Circuit(len(initial_mapping.keys()))
        topology_graph = nx.Graph(dict_topology_tolist(STAR_ARCHITECTURE))
        
        for timestep in timesteps:
            for gate in timestep:

                # If the gate is a single qubit gate, add it to the output circuit following the mapping
                if len(gate.qubits) == 1:
                    output_circuit.add(string_gate(gate.name, initial_mapping[gate.qubits[0]]))

                # If the gate is a two qubit gate, check if the qubits are connected in the topology
                elif len(gate.qubits) == 2:
                    if (initial_mapping[gate.qubits[0]], initial_mapping[gate.qubits[1]]) in list(topology_graph.edges):
                        output_circuit.add(
                            string_gate(gate.name, (initial_mapping[gate.qubits[0]], initial_mapping[gate.qubits[1]]))
                        )
                    else:
                        path = astar_path(topology_graph, initial_mapping[gate.qubits[0]], initial_mapping[gate.qubits[1]])

                        for i in range(len(path) - 1):
                            output_circuit.add(string_gate("cx", (path[i], path[i + 1])))
                            output_circuit.add(string_gate("cx", (path[i + 1], path[i])))
                            output_circuit.add(string_gate("cx", (path[i], path[i + 1])))

                        initial_mapping[gate.qubits[1]] = gate.qubits[0]
                        initial_mapping[gate.qubits[0]] = gate.qubits[1]

                        output_circuit.add(string_gate(gate.name, (path[-1], initial_mapping[gate.qubits[0]])))

        return output_circuit

    def optimize_circuit(self, circuit: models.Circuit) -> models.Circuit:
        """
        Function that takes as input the circuit and outputs the optimized circuit

        Args:
        circuit (models.Circuit): The circuit to be optimized.

        Returns:
        models.Circuit: The optimized circuit.
        """

        output_circuit = models.Circuit(circuit.nqubits)
        circ = circuit.copy()

        num_list = circ.ngates

        # last_qubit_gate = {}
        # for i, gate in enumerate(circ.queue):
        #     if last_qubit_gate[gate.qubits[0]] != gate:
        #         last_qubit_gate[gate.qubits[0]] = gate
        #         output_circuit.add(gate)
        #     else:

        for i, gate in enumerate(circ.queue):
            for j in range(i + 1, len(circ.queue)):
                comp = circ.queue[j]
                if any(x == y for x, y in zip(gate[1], comp[1])):
                    if gate == comp:
                        break
                    else:
                        output_circuit.add(gates.CNOT(*gate))
                        break

        return circuit


def string_gate(name: str, qubits: int | tuple[int, int]) -> gates.Gate:
    """Converts a tuple representation of a get as (name, qubits) into a Gate object.

    Args:
        name (str): The name of the gate. Can be "cnot", "x" or "h".
        qubits (int | tuple[int, int]): The qubits the gate acts on. If the gate is a single qubit gate, it is an int.
        If it is a two qubit gate, it is a tuple of two ints.

    Raises:
        ValueError: If the gate name is not supported.

    Returns:
        gates.Gate: The qibo Gate object.
    """
    if name == "cx":
        return gates.CNOT(*qubits)
    elif name == "x":
        return gates.X(qubits)
    elif name == "h":
        return gates.H(qubits)
    else:
        raise ValueError(f"Gate {name} not supported")


def dict_topology_tolist(topology: dict[int, list[int]]) -> List[Tuple[int, int]]:
    """Helper function to convert a dictionary {node: [neighbors]} into a list of edges as tuples of nodes.

    Args:
        topology (dict[int, list[int]]): The topology of the quantum device represented as a dictionary {node: [neighbors]}.

    Returns:
        List[Tuple[int, int]]: The list of edges as tuples of nodes.
    """
    edges = []
    for node, neighbors in topology.items():
        for neighbor in neighbors:
            edges.append((node, neighbor))
    return edges
