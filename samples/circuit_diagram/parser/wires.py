from dataclasses import dataclass
from typing import FrozenSet, Optional

from parse_2d import Diagram, Directions, Translation, Wire, WireTokenizer, tokenize

__all__ = ["extract_wires"]


@dataclass(frozen=True)
class CrossoverWireTokenizer(WireTokenizer[str]):
    def starts_on(self, value: str) -> bool:
        if value == "=":
            return False

        return super().starts_on(value)

    def connections(
        self, segment: str, incoming_direction: Optional[Translation] = None
    ) -> FrozenSet[Translation]:
        if segment == "=" and incoming_direction is not None:
            return frozenset({-incoming_direction})

        return super().connections(segment, incoming_direction)


wire_tokenizer = CrossoverWireTokenizer(
    {
        "-": Directions.horizontal,
        "|": Directions.vertical,
        "/": {Directions.UP_RIGHT.value, Directions.DOWN_LEFT.value},
        "\\": {Directions.UP_LEFT.value, Directions.DOWN_RIGHT.value},
        ".": Directions.all,
        "=": Directions.all,
    }
)


def extract_wires(diagram: Diagram[str]) -> FrozenSet[Wire]:
    return frozenset(token.value for token in tokenize(diagram, [wire_tokenizer]))
