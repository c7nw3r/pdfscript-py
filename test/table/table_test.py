from unittest import TestCase

from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor


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
        interceptor.verify("./test_table.txt")
