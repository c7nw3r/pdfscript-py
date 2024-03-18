from typing import Optional

from pdfscript.__spi__.protocols import PDFOpset
from pdfscript.__spi__.styles import TextStyle, ImageStyle, LineStyle, RectStyle
from pdfscript.__spi__.types import Number, PDFCoords, PDFPosition


class NoOpInterceptor(PDFOpset):

    def add_text(self, text: str, box: PDFCoords, styling: TextStyle):
        pass

    def add_image(self, src: str, box: PDFCoords, styling: ImageStyle):
        pass

    def draw_line(self, x1: Number, y1: Number, x2: Number, y2: Number, style: LineStyle = LineStyle()):
        pass

    def draw_rect(self, x1: Number, y1: Number, x2: Number, y2: Number, style: RectStyle = RectStyle()):
        pass

    def get_width_of_text(self, text: str, font_name: str, font_size: int, consider_overflow: bool = True):
        pass

    def split_text_by_height(self, text: str, style: TextStyle, pos: PDFPosition):
        pass

    def get_height_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        pass

    def add_page(self):
        pass

    def page(self):
        pass
