from typing import Optional

from pdfscript.__spi__.protocols import PDFOpset
from pdfscript.__spi__.styles import TextStyle, LineStyle, ImageStyle, RectStyle
from pdfscript.__spi__.types import Number, PDFCoords, PDFPosition


class AuditInterceptor(PDFOpset):

    def __init__(self):
        super().__init__()
        self.audit_log = []

    def add_text(self, text: str, box: PDFCoords, styling: TextStyle):
        self.audit_log.append(f'add_text("{text}", {box.x}, {box.y}, {styling})')

    def add_image(self, src: str, box: PDFCoords, styling: ImageStyle):
        self.audit_log.append(f'add_image("{src[src.rfind("/") + 1:]}", {box.x}, {box.y}, {styling})')

    def draw_line(self, x1: Number, y1: Number, x2: Number, y2: Number, style: LineStyle = LineStyle()):
        self.audit_log.append(f"draw_line({x1}, {y1}, {x2}, {y2}, {style})")

    def draw_rect(self, x1: Number, y1: Number, x2: Number, y2: Number, style: RectStyle = RectStyle()):
        self.audit_log.append(f"draw_rect({x1}, {y1}, {x2}, {y2}, {style})")

    def get_width_of_text(self, text: str, font_name: str, font_size: int, consider_overflow: bool = True):
        pass

    def get_height_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        pass

    def split_text_by_height(self, text: str, style: TextStyle, pos: PDFPosition):
        pass

    def add_page(self):
        self.audit_log.append("add_page")

    def __iter__(self):
        for e in self.audit_log:
            yield e

    def __repr__(self):
        return "\n".join(self)

    def save(self, path: str):
        with open(path, "w") as file:
            file.write(str(self))

    def verify(self, path: str):
        with open(path, "r") as file:
            to_compare = file.readlines()

        from unittest import TestCase
        for a, b in zip(to_compare, self.audit_log):
            TestCase().assertEquals(a.strip(), b.strip())
