from unittest import TestCase

from pdfscript.__spi__.styles import TableColStyle, LineStyle, TableRowStyle
from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from pdfscript.stream.listener.bbox_listener import BBoxListener
from test import get_local_dir
from test.consts import WIKIPEDIA_TEXT


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

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_table.txt")

    def test_table_without_border(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        row_style = TableRowStyle(gap=5)
        col_style = TableColStyle(border=LineStyle("white"))

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

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_table_without_border.txt")

    def test_paragraph_and_table(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()
        listener = BBoxListener(draw=True, seed=1)

        script.paragraph("abcd" * 10)

        table = script.table(listener=listener)
        row1 = table.row(TableRowStyle(gap=10))
        row1.col().text(
            "The Foundation has grown rapidly throughout its existence. By 2022, it employed around 700 staff")
        row1.col().text(
            "and contractors, with annual revenues of $155 million, annual expenses of $146 million, net assets")
        row1.col().text(
            "of $240 million and a growing endowment, which surpassed $100 million in June 2021.")

        script.paragraph("abcd" * 10)

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph_and_table.txt")

    def test_different_col_height(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        script.paragraph("abcd" * 10)

        table = script.table()
        row1 = table.row()
        row1.col(TableColStyle()).text("Column 1")
        row1.col(TableColStyle()).text("Column 2")
        row1.col(TableColStyle()).text("Column 3")
        row2 = table.row()
        row2.col(TableColStyle()).text(WIKIPEDIA_TEXT[0:500])
        row2.col(TableColStyle()).text(WIKIPEDIA_TEXT[0:550])
        row2.col(TableColStyle()).text(WIKIPEDIA_TEXT[0:400])

        script.paragraph("abcd" * 10)

        script.render_as_stream(interceptor)
        interceptor.save(f"{get_local_dir(__file__)}/test_different_col_height.txt")

    def test_too_long_col(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        table = script.table()
        row1 = table.row()
        row1.col(TableColStyle()).text(WIKIPEDIA_TEXT[0:800])
        row1.col(TableColStyle()).text(WIKIPEDIA_TEXT[0:550])
        row1.col(TableColStyle()).text(WIKIPEDIA_TEXT[0:400])

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_too_long_col.txt")

    def test_col4(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        table = script.table()
        row1 = table.row()
        row1.col(TableColStyle()).text(WIKIPEDIA_TEXT[0:463])
        row1.col(TableColStyle()).text(WIKIPEDIA_TEXT[0:250])
        row1.col(TableColStyle()).text(WIKIPEDIA_TEXT[0:200])
        row1.col(TableColStyle()).text(WIKIPEDIA_TEXT[0:200])
        script.text(WIKIPEDIA_TEXT)

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_col4.txt")
