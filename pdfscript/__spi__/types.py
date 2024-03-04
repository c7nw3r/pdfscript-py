from dataclasses import dataclass
from typing import Optional, Union

Number = Union[int, float]


@dataclass
class Space:
    width: float
    height: float

    def __iter__(self):
        yield self.width
        yield self.height


class PDFPosition:
    def __init__(self, x: int, y: int, min_x: int, min_y: int, max_x: int, max_y: int):
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
    top: Optional[float]
    right: Optional[float]
    bottom: Optional[float]
    left: Optional[float]
