from dataclasses import dataclass
from typing import Callable, FrozenSet, Mapping, TypeVar

from more_properties import cached_property

from parse_2d.diagram import Diagram, Index
from parse_2d.regions import RectRegion
from parse_2d.tokens.translation import Directions, Translation
from parse_2d.tokens.types import Token, Tokenizer

__all__ = ["BoxTokenizer"]

ST = TypeVar("ST")  # Symbol type
VT = TypeVar("VT")  # Token value type

corners = {
    Directions.UP_RIGHT,
    Directions.DOWN_RIGHT,
    Directions.DOWN_LEFT,
    Directions.UP_LEFT,
}
search_directions = {
    Directions.UP: Directions.RIGHT.value,
    Directions.UP_RIGHT: Directions.DOWN.value,
    Directions.RIGHT: Directions.DOWN.value,
    Directions.DOWN_RIGHT: Directions.LEFT.value,
    Directions.DOWN: Directions.LEFT.value,
    Directions.DOWN_LEFT: Directions.UP.value,
    Directions.LEFT: Directions.UP.value,
    Directions.UP_LEFT: Directions.RIGHT.value,
}
next_edge = {
    Directions.UP: Directions.UP_RIGHT,
    Directions.UP_RIGHT: Directions.RIGHT,
    Directions.RIGHT: Directions.DOWN_RIGHT,
    Directions.DOWN_RIGHT: Directions.DOWN,
    Directions.DOWN: Directions.DOWN_LEFT,
    Directions.DOWN_LEFT: Directions.LEFT,
    Directions.LEFT: Directions.UP_LEFT,
    Directions.UP_LEFT: Directions.UP,
}


@dataclass(frozen=True)
class BoxTokenizer(Tokenizer[ST, VT]):
    """
    Tokenizer for tokens represented by a box of edge symbols.

    BoxTokenizer(edge_symbols, contents_tokenizer)

    `edge_tokens` is a mapping from a side of the box, to the collection of
    symbols that may be used for that edge.

    `contents_tokenizer` is a function to determine the value of the extracted
    token, and is passed the entire box (including the edge) as its only
    parameter.
    """

    edge_symbols: Mapping[Directions, FrozenSet[ST]]
    contents_tokenizer: Callable[[Diagram[ST]], VT]

    @cached_property
    def symbols(self):
        return frozenset.union(*self.edge_symbols.values())

    def starts_on(self, symbol: ST) -> bool:
        return symbol in self.symbols

    @staticmethod
    def follow_line(
        diagram: Diagram[ST],
        index: Index,
        line_symbols: FrozenSet[ST],
        direction: Translation,
    ) -> Index:
        while diagram[index] in line_symbols:
            index += direction

        return index

    def trace_box(self, diagram: Diagram[ST], index: Index, starting_edge: Directions):
        current_edge = starting_edge

        min_x, min_y = index
        max_x, max_y = index

        for _ in range(8):
            direction = search_directions[current_edge]

            if diagram[index] not in self.edge_symbols[current_edge]:
                raise TypeError()

            index = self.follow_line(
                diagram, index, self.edge_symbols[current_edge], direction
            )

            x, y = index

            min_x = min(x, min_x)
            min_y = min(y, min_y)
            max_x = max(x, max_x)
            max_y = max(y, max_y)

            current_edge = next_edge[current_edge]

        top_left = min_x, min_y
        bottom_right = (max_x, max_y) + Directions.DOWN_RIGHT.value

        return Token(
            RectRegion(top_left, bottom_right),
            self.contents_tokenizer(diagram[top_left:bottom_right]),
        )

    def extract_token(self, diagram: Diagram[ST], index: Index) -> Token[VT]:
        potential_starting_edges = (
            edge
            for edge, symbols in self.edge_symbols.items()
            if diagram[index] in symbols
        )

        for potential_starting_edge in potential_starting_edges:
            try:
                return self.trace_box(diagram, index, potential_starting_edge)
            except TypeError:
                continue
