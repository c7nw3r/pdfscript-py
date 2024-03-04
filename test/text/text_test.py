from unittest import TestCase

from pdfscript.__spi__.styles import TextStyle
from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from test import get_local_dir


class TextTest(TestCase):

    def test_paragraph(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.text("Test asdf" * 20)

        script.execute("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph.txt")

    def test_paragraph_with_custom_font(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.text("Test asdf" * 20, TextStyle(font_name="Times-Bold", font_size=20))

        script.execute("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph_with_custom_font_justified.txt")

    def test_paragraph_with_header_and_footer(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        header = script.with_header()
        header.text("Test asdf" * 10)

        footer = script.with_footer()
        footer.text("Test asdf" * 10)

        script.text("Test asdf" * 20, TextStyle(font_size=16))

        script.execute("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph_with_header_and_footer.txt")
