from typing import Optional

from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.pdf_context import PDFContext, PageMargin, PageFormat
from pdfscript.__spi__.pdf_font_registry import PDFFontRegistry
from pdfscript.__spi__.pdf_interceptor import DevNullInterceptor
from pdfscript.__spi__.pdf_writable import PDFEvaluations
from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.__spi__.pdf_writer_api import Configurer
from pdfscript.__spi__.styles import ImageStyle, VStackStyle, HStackStyle, TableStyle, LineStyle
from pdfscript.__spi__.types import BoundingBox
from pdfscript.pdf_script_stream import PDFScriptStream
from pdfscript.stream.writable.table.table_row_writer import TableRowConfigurer
from pdfscript.stream.writable.text import TextStyle
from reportlab.pdfgen import canvas


class PDFScript:
    def __init__(self, context: PDFContext):
        self.context = context
        self.font_registry = PDFFontRegistry()
        self.header_writer = PDFWriter(context)
        self.center_writer = PDFWriter(context)
        self.footer_writer = PDFWriter(context)
        self.canvas_writer = PDFWriter(context)

    @staticmethod
    def a4(margin: PageMargin = PageMargin.default()):
        return PDFScript(PDFContext(PageFormat.A4, margin))

    def text(self, content: str, style: TextStyle = TextStyle()):
        self.center_writer.text(content, style)

    def image(self, src: str, style: ImageStyle = ImageStyle()):
        self.center_writer.image(src, style)

    def vstack(self, configurer: Configurer, style: VStackStyle = VStackStyle()):
        self.center_writer.vstack(configurer, style)

    def hstack(self, configurer: Configurer, style: HStackStyle = HStackStyle()):
        self.center_writer.hstack(configurer, style)

    def table(self, configurer: TableRowConfigurer, style: TableStyle = TableStyle()):
        self.center_writer.table(configurer, style)

    def execute(self, path: str, interceptor: PDFApi = DevNullInterceptor()):
        file_name = path[max(0, path.rfind("/")):]
        document = canvas.Canvas(file_name)

        stream = PDFScriptStream(document, self.context, interceptor)

        width, height = self.context.page_format.value
        t, b, l, r, h, f = self.context.page_margin

        header_eval = self.header_writer.write()
        center_eval = self.center_writer.write()
        footer_eval = self.footer_writer.write()
        canvas_eval = self.canvas_writer.write()

        hh = self._calc_height(header_eval, stream, width - r)
        ch = self._calc_height(center_eval, stream, width - r)
        fh = self._calc_height(footer_eval, stream, width - r)

        hy = min(height - t, height - (hh + h))
        fy = min(b, fh + f)

        # stream.draw_line(0, hy, width, hy, LineStyle(stroke_color="red"))

        available_center_height = height - hy - fy
        # stream.putPDFValue("totalPages", Math.max(Math.ceil(ch / availableCenterHeight), 1))

        def render_header():
            box = BoundingBox(l, h, l, h, width - r, hh)
            return header_eval.execute(stream, box)

        def render_center():
            box = BoundingBox(l, hy, l, fy, width - r, hy)
            return center_eval.execute(stream, box)

        def render_footer():
            box = BoundingBox(l, height - fh - f, l, height - fh - f, width - r, height - f)
            return footer_eval.execute(stream, box)

        def render_canvas():
            box = BoundingBox(0, 0, 0, 0, width, height)
            return canvas_eval.execute(stream, box)

        render_header()
        render_center()
        render_footer()
        render_canvas()

        document.save()

    def _calc_height(self, evals: PDFEvaluations, stream: PDFScriptStream, max_x: int):
        zero = BoundingBox(0, 0, 0, 0, max_x, 1000)
        return sum([e.space(stream, zero).height for e in evals])