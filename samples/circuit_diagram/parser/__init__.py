from parse_2d.diagram import Diagram
from samples.circuit_diagram.ast import Circuit
from samples.circuit_diagram.parser.circuit_diagram import (
    parse_circuit_diagram as _parse_circuit_diagram,
)

__all__ = ["parse_circuit_diagram"]


def parse_circuit_diagram(diagram_str: str) -> Circuit:
    return _parse_circuit_diagram(Diagram.from_string(diagram_str))
