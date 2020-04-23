from abc import ABCMeta
from dataclasses import dataclass, field
from typing import Callable, FrozenSet, Set, Tuple

__all__ = [
    "Node",
    "InputNode",
    "OutputNode",
    "OpNode",
    "NodeInput",
    "ConnectionLabel",
    "Connection",
    "Circuit",
]

NodeID = int


@dataclass(frozen=True)
class Node(metaclass=ABCMeta):
    id: NodeID


@dataclass(frozen=True)
class InputNode(Node):
    pass


@dataclass(frozen=True)
class OutputNode(Node):
    pass


@dataclass(frozen=True)
class OpNode(Node):
    func: Callable
    arg_count: int


@dataclass(frozen=True)
class NodeInput:
    id: NodeID
    arg_pos: int


@dataclass(frozen=True)
class ConnectionLabel:
    constant: int = 0
    variables: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Connection:
    inputs: FrozenSet[NodeID]
    outputs: FrozenSet[NodeInput]

    labels: FrozenSet[ConnectionLabel] = field(default_factory=frozenset)


@dataclass
class Circuit:
    nodes: Set[Node] = field(default_factory=set)
    connections: Set[Connection] = field(default_factory=set)
