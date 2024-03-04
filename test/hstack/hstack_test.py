from unittest import TestCase

from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor


class HStackTest(TestCase):

    def test_hstack(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        def hstack_configurer(writer: PDFWriter):
            writer.text("Line 1")
            writer.text("Line 2")

        script.vstack(hstack_configurer)
        script.vstack(hstack_configurer)

        script.execute("hstack.pdf", interceptor)
        interceptor.verify("./test_hstack.txt")
