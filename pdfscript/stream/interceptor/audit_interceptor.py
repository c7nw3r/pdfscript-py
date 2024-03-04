from typing import Optional

from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.styles import TextStyle, LineStyle, ImageStyle
from pdfscript.__spi__.types import Number, BoundingBox


class AuditInterceptor(PDFApi):

    def __init__(self):
        super().__init__()
        self.audit_log = []

    def add_text(self, text: str, box: BoundingBox, styling: TextStyle):
        self.audit_log.append(f'add_text("{text}", {box.x}, {box.y}, {styling})')

    def add_image(self, src: str, box: BoundingBox, styling: ImageStyle):
        self.audit_log.append(f'add_image("{src[src.rfind("/") + 1:]}", {box.x}, {box.y}, {styling})')

    def draw_line(self, x1: Number, y1: Number, x2: Number, y2: Number, style: LineStyle = LineStyle()):
        self.audit_log.append(f"draw_line({x1}, {y1}, {x2}, {y2}, {style})")

    def get_width_of_text(self, text: str, font_name: str, font_size: int, consider_overflow: bool = True):
        pass

    def get_height_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
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
