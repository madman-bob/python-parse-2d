from dataclasses import dataclass
from typing import TypeVar

from parse_2d.diagram import Diagram, Index
from parse_2d.regions import TinyRegion
from parse_2d.tokens.types import Token, Tokenizer

__all__ = ["TinyTokenizer"]

ST = TypeVar("ST")  # Symbol type
VT = TypeVar("VT")  # Token value type


@dataclass(frozen=True)
class TinyTokenizer(Tokenizer[ST, VT]):
    """
    Tokenizer for tokens represented by a single symbol

    TinyTokenizer(symbol, token_value)

    Extracts a token of value `token_value` for every `symbol` in the diagram.
    """

    symbol: ST
    token_value: VT

    def starts_on(self, symbol: ST) -> bool:
        return symbol == self.symbol

    def extract_token(self, diagram: Diagram[ST], index: Index) -> Token[VT]:
        assert diagram[index] == self.symbol

        return Token(TinyRegion(index), self.token_value)
