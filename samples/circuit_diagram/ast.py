from abc import ABCMeta
from dataclasses import dataclass, field
from typing import Callable, FrozenSet, Mapping, Set, Tuple, Union

__all__ = [
    "Node",
    "InputNode",
    "OutputNode",
    "OpNode",
    "Function",
    "FuncNode",
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
class Function:
    name: str
    contents: "Circuit"


@dataclass(frozen=True)
class FuncNode(Node):
    func: Union[str, Callable]
    arg_count: int
    out_count: int


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
    functions: Mapping[str, Function] = field(default_factory=dict)
    nodes: Set[Node] = field(default_factory=set)
    connections: Set[Connection] = field(default_factory=set)
