from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Generic, Iterable, List, TypeVar

from parse_2d.diagram import Diagram, Index
from parse_2d.regions import Region

__all__ = [
    "Token",
    "Tokenizer",
    "tokenize",
]

ST = TypeVar("ST")  # Symbol type
VT = TypeVar("VT")  # Token value type


@dataclass(frozen=True)
class Token(Generic[VT]):
    region: Region
    value: VT


class Tokenizer(Generic[ST, VT], metaclass=ABCMeta):
    """
    Abstract class for Diagram tokenizers of ST symbols, to VT tokens, that can
    recognize its token type based on the presence of a particular symbol.

    `starts_on(symbol)` returns whether this class can start tokenizing from the
    given symbol.

    `extract_token(diagram, index)` returns the token generated from the given
    diagram at the given index.
    """

    @abstractmethod
    def starts_on(self, symbol: ST) -> bool:
        raise NotImplementedError

    @abstractmethod
    def extract_token(self, diagram: Diagram[ST], index: Index) -> Token[VT]:
        raise NotImplementedError


def tokenize(
    diagram: Diagram[ST], tokenizers: List[Tokenizer[ST, VT]],
) -> Iterable[Token[VT]]:
    diagram_coverage = set()

    for index, value in diagram.items():
        if index in diagram_coverage:
            continue

        for tokenizer in tokenizers:
            if tokenizer.starts_on(value):
                token = tokenizer.extract_token(diagram, index)
                diagram_coverage |= set(list(token.region))
                yield token
