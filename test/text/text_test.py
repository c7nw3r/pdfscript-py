from unittest import TestCase

from pdfscript.__spi__.styles import TextStyle, Align
from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor


class SimpleTest(TestCase):

    def test_paragraph(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.text("Test asdf" * 20)

        script.execute("simple.pdf", interceptor)
        interceptor.verify("./test_paragraph.txt")

    def test_paragraph_with_custom_font(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.text("Test asdf" * 20, TextStyle(font_name="Times-Bold", font_size=20))

        script.execute("simple.pdf", interceptor)
        interceptor.verify("./test_paragraph_with_custom_font_justified.txt")
