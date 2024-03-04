from typing import Optional

from pdfscript.__spi__.pdf_opset import PDFOpset
from pdfscript.__spi__.styles import TextStyle, ImageStyle, LineStyle
from pdfscript.__spi__.types import Number, PDFPosition


class DevNullInterceptor(PDFOpset):

    def add_text(self, text: str, box: PDFPosition, styling: TextStyle):
        pass

    def add_image(self, src: str, box: PDFPosition, styling: ImageStyle):
        pass

    def draw_line(self, x1: Number, y1: Number, x2: Number, y2: Number, style: LineStyle = LineStyle()):
        pass

    def get_width_of_text(self, text: str, font_name: str, font_size: int, consider_overflow: bool = True):
        pass

    def get_height_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        pass

    def add_page(self):
        pass
