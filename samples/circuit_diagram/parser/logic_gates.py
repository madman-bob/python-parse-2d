from operator import and_, not_, or_, xor
from typing import Dict, Iterator

from parse_2d import Diagram, Index, TinyTokenizer, tokenize
from samples.circuit_diagram.ast import OpNode

__all__ = ["parse_logic_gates"]

nand = lambda a, b: not a & b
nor = lambda a, b: not a | b
xnor = lambda a, b: not a ^ b

logic_gate_tokenizers = [
    TinyTokenizer("a", (and_, 2)),
    TinyTokenizer("A", (nand, 2)),
    TinyTokenizer("o", (or_, 2)),
    TinyTokenizer("O", (nor, 2)),
    TinyTokenizer("x", (xor, 2)),
    TinyTokenizer("X", (xnor, 2)),
    TinyTokenizer("~", (not_, 1)),
]


def parse_logic_gates(
    diagram: Diagram[str], node_ids: Iterator[int]
) -> Dict[Index, OpNode]:
    return {
        token.region.location: OpNode(next(node_ids), *token.value)
        for token in tokenize(diagram, logic_gate_tokenizers)
    }
