from abc import ABC, abstractmethod
from typing import Optional, Protocol

from pdfscript.__spi__.styles import TextStyle, ImageStyle, LineStyle
from pdfscript.__spi__.types import BoundingBox, Number


class PDFApi(Protocol):

    @abstractmethod
    def add_text(self, text: str, box: BoundingBox, styling: TextStyle):
        pass

    @abstractmethod
    def add_image(self, src: str, box: BoundingBox, styling: ImageStyle):
        pass

    def draw_line(self, x1: Number, y1: Number, x2: Number, y2: Number, style: LineStyle = LineStyle()):
        pass

    @abstractmethod
    def get_width_of_text(self, text: str, font_name: str, font_size: int, consider_overflow: bool = True):
        pass

    @abstractmethod
    def get_height_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        pass

    @abstractmethod
    def add_page(self):
        pass
