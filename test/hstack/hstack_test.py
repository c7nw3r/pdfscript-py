from unittest import TestCase

from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from test import get_local_dir


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
        interceptor.verify(f"{get_local_dir(__file__)}/test_hstack.txt")
