from unittest import TestCase

from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.__spi__.pdf_writer_api import PDFWriterApi
from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from pdfscript.stream.writable.table.table_col_writer import TableColWriter
from pdfscript.stream.writable.table.table_row_writer import TableRowWriter


class TableTest(TestCase):

    def test_table(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        def col(writer: PDFWriterApi):
            writer.text("abcd" * 10)

        def row(col_writer: TableColWriter):
            col_writer.col(col)
            col_writer.col(col)
            col_writer.col(col)

        def table(writer: TableRowWriter):
            writer.row(row)
            writer.row(row)
            writer.row(row)

        script.table(table)
        # script.text("abcd")

        script.execute("table.pdf", interceptor)
        interceptor.verify("./test_table.txt")
