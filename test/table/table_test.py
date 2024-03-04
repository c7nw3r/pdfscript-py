from unittest import TestCase

from pdfscript.__spi__.styles import TableColStyle, LineStyle, TableRowStyle
from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from test import get_local_dir


class TableTest(TestCase):

    def test_table(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        table = script.table()
        row1 = table.row()
        row1.col().text("abcd" * 10)
        row1.col().text("abcd" * 10)
        row1.col().text("abcd" * 10)

        row2 = table.row()
        row2.col().text("abcd" * 10)
        row2.col().text("abcd" * 10)
        row2.col().text("abcd" * 10)

        row3 = table.row()
        row3.col().text("abcd" * 10)
        row3.col().text("abcd" * 10)
        row3.col().text("abcd" * 10)

        script.execute("table.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_table.txt")

    def test_table_without_border(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        row_style = TableRowStyle(gap=20)
        col_style = TableColStyle(border=LineStyle("black"), gap=20)

        table = script.table()
        row1 = table.row(row_style)
        row1.col(col_style).text("abcd" * 10)
        row1.col(col_style).text("abcd" * 10)
        row1.col(col_style).text("abcd" * 10)

        row2 = table.row(row_style)
        row2.col(col_style).text("abcd" * 10)
        row2.col(col_style).text("abcd" * 10)
        row2.col(col_style).text("abcd" * 10)

        row3 = table.row(row_style)
        row3.col(col_style).text("abcd" * 10)
        row3.col(col_style).text("abcd" * 10)
        row3.col(col_style).text("abcd" * 10)

        script.execute("table.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_table_without_border.txt")
