from unittest import TestCase

from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor


class VStackTest(TestCase):

    def test_vstack(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        v_stack = script.v_stack()
        v_stack.text("Line 1")
        v_stack.text("Line 2")

        script.execute("vstack.pdf", interceptor)
        interceptor.verify("./test_vstack.txt")
