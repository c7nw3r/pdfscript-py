from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_writable import PDFEvaluations
from pdfscript.__spi__.protocols import PDFListener
from pdfscript.__spi__.styles import ImageStyle, VStackStyle, HStackStyle, LineStyle, RectStyle, ParagraphStyle
from pdfscript.__spi__.types import Number
from pdfscript.stream.listener.noop_listener import NoOpListener
from pdfscript.stream.writable.bold import Bold
from pdfscript.stream.writable.canvas.canvas_image import CanvasImage
from pdfscript.stream.writable.canvas.canvas_line import CanvasLine
from pdfscript.stream.writable.canvas.canvas_rect import CanvasRect
from pdfscript.stream.writable.canvas.canvas_text import CanvasText
from pdfscript.stream.writable.image import Image
from pdfscript.stream.writable.list.list_items_writer import ListItemsWriter
from pdfscript.stream.writable.paragraph import Paragraph
from pdfscript.stream.writable.table.table_row_writer import TableRowWriter
from pdfscript.stream.writable.text import TextStyle, Text
from pdfscript.stream.writable.title import Title


class PDFCanvas:
    def __init__(self, context: PDFContext):
        self.context = context
        self.objects = []

    def draw_line(self, x: Number, y: Number, w: Number, h: Number, style: LineStyle = LineStyle()):
        self.objects.append(CanvasLine(x, y, w, h, style))

    def draw_rect(self, x: Number, y: Number, w: Number, h: Number, style: RectStyle = RectStyle()):
        self.objects.append(CanvasRect(x, y, w, h, style))

    def draw_image(self, src: str, x: Number, y: Number, style: ImageStyle = ImageStyle()):
        self.objects.append(CanvasImage(src, x, y, style))

    def draw_text(self, text: str, x: Number, y: Number, style: TextStyle = TextStyle()):
        self.objects.append(CanvasText(text, x, y, style))

    def write(self) -> PDFEvaluations:
        return PDFEvaluations([e.evaluate(self.context) for e in self.objects])


class PDFWriter(PDFCanvas):

    def __init__(self, context: PDFContext):
        super().__init__(context)

    def text(self, content: str, style: TextStyle = TextStyle(), listener: PDFListener = NoOpListener()):
        self.objects.append(Text(content, style, listener))

    def bold(self, content: str, style: TextStyle = TextStyle(), listener: PDFListener = NoOpListener()):
        self.objects.append(Bold(content, style, listener))

    def title1(self, content: str, style: TextStyle = TextStyle(), listener: PDFListener = NoOpListener()):
        self.objects.append(Title(content, style, order=1, listener=listener))

    def title2(self, content: str, style: TextStyle = TextStyle(), listener: PDFListener = NoOpListener()):
        self.objects.append(Title(content, style, order=2, listener=listener))

    def title3(self, content: str, style: TextStyle = TextStyle(), listener: PDFListener = NoOpListener()):
        self.objects.append(Title(content, style, order=3, listener=listener))

    def paragraph(self, content: str, style: ParagraphStyle = ParagraphStyle(), listener: PDFListener = NoOpListener()):
        self.objects.append(Paragraph(content, style, listener))

    def image(self, src: str, style: ImageStyle = ImageStyle()):
        self.objects.append(Image(src, style))

    def v_stack(self, configurer: 'PDFWriter', style: VStackStyle = VStackStyle()):
        from pdfscript.stream.writable.vstack import VStack
        self.objects.append(VStack(configurer, style))

    def h_stack(self, configurer: 'PDFWriter', style: HStackStyle = HStackStyle()):
        from pdfscript.stream.writable.hstack import HStack
        self.objects.append(HStack(configurer, style))

    def table(self, configurer: TableRowWriter, listener: PDFListener = NoOpListener()):
        from pdfscript.stream.writable.table.table import Table
        self.objects.append(Table(configurer, listener))

    def list_items(self, configurer: ListItemsWriter):
        from pdfscript.stream.writable.list.list_items import ListItems
        self.objects.append(ListItems(configurer))

    def write(self) -> PDFEvaluations:
        return PDFEvaluations([e.evaluate(self.context) for e in self.objects])
