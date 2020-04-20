from dataclasses import dataclass
from enum import Enum

from more_properties import cached_class_property

__all__ = ["Translation", "Directions"]


@dataclass(frozen=True)
class Translation:
    x: int
    y: int

    @classmethod
    def between(cls, start, end):
        start_x, start_y = start
        end_x, end_y = end

        return cls(end_x - start_x, end_y - start_y)

    def __radd__(self, other):
        return self.x + other[0], self.y + other[1]

    def __neg__(self):
        return Translation(-self.x, -self.y)


class Directions(Enum):
    UP = Translation(0, -1)
    UP_RIGHT = Translation(1, -1)
    RIGHT = Translation(1, 0)
    DOWN_RIGHT = Translation(1, 1)
    DOWN = Translation(0, 1)
    DOWN_LEFT = Translation(-1, 1)
    LEFT = Translation(-1, 0)
    UP_LEFT = Translation(-1, -1)

    @cached_class_property
    def vertical(cls):
        return cls.UP.value, cls.DOWN.value

    @cached_class_property
    def horizontal(cls):
        return cls.LEFT.value, cls.RIGHT.value

    @cached_class_property
    def all(cls):
        return tuple(item.value for item in cls)
