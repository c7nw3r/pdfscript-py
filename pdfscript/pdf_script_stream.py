from typing import Optional

from reportlab.pdfgen.canvas import Canvas

from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.protocols import PDFOpset
from pdfscript.__spi__.styles import ImageStyle, LineStyle, RectStyle
from pdfscript.__spi__.types import Number, PDFCoords, PDFPosition, TextChunk
from pdfscript.stream.writable.text import TextStyle


class PDFScriptStream(PDFOpset):

    def __init__(self, canvas: Canvas, context: PDFContext, interceptor: PDFOpset):
        self.page_num = 0
        self.canvas = canvas
        self.context = context
        self.interceptor = interceptor

    def add_text(self, text: str, box: PDFCoords, style: TextStyle):
        self.interceptor.add_text(text, box, style)

        from reportlab.platypus import Paragraph
        paragraph = Paragraph(text, style.to_paragraph_style())

        w, h = paragraph.wrap(box.max_x - box.x, box.y - box.min_y)
        paragraph.drawOn(self.canvas, box.x, box.y - h)

    def add_image(self, src: str, box: PDFCoords, style: ImageStyle):
        self.interceptor.add_image(src, box, style)
        self.canvas.drawImage(src, box.x, box.y - style.height, style.width, style.height, mask="auto")

    def draw_line(self, x1: Number, y1: Number, x2: Number, y2: Number, style: LineStyle = LineStyle()):
        self.interceptor.draw_line(x1, y1, x2, y2, style)

        if style.stroke_color:
            self.canvas.setStrokeColor(style.stroke_color, style.stroke_opacity)

        self.canvas.line(x1, y1, x2, y2)

        if style.stroke_color:
            self.canvas.setStrokeColor("black", 1)

    def draw_rect(self, x1: Number, y1: Number, x2: Number, y2: Number, style: RectStyle = RectStyle()):
        self.interceptor.draw_rect(x1, y1, x2, y2, style)

        if style.stroke_color:
            self.canvas.setStrokeColor(style.stroke_color, style.stroke_opacity)
        if style.fill_color:
            self.canvas.setFillColor(style.fill_color, style.fill_opacity)

        self.canvas.rect(x1, y1, x2 - x1, y2 - y1, fill=style.fill_color is not None)

        if style.stroke_color:
            self.canvas.setStrokeColor("black", 1)
        if style.stroke_color:
            self.canvas.setStrokeColor("white", 0)

    def get_width_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        self.interceptor.get_width_of_text(text, style, max_x)

        from reportlab.pdfbase.pdfmetrics import stringWidth
        if max_x is None:
            max_x, _ = self.context.format.value
        width = stringWidth(text, style.font_name, style.font_size)

        return min(width, max_x)

    def get_height_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        self.interceptor.get_height_of_text(text, style, max_x)
        max_x = max_x or self.context.format.value[0]

        from reportlab.platypus import Paragraph
        paragraph = Paragraph(text, style.to_paragraph_style())

        _, h = paragraph.wrap(max_x, self.context.format.value[1])
        return h

    # TODO: make more performant
    def split_text_by_height(self, text: str, style: TextStyle, pos: PDFPosition):
        necessary_height = self.get_height_of_text(text, style, pos.max_x - pos.x)
        available_height = pos.y - pos.min_y

        if pos.y <= pos.min_y:
            return None, TextChunk(text, necessary_height)

        chunk_height = necessary_height
        all_tokens = text.split(" ")
        tokens = text.split(" ")

        split_pos = None
        while chunk_height > available_height:
            split_pos = len(tokens) - 10
            tokens = tokens[:split_pos]
            chunk = " ".join(tokens)

            chunk_height = self.get_height_of_text(chunk, style, pos.max_x - pos.x)

        if split_pos is None:
            return [TextChunk(text, necessary_height), None]
        elif split_pos <= 0:
            return [None, TextChunk(text, chunk_height)]
        return [
            TextChunk(" ".join(all_tokens[:split_pos]), chunk_height),
            TextChunk(" ".join(all_tokens[split_pos:]), available_height - chunk_height)
        ]

    def add_page(self):
        self.interceptor.add_page()
        # TODO: render_header
        # TODO: render_footer
        self.canvas.showPage()
        self.page_num += 1

    def page(self):
        return self.page_num
