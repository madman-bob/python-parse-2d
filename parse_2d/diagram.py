from dataclasses import dataclass
from typing import Iterable, List, MutableMapping, Tuple, TypeVar, Union

__all__ = ["char_matrix", "Index", "Diagram"]

V = TypeVar("V")  # Value type
D = TypeVar("D")  # Default value type

Index = Tuple[int, int]


def char_matrix(s: str) -> List[List[str]]:
    return list(map(list, s.splitlines()))


@dataclass
class Diagram(MutableMapping[Index, V]):
    contents: List[List[V]]
    whitespace: V

    def __getitem__(self, item: Index) -> V:
        if isinstance(item, slice):
            min_x, min_y = item.start
            max_x, max_y = item.stop

            return [line[min_x:max_x] for line in self.contents[min_y:max_y]]

        x, y = item

        if y < 0 or y >= len(self.contents) or x < 0 or x >= len(self.contents[y]):
            return self.whitespace

        return self.contents[y][x]

    def __setitem__(self, key: Index, value: V) -> None:
        if isinstance(key, slice):
            min_x, min_y = key.start
            max_x, max_y = key.stop

            if max_y - min_y != len(value):
                raise IndexError

            for line, replacement_line in zip(self.contents[min_y:max_y], value):
                if max_x - min_x != len(replacement_line):
                    raise IndexError

                line[min_x:max_x] = replacement_line

            return

        x, y = key

        if y < 0 or y >= len(self.contents) or x < 0 or x >= len(self.contents[y]):
            raise IndexError

        self.contents[y][x] = value

    def __delitem__(self, key):
        if isinstance(key, slice):
            min_x, min_y = key.start
            max_x, max_y = key.stop

            for line in self.contents[min_y:max_y]:
                line[min_x:max_x] = [self.whitespace] * (max_x - min_x)

            return

        x, y = key

        if y < 0 or y >= len(self.contents) or x < 0 or x >= len(self.contents[y]):
            raise IndexError

        self.contents[y][x] = self.whitespace

    def __iter__(self) -> Iterable[Index]:
        return self.keys()

    def __len__(self) -> int:
        return sum(1 for item in self.values() if item != self.whitespace)

    def __contains__(self, item: Index) -> bool:
        return self[item] != self.whitespace

    def keys(self) -> Iterable[Index]:
        for index, item in self.items():
            yield index

    def items(self) -> Iterable[Tuple[Index, V]]:
        for y, line in enumerate(self.contents):
            for x, item in enumerate(line):
                if item != self.whitespace:
                    yield (x, y), item

    def values(self) -> Iterable[V]:
        for index, item in self.items():
            yield item

    def get(self, key: Index, default: D = None) -> Union[V, D]:
        value = self[key]

        if value == self.whitespace:
            return default

        return value

    @classmethod
    def from_string(cls, s: str, whitespace: str = " ") -> "Diagram[str]":
        return cls(contents=char_matrix(s), whitespace=whitespace)
