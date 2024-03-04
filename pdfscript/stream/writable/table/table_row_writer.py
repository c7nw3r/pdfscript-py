from typing import Callable

from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_writable import PDFEvaluations
from pdfscript.__spi__.styles import TableRowStyle
from pdfscript.stream.writable.table.table_col_writer import TableColWriter

TableRowConfigurer = Callable[['TableRowWriter'], None]


class TableRowWriter:

    def __init__(self, context: PDFContext):
        self.context = context
        self.objects = []

    def write(self) -> PDFEvaluations:
        return PDFEvaluations([e.evaluate(self.context) for e in self.objects])

    def row(self, style: TableRowStyle = TableRowStyle()):
        from pdfscript.stream.writable.table.table_row import TableRow

        configurer = TableColWriter(self.context)
        self.objects.append(TableRow(configurer, style))
        return configurer
