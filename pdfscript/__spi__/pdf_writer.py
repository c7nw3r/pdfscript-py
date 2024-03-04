from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_writable import PDFEvaluations
from pdfscript.__spi__.pdf_writer_api import PDFWriterApi, Configurer
from pdfscript.__spi__.styles import ImageStyle, VStackStyle, HStackStyle, TableStyle
from pdfscript.stream.writable.image import Image
from pdfscript.stream.writable.table.table_row_writer import TableRowConfigurer
from pdfscript.stream.writable.text import TextStyle, Text


class PDFWriter(PDFWriterApi):

    def __init__(self, context: PDFContext):
        self.context = context
        self.objects = []

    def text(self, content: str, style: TextStyle = TextStyle()):
        self.objects.append(Text(content, style))

    def image(self, src: str, style: ImageStyle = ImageStyle()):
        self.objects.append(Image(src, style))

    def vstack(self, configurer: Configurer, style: HStackStyle = HStackStyle()):
        from pdfscript.stream.writable.vstack import VStack
        self.objects.append(VStack(configurer, style))

    def hstack(self, configurer: Configurer, style: VStackStyle = VStackStyle()):
        from pdfscript.stream.writable.hstack import HStack
        self.objects.append(HStack(configurer, style))

    def table(self, configurer: TableRowConfigurer, style: TableStyle = TableStyle()):
        from pdfscript.stream.writable.table.table import Table
        self.objects.append(Table(configurer, style))

    def write(self) -> PDFEvaluations:
        return PDFEvaluations([e.evaluate(self.context) for e in self.objects])
