from dataclasses import dataclass
from typing import Mapping, TypeVar

from more_properties import cached_property

from parse_2d.diagram import Diagram, Index
from parse_2d.regions import SparseRegion
from parse_2d.tokens.translation import Translation
from parse_2d.tokens.types import Token, Tokenizer

__all__ = ["TemplateTokenizer"]

ST = TypeVar("ST")  # Symbol type
VT = TypeVar("VT")  # Token value type


@dataclass(frozen=True)
class TemplateTokenizer(Tokenizer[ST, VT]):
    """
    Tokenizer for tokens represented by a fixed template of symbols.

    TemplateTokenizer(template, token_value)

    `template` is either a mapping of relative locations to symbols, or a
    Diagram.

    Extracts a token of value `token_value` for every non-overlapping
    translation of the template found in the parent Diagram.
    """

    template: Mapping[Index, ST]
    token_value: VT

    @cached_property
    def symbols(self):
        return set(self.template.values())

    def starts_on(self, symbol: ST) -> bool:
        return symbol in self.symbols

    def matches(self, diagram: Diagram[ST], translation: Translation):
        return all(
            diagram[i + translation] == symbol for i, symbol in self.template.items()
        )

    def extract_token(self, diagram: Diagram[ST], index: Index) -> Token[VT]:
        starting_symbol = diagram[index]

        potential_translations = (
            Translation.between(i, index)
            for i, symbol in self.template.items()
            if symbol == starting_symbol
        )

        for translation in potential_translations:
            if self.matches(diagram, translation):
                return Token(
                    SparseRegion(
                        frozenset(index + translation for index in self.template)
                    ),
                    self.token_value,
                )

        raise IndexError(f"Template not found around index {index!r}")
