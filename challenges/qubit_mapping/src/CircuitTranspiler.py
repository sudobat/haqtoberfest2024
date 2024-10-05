# We assume non-directed star topology and that the qubit 2 is the center of the star
from typing import List, Tuple, Dict

from networkx import astar_path
from qibo import Circuit, models, gates
from collections import deque
import networkx as nx


class CircuitTranspiler:
    def __init__(self, circuit: models.Circuit, topology: dict[int, list[int]]):
        self.circuit = circuit
        self.topology_graph = nx.Graph(dict_topology_tolist(topology))
        self.output_circuit = models.Circuit(self.circuit.nqubits)
        self.mapping = {i: i for i in range(self.circuit.nqubits)}

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

    def routing(self, timesteps: List[List[Tuple[int, int]]], initial_mapping: Dict[int, int]) -> models.Circuit:
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
        for timestep in timesteps:
            for gate in timestep:

                # If the gate is a single qubit gate, add it to the output circuit following the mapping
                if len(gate[2]) == 1:
                    self.output_circuit.add(string_gate(gate[0], self.mapping[gate[1][0]]))

                # If the gate is a two qubit gate, check if the qubits are connected in the topology
                elif len(gate[2]) == 2:
                    if (self.mapping[gate[1][0]], self.mapping[gate[1][1]]) in list(self.topology_graph.edges):
                        self.output_circuit.add(
                            string_gate(gate[0], (self.mapping[gate[1][0]], self.mapping[gate[1][1]]))
                        )
                    else:
                        path = astar_path(self.topology_graph, self.mapping[gate[1][0]], self.mapping[gate[1][1]])

                        for i in range(len(path) - 1):
                            self.output_circuit.add(string_gate("CNOT", (path[i], path[i + 1])))
                            self.output_circuit.add(string_gate("CNOT", (path[i + 1], path[i])))
                            self.output_circuit.add(string_gate("CNOT", (path[i], path[i + 1])))

                        self.mapping[gate[2][1]] = gate[2][0]
                        self.mapping[gate[2][0]] = gate[2][1]

                        self.output_circuit.add(string_gate(gate[0], (path[-1], self.mapping[gate[2][0]])))

        return self.output_circuit

    def optimize_circuit(circuit: models.Circuit) -> models.Circuit:
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
    if name == "cnot":
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
