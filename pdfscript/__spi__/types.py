from dataclasses import dataclass
from typing import Union

Number = Union[int, float]


@dataclass
class Space:
    width: float
    height: float

    def __iter__(self):
        yield self.width
        yield self.height


@dataclass
class PDFCoords:
    x: Number
    y: Number


class PDFPosition(PDFCoords):
    def __init__(self, x: int, y: int, min_x: int, min_y: int, max_x: int, max_y: int):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def copy(self):
        return PDFPosition(self.x, self.y, self.min_x, self.min_y, self.max_x, self.max_y)

    def move_x_offset(self, amount: Number = 0):
        pass

    def move_y_offset(self, amount: Number = 0):
        pass

    def move_to(self, x: Number, y: Number):
        self.x = x
        self.y = y
        return self

    def with_x_offset(self, amount: Number = 0):
        return PDFPosition(self.x + amount, self.y, self.min_x, self.min_y, self.max_x, self.max_y)

    def with_max_x(self, amount: Number = 0):
        return PDFPosition(self.x, self.y, self.min_x, self.min_y, amount, self.max_y)

    def with_max_y(self, amount: Number = 0):
        return PDFPosition(self.x, self.y, self.min_x, self.min_y, self.max_x, amount)

    def __iter__(self):
        yield self.x
        yield self.y


@dataclass
class Margin:
    """
    Dataclass used to specify the amount of margin of a writable.
    """

    top: Number = 0
    right: Number = 0
    bottom: Number = 0
    left: Number = 0

    def __iter__(self):
        yield self.top
        yield self.right
        yield self.bottom
        yield self.left
