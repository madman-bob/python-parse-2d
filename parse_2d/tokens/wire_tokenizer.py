from collections import deque
from dataclasses import dataclass
from typing import FrozenSet, Mapping, Optional, TypeVar

from parse_2d.diagram import Diagram, Index
from parse_2d.tokens.translation import Directions, Translation
from parse_2d.tokens.types import Token, Tokenizer

__all__ = ["WireSocket", "Wire", "WireTokenizer"]

ST = TypeVar("ST")  # Symbol type


@dataclass(frozen=True)
class WireSocket:
    """
    A socket is an available connection, that can be connected to from the given
    location, by going in the given direction
    """

    location: Index
    direction: Translation


@dataclass(frozen=True)
class Wire:
    sockets: FrozenSet[WireSocket]


@dataclass(frozen=True)
class WireTokenizer(Tokenizer[ST, Wire]):
    """
    Tokenizer for wire tokens, represented by a path through a diagram

    WireTokenizer(segment_connections)

    A wire consists of multiple symbol "segments", each of which has a fixed
    collection of directions it can connect to.

    `segment_connections` is a mapping from segment symbols to a collection of
    that segment's available connections.

    Extracts a wire token representing the available connections to that wire.

    This class assumes that segments connect all possible incoming directions
    to all possible outgoing directions.
    Child classes may override this behaviour by overriding `connections`:

    `connections(segment, incoming_direction=None)`
    Returns all of the segment's outgoing directions, restricted to those
    available from the incoming direction, if given.
    """

    segment_connections: Mapping[ST, FrozenSet[Translation]]

    def starts_on(self, value: ST) -> bool:
        return value in self.segment_connections

    def is_segment(self, value: ST) -> bool:
        return value in self.segment_connections

    def connections(
        self, segment: ST, incoming_direction: Optional[Translation] = None
    ) -> FrozenSet[Translation]:
        return self.segment_connections.get(segment, Directions.all)

    def extract_token(self, diagram: Diagram[ST], index: Index) -> Token[Wire]:
        connections_border = deque([(index, None)])
        visited_connections = set()
        sockets = set()

        while connections_border:
            i, incoming_direction = connections_border.pop()
            symbol = diagram[i]

            for direction in self.connections(symbol, incoming_direction):
                adj_i = i + direction
                adj_symbol = diagram[adj_i]
                connection = adj_i, -direction

                if connection in visited_connections:
                    continue

                if adj_symbol == diagram.whitespace:
                    continue

                if -direction in self.connections(adj_symbol):
                    if self.is_segment(adj_symbol):
                        connections_border.append(connection)
                        visited_connections.add(connection)
                    else:
                        sockets.add(WireSocket(*connection))

        return Token({i for i, _ in visited_connections}, Wire(frozenset(sockets)))
