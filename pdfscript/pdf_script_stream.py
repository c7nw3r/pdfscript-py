from typing import Optional

from reportlab.pdfgen.canvas import Canvas

from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.styles import ImageStyle, LineStyle
from pdfscript.__spi__.types import BoundingBox, Number
from pdfscript.stream.writable.text import TextStyle


class PDFScriptStream(PDFApi):

    def __init__(self, canvas: Canvas, context: PDFContext, interceptor: PDFApi):
        self.canvas = canvas
        self.context = context
        self.interceptor = interceptor

    def add_text(self, text: str, box: BoundingBox, style: TextStyle):
        self.interceptor.add_text(text, box, style)

        from reportlab.platypus import Paragraph
        paragraph = Paragraph(text, style.to_paragraph_style())

        w, h = paragraph.wrap(box.max_x - box.x, box.y - box.min_y)
        paragraph.drawOn(self.canvas, box.x, box.y - h)

    def add_image(self, src: str, box: BoundingBox, style: ImageStyle):
        self.interceptor.add_image(src, box, style)
        self.canvas.drawImage(src, box.x, box.y - style.height, style.width, style.height, mask="auto")

    def draw_line(self, x1: Number, y1: Number, x2: Number, y2: Number, style: LineStyle = LineStyle()):
        self.interceptor.draw_line(x1, y1, x2, y2, style)

        if style.stroke_color:
            self.canvas.setStrokeColor(style.stroke_color, style.stroke_opacity)

        self.canvas.line(x1, y1, x2, y2)

        if style.stroke_color:
            self.canvas.setStrokeColor("black", 1)

    def get_width_of_text(self, text: str, font_name: str, font_size: int, consider_overflow: bool = True):
        self.interceptor.get_width_of_text(text, font_name, font_size, consider_overflow)

        from reportlab.pdfbase.pdfmetrics import stringWidth
        max_x, _ = self.context.page_format.value
        width = stringWidth(text, font_name, font_size)

        return min(width, max_x) if consider_overflow else width

    def get_height_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        self.interceptor.get_height_of_text(text, style, max_x)

        import math
        from reportlab.pdfbase import pdfmetrics

        max_x = max_x or self.context.page_format.value[0]
        width = self.get_width_of_text(text, style.font_name, style.font_size, consider_overflow=False)
        lines = math.ceil(width / max_x)

        face = pdfmetrics.getFont(style.font_name).face
        return ((face.ascent - face.descent) / 1000 * style.font_size) * lines

    def add_page(self):
        self.interceptor.add_page()
        # TODO: render_header
        # TODO: render_footer
        self.canvas.showPage()
