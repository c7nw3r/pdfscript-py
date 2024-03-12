from io import BytesIO

from reportlab.pdfgen import canvas

from pdfscript.__spi__.pdf_context import PDFContext, PageMargin, PageFormat
from pdfscript.__spi__.pdf_writable import PDFEvaluations
from pdfscript.__spi__.pdf_writer import PDFWriter, PDFCanvas
from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.styles import ImageStyle, VStackStyle, HStackStyle, RectStyle, ParagraphStyle, \
    DEFAULT_TITLE_STYLE
from pdfscript.__spi__.types import PDFPosition, Number
from pdfscript.pdf_script_stream import PDFScriptStream
from pdfscript.stream.interceptor.noop_interceptor import NoOpInterceptor
from pdfscript.stream.listener.noop_listener import NoOpListener
from pdfscript.stream.writable.table.table_row_writer import TableRowWriter
from pdfscript.stream.writable.text import TextStyle


class PDFScript:
    def __init__(self, context: PDFContext):
        self.context = context
        self.header_writer = PDFWriter(context)
        self.center_writer = PDFWriter(context)
        self.footer_writer = PDFWriter(context)
        self.canvas_writer = PDFCanvas(context)

    @staticmethod
    def a4(margin: PageMargin = PageMargin.default()):
        return PDFScript(PDFContext(PageFormat.A4, margin))

    def text(self, content: str, style: TextStyle = TextStyle(), listener: PDFListener = NoOpListener()):
        self.center_writer.text(content, style, listener)

    def bold(self, content: str, style: TextStyle = TextStyle(), listener: PDFListener = NoOpListener()):
        self.center_writer.bold(content, style, listener)

    def paragraph(self, content: str, style: ParagraphStyle = ParagraphStyle(), listener: PDFListener = NoOpListener()):
        self.center_writer.paragraph(content, style, listener)

    def title1(self, content: str, style: TextStyle = DEFAULT_TITLE_STYLE, listener: PDFListener = NoOpListener):
        self.center_writer.title1(content, style, listener)

    def title2(self, content: str, style: TextStyle = DEFAULT_TITLE_STYLE, listener: PDFListener = NoOpListener):
        self.center_writer.title2(content, style, listener)

    def title3(self, content: str, style: TextStyle = DEFAULT_TITLE_STYLE, listener: PDFListener = NoOpListener):
        self.center_writer.title3(content, style, listener)

    def image(self, src: str, style: ImageStyle = ImageStyle()):
        self.center_writer.image(src, style)

    def v_stack(self, style: VStackStyle = VStackStyle()):
        configurer = PDFWriter(self.context)
        self.center_writer.v_stack(configurer, style)
        return configurer

    def h_stack(self, style: HStackStyle = HStackStyle()):
        configurer = PDFWriter(self.context)
        self.center_writer.h_stack(configurer, style)
        return configurer

    def table(self):
        configurer = TableRowWriter(self.context)
        self.center_writer.table(configurer)
        return configurer

    def rect(self, x1: Number, y1: Number, x2: Number, y2: Number, style: RectStyle = RectStyle()):
        self.canvas_writer.draw_rect(x1, y1, x2, y2, style)

    def with_header(self):
        return self.header_writer

    def with_footer(self):
        return self.footer_writer

    def with_canvas(self):
        return self.canvas_writer

    def render_as_stream(self, interceptor: PDFOpset = NoOpInterceptor()):
        buf = BytesIO()
        document = canvas.Canvas(buf)

        self._render(document, interceptor)

        buf.seek(0)
        return buf.read()

    def render_as_file(self, path: str, interceptor: PDFOpset = NoOpInterceptor()):
        file_name = path[max(0, path.rfind("/")):]
        document = canvas.Canvas(file_name)
        self._render(document, interceptor)

        with open(path, "r") as file:
            return file

    def _render(self, document: canvas.Canvas, interceptor: PDFOpset = NoOpInterceptor()):
        stream = PDFScriptStream(document, self.context, interceptor)

        width, height = self.context.format.value
        t, b, l, r, _, _ = self.context.margin

        header_eval = self.header_writer.write()
        center_eval = self.center_writer.write()
        footer_eval = self.footer_writer.write()
        canvas_eval = self.canvas_writer.write()

        hh = self._calc_height(header_eval, stream)
        # ch = self._calc_height(center_eval, stream)
        fh = self._calc_height(footer_eval, stream)

        hy = min(height - t, height - (hh + self.context.margin.header))
        fy = min(b, fh + self.context.margin.footer)

        # stream.draw_line(0, hy, width, hy, LineStyle(stroke_color="red"))
        # available_center_height = height - hy - fy
        # stream.putPDFValue("totalPages", Math.max(Math.ceil(ch / availableCenterHeight), 1))

        def render_header():
            h_margin = self.context.margin.header
            pos = PDFPosition(l, height - h_margin, l, height - h_margin - hh, width - r, height - h_margin)
            return header_eval.execute(stream, pos)

        def render_center():
            pos = PDFPosition(l, hy, l, fy, width - r, hy)
            return center_eval.execute(stream, pos)

        def render_footer():
            f_margin = self.context.margin.footer
            pos = PDFPosition(l, fh + f_margin, l, f_margin, width - r, height + f_margin)
            return footer_eval.execute(stream, pos)

        def render_canvas():
            pos = PDFPosition(0, 0, 0, 0, width, height)
            return canvas_eval.execute(stream, pos)

        render_header()
        render_center()
        render_footer()
        render_canvas()

        document.save()

    def _calc_height(self, evals: PDFEvaluations, stream: PDFScriptStream):
        width, height = self.context.format.value
        t, b, l, r, _, _ = self.context.margin
        zero = PDFPosition(l, 0, l, 0, width - r, 1000)
        return sum([e.space(stream, zero).height for e in evals])
