from typing import Optional

from pdfscript.__spi__.protocols import PDFOpset
from pdfscript.__spi__.styles import TextStyle, RectStyle, LineStyle, ImageStyle
from pdfscript.__spi__.types import PDFPosition, Number, PDFCoords


class PDFOpsetAdapter(PDFOpset):

    def __init__(self, opset: PDFOpset):
        self.opset = opset

    def add_text(self, text: str, coords: PDFCoords, styling: TextStyle):
        self.opset.add_text(text, coords, styling)

    def add_image(self, src: str, coords: PDFCoords, styling: ImageStyle):
        self.opset.add_image(src, coords, styling)

    def draw_line(self, x1: Number, y1: Number, x2: Number, y2: Number, style: LineStyle = LineStyle()):
        self.opset.draw_line(x1, y1, x2, y2, style)

    def draw_rect(self, x1: Number, y1: Number, x2: Number, y2: Number, style: RectStyle = RectStyle()):
        self.opset.draw_rect(x1, y1, x2, y2, style)

    def get_width_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        return self.opset.get_width_of_text(text, style, max_x)

    def get_height_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        return self.opset.get_height_of_text(text, style, max_x)

    def split_text_by_height(self, text: str, style: TextStyle, pos: PDFPosition):
        return self.opset.split_text_by_height(text, style, pos)

    def add_page(self):
        self.opset.add_page()

    def page(self):
        self.opset.page()
