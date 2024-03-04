from typing import Callable

from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_writable import PDFEvaluations
from pdfscript.__spi__.styles import TableColStyle

TableColConfigurer = Callable[['TableColWriter'], None]


class TableColWriter:

    def __init__(self, context: PDFContext):
        self.context = context
        self.objects = []

    def write(self) -> PDFEvaluations:
        return PDFEvaluations([e.evaluate(self.context) for e in self.objects])

    def col(self, style: TableColStyle = TableColStyle()):
        from pdfscript.__spi__.pdf_writer import PDFWriter
        configurer = PDFWriter(self.context)
        from pdfscript.stream.writable.table.table_col import TableCol
        self.objects.append(TableCol(configurer, style))
        return configurer
