from typing import Tuple, List


def is_pair_present_in_graph(graph: List[Tuple[int, int]], pair: Tuple[int, int]) -> bool:
    reversed_pair = tuple(reversed(pair))
    for edge in graph:
        if pair == edge:
            return True
        elif reversed_pair == edge:
            return True
    return False

