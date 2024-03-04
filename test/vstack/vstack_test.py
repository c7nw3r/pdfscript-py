from unittest import TestCase

from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor


class VStackTest(TestCase):

    def test_vstack(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        def vstack_configurer(writer: PDFWriter):
            writer.text("Line 1")
            writer.text("Line 2")

        script.vstack(vstack_configurer)

        script.execute("vstack.pdf", interceptor)
        interceptor.verify("./test_vstack.txt")
