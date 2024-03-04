from unittest import TestCase

from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor


class HStackTest(TestCase):

    def test_hstack(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        h_stack1 = script.h_stack()
        h_stack1.text("Line 1")
        h_stack1.text("Line 2")

        h_stack2 = script.h_stack()
        h_stack2.text("Line 1")
        h_stack2.text("Line 2")

        script.execute("hstack.pdf", interceptor)
        interceptor.verify("./test_hstack.txt")
