from abc import abstractmethod
from typing import Optional, Protocol

from pdfscript.__spi__.styles import TextStyle, ImageStyle, LineStyle, RectStyle
from pdfscript.__spi__.types import Number, PDFCoords, Space, BoundingBox


class PDFOpset(Protocol):

    @abstractmethod
    def add_text(self, text: str, coords: PDFCoords, styling: TextStyle):
        pass

    @abstractmethod
    def add_image(self, src: str, coords: PDFCoords, styling: ImageStyle):
        pass

    @abstractmethod
    def draw_line(self, x1: Number, y1: Number, x2: Number, y2: Number, style: LineStyle = LineStyle()):
        pass

    @abstractmethod
    def draw_rect(self, x1: Number, y1: Number, x2: Number, y2: Number, style: RectStyle = RectStyle()):
        pass

    @abstractmethod
    def get_width_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        pass

    @abstractmethod
    def get_height_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        pass

    @abstractmethod
    def add_page(self):
        pass


class PDFListener(Protocol):

    @abstractmethod
    def on_space(self, space: Space):
        pass

    @abstractmethod
    def on_instr(self, bbox: BoundingBox):
        pass
