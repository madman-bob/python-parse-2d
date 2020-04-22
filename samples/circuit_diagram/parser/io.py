from typing import Dict, Iterator

from parse_2d import Diagram, Index, TinyTokenizer, tokenize
from samples.circuit_diagram.ast import InputNode, OutputNode

__all__ = ["parse_input_nodes", "parse_output_nodes"]


def parse_input_nodes(
    diagram: Diagram[str], node_ids: Iterator[int]
) -> Dict[Index, InputNode]:
    input_indices = [
        (0, y) for y in range(len(diagram.contents)) if diagram[(0, y)] == "-"
    ]

    for input_index in input_indices:
        diagram[input_index] = "-input"

    return {index: InputNode(next(node_ids)) for index in input_indices}


def parse_output_nodes(
    diagram: Diagram[str], node_ids: Iterator[int]
) -> Dict[Index, OutputNode]:
    return {
        token.region.location: OutputNode(next(node_ids))
        for token in tokenize(diagram, [TinyTokenizer(":", None)])
    }
