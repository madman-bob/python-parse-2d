from dataclasses import dataclass
from typing import FrozenSet, Set

from parse_2d.diagram import Index

__all__ = ["Region", "TinyRegion", "RectRegion", "SparseRegion"]

Region = Set[Index]


@dataclass(frozen=True)
class TinyRegion(Region):
    location: Index

    def __contains__(self, item: Index) -> bool:
        return item == self.location

    def __iter__(self):
        yield self.location

    def __len__(self):
        return 1


@dataclass(frozen=True)
class RectRegion(Region):
    top_left: Index
    bottom_right: Index

    def __contains__(self, item: Index) -> bool:
        min_x, min_y = self.top_left
        max_x, max_y = self.bottom_right
        x, y = item

        return min_x <= x < max_x and min_y <= y < max_y

    def __iter__(self):
        min_x, min_y = self.top_left
        max_x, max_y = self.bottom_right

        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                yield x, y

    def __len__(self):
        min_x, min_y = self.top_left
        max_x, max_y = self.bottom_right

        return (max_y - min_y) * (max_x - min_x)


@dataclass(frozen=True)
class SparseRegion(Region):
    contents: FrozenSet[Index]

    def __contains__(self, item: Index) -> bool:
        return item in self.contents

    def __iter__(self):
        yield from self.contents

    def __len__(self):
        return len(self.contents)
