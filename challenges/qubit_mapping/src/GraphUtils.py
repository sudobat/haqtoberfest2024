from os import remove
from typing import Tuple, List, Dict


def get_highest_degree_node(graph: Dict[int, List[int]]) -> int:
    # if graph is empty, return -1
    max_node = -1
    max_degree = 0
    for node, connections in graph.items():
        degree = len(connections)
        if degree > max_degree:
            max_degree = degree
            max_node = node

    return max_node


def remove_edge(graph: Dict[int, List[int]], edge: Tuple[int,int]) -> Dict[int, List[int]]:
    new_graph = graph.copy()
    new_graph[edge[0]].remove(edge[1])
    if not new_graph[edge[0]]:
        del new_graph[edge[0]]

    new_graph[edge[1]].remove(edge[0])
    if not new_graph[edge[1]]:
        del new_graph[edge[1]]

    return new_graph


def get_max_degree_neighbor(graph: Dict[int, List[int]], node: int) -> int:
    max_degree_neighbor = graph[node][0]
    for neighbor in graph[node]:
        if len(graph[neighbor]) > len(graph[max_degree_neighbor]):
            max_degree_neighbor = neighbor
    return max_degree_neighbor


def get_subgraphs(graph: Dict[int, List[int]]) -> List[int]:
    new_graph = graph.copy()
    subgraphs: List[int] = []

    starting_node = get_highest_degree_node(new_graph)
    while starting_node != -1:
        subgraph = get_next_subgraph(new_graph)
        subgraphs.extend(subgraph)
        starting_node = get_highest_degree_node(new_graph)

    return subgraphs


def get_next_subgraph(remaining_graph: Dict[int, List[int]], node: int) -> List[int]:
    current_node = node
    subgraph = [current_node]
    neighbor_amount = len(remaining_graph[current_node])

    while neighbor_amount > 0 and current_node not in subgraph:
        max_degree_neighbor = get_max_degree_neighbor(remaining_graph, current_node)
        subgraph.append(max_degree_neighbor)
        remaining_graph = remove_edge(remaining_graph, (current_node, max_degree_neighbor))
        current_node = max_degree_neighbor
        neighbor_amount = len(remaining_graph[current_node])

    del remaining_graph[current_node]
    return subgraph