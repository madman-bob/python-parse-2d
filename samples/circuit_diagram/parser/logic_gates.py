from operator import and_, not_, or_, xor
from typing import Dict, Iterator

from parse_2d import Diagram, Index, TinyTokenizer, tokenize
from samples.circuit_diagram.ast import OpNode

__all__ = ["parse_logic_gates"]

nand = lambda a, b: not a & b
nor = lambda a, b: not a | b
xnor = lambda a, b: not a ^ b
const_0 = lambda: False
const_1 = lambda: True

logic_gate_tokenizers = [
    TinyTokenizer("a", (and_, 2)),
    TinyTokenizer("A", (nand, 2)),
    TinyTokenizer("o", (or_, 2)),
    TinyTokenizer("O", (nor, 2)),
    TinyTokenizer("x", (xor, 2)),
    TinyTokenizer("X", (xnor, 2)),
    TinyTokenizer("~", (not_, 1)),
    TinyTokenizer("(", (const_0, 0)),
    TinyTokenizer(")", (const_1, 0)),
]


def parse_logic_gates(
    diagram: Diagram[str], node_ids: Iterator[int]
) -> Dict[Index, OpNode]:
    logic_gates = {
        token.region.location: OpNode(next(node_ids), *token.value)
        for token in tokenize(diagram, logic_gate_tokenizers)
    }

    for logic_gate_index in logic_gates:
        diagram[logic_gate_index] = "logic_gate"

    return logic_gates
