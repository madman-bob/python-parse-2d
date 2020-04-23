from collections import deque
from dataclasses import dataclass, field
from typing import Deque, FrozenSet, List, Optional

from parse_2d import (
    Diagram,
    Directions,
    Index,
    Token,
    Translation,
    Wire,
    WireTokenizer,
    tokenize,
)

__all__ = ["extract_wires"]


@dataclass(frozen=True)
class CircuitDiagramWire(Wire):
    labels: FrozenSet[str]


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


label_reading_directions = {
    Directions.UP_RIGHT.value,
    Directions.RIGHT.value,
    Directions.DOWN_RIGHT.value,
    Directions.DOWN.value,
}


@dataclass(frozen=True)
class LabelledWireTokenizer(WireTokenizer[str]):
    labels: List[str] = field(default_factory=list)
    partial_label: Deque[str] = field(default_factory=deque)

    def is_segment(self, value: str) -> bool:
        if value.isalnum() or value == "+":
            return True

        return super().is_segment(value)

    def connections(
        self, segment: str, incoming_direction: Optional[Translation] = None
    ) -> FrozenSet[Translation]:
        if incoming_direction is None:
            return super().connections(segment, incoming_direction)

        if segment.isalnum() or segment == "+":

            if incoming_direction in label_reading_directions:
                self.partial_label.appendleft(segment)
            else:
                self.partial_label.append(segment)

            return frozenset({-incoming_direction})
        elif self.partial_label:

            self.labels.append("".join(self.partial_label))
            self.partial_label.clear()

        return super().connections(segment, incoming_direction)

    def extract_token(
        self, diagram: Diagram[str], index: Index
    ) -> Token[CircuitDiagramWire]:
        self.partial_label.clear()
        self.labels.clear()

        wire_token = super().extract_token(diagram, index)

        if self.partial_label:
            self.labels.append("".join(self.partial_label))

        return Token(
            wire_token.region,
            CircuitDiagramWire(wire_token.value.sockets, frozenset(self.labels)),
        )


@dataclass(frozen=True)
class CircuitDiagramWireTokenizer(CrossoverWireTokenizer, LabelledWireTokenizer):
    pass


wire_tokenizer = CircuitDiagramWireTokenizer(
    {
        "-": Directions.horizontal,
        "|": Directions.vertical,
        "/": {Directions.UP_RIGHT.value, Directions.DOWN_LEFT.value},
        "\\": {Directions.UP_LEFT.value, Directions.DOWN_RIGHT.value},
        ".": Directions.all,
        "=": Directions.all,
    }
)


def extract_wires(diagram: Diagram[str]) -> FrozenSet[CircuitDiagramWire]:
    return frozenset(token.value for token in tokenize(diagram, [wire_tokenizer]))
