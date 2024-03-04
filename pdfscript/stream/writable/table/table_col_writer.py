from typing import Callable

from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_writable import PDFEvaluations
from pdfscript.__spi__.pdf_writer_api import Configurer
from pdfscript.__spi__.styles import TableStyle, TableColStyle

TableColConfigurer = Callable[['TableColWriter'], None]

class TableColWriter:

    def __init__(self, context: PDFContext):
        self.context = context
        self.objects = []

    def write(self) -> PDFEvaluations:
        return PDFEvaluations([e.evaluate(self.context) for e in self.objects])

    def col(self, configurer: Configurer, style: TableColStyle = TableColStyle()):
        from pdfscript.stream.writable.table.table_col import TableCol
        self.objects.append(TableCol(configurer, style))
