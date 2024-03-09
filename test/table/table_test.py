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

        script.render_as_file("table.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_table.txt")

    def test_table_without_border(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        row_style = TableRowStyle()
        col_style = TableColStyle(border=LineStyle("white"), gap=5)

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

        script.render_as_file("table.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_table_without_border.txt")

    def test_paragraph_and_table(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        script.paragraph("abcd" * 10)

        table = script.table()
        row1 = table.row()
        row1.col(TableColStyle(gap=10)).text("The Foundation has grown rapidly throughout its existence. By 2022, it employed around 700 staff")
        row1.col(TableColStyle(gap=10)).text("and contractors, with annual revenues of $155 million, annual expenses of $146 million, net assets")
        row1.col(TableColStyle(gap=10)).text("of $240 million and a growing endowment, which surpassed $100 million in June 2021.")

        script.paragraph("abcd" * 10)

        script.render_as_file("table.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph_and_table.txt")

    # def test_table_overflow(self):
    #     interceptor = AuditInterceptor()
    #     script = PDFScript.a4()
    #
    #     script.paragraph("abcd" * 10)
    #
    #     table = script.table()
    #     for i in range(10):
    #         row = table.row()
    #         row.col(TableColStyle(gap=10)).text("ABC " * 150)
    #         row.col(TableColStyle(gap=10)).text("ABC " * 150)
    #         row.col(TableColStyle(gap=10)).text("ABC " * 150)
    #
    #     script.paragraph("abcd" * 10)
    #
    #     script.render_as_file("table.pdf", interceptor)
    #     interceptor.verify(f"{get_local_dir(__file__)}/test_table_overflow.txt")