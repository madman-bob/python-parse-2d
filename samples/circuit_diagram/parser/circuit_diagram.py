from itertools import count
from typing import List, Optional

from parse_2d import Diagram, Directions, Translation
from samples.circuit_diagram.ast import (
    Circuit,
    Connection,
    ConnectionLabel,
    InputNode,
    Node,
    NodeInput,
    OpNode,
    OutputNode,
)
from samples.circuit_diagram.parser.io import parse_input_nodes, parse_output_nodes
from samples.circuit_diagram.parser.logic_gates import parse_logic_gates
from samples.circuit_diagram.parser.wires import extract_wires

__all__ = ["parse_circuit_diagram"]

arg_count_input_directions = {
    0: [],
    1: [Directions.LEFT.value],
    2: [Directions.UP_LEFT.value, Directions.DOWN_LEFT.value],
}


def node_inputs(node: Optional[Node]) -> List[Translation]:
    if isinstance(node, OutputNode):
        arg_count = 1
    elif isinstance(node, OpNode):
        arg_count = node.arg_count
    else:
        arg_count = 0

    return arg_count_input_directions[arg_count]


def node_output(node: Optional[Node]) -> Optional[Translation]:
    if isinstance(node, (InputNode, OpNode)):
        return Directions.RIGHT.value


def parse_connection_label(label: str) -> ConnectionLabel:
    components = label.split("+")

    return ConnectionLabel(
        sum((int(component) for component in components if component.isnumeric()), 0),
        tuple(component for component in components if not component.isnumeric()),
    )


def parse_circuit_diagram(diagram: Diagram[str]):
    node_ids = count()

    input_nodes = parse_input_nodes(diagram, node_ids)
    output_nodes = parse_output_nodes(diagram, node_ids)
    logic_gate_nodes = parse_logic_gates(diagram, node_ids)

    wires = extract_wires(diagram)

    nodes = {**input_nodes, **output_nodes, **logic_gate_nodes}

    connections = set()

    for wire in wires:
        socket_nodes = [nodes.get(socket.location) for socket in wire.sockets]
        socket_nodes_inputs = [node_inputs(node) for node in socket_nodes]

        connections.add(
            Connection(
                frozenset(
                    node.id
                    for socket, node in zip(wire.sockets, socket_nodes)
                    if socket.direction == node_output(node)
                ),
                frozenset(
                    NodeInput(node.id, inputs.index(socket.direction))
                    for socket, node, inputs in zip(
                        wire.sockets, socket_nodes, socket_nodes_inputs
                    )
                    if socket.direction in inputs
                ),
                frozenset(parse_connection_label(label) for label in wire.labels),
            )
        )

    return Circuit(set(nodes.values()), connections)
