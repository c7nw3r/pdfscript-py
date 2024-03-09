from unittest import TestCase

from pdfscript.__spi__.styles import TextStyle
from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from pdfscript.stream.listener.bbox_listener import BBoxListener
from test import get_local_dir
from test.consts import WIKIPEDIA_TEXT


class TextTest(TestCase):

    def test_paragraph(self):
        bbox_listener = BBoxListener("text")
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.text("Test asdf" * 30, listener=bbox_listener)

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph.txt")

    def test_paragraph_with_custom_font(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.text("Test asdf" * 20, TextStyle(font_name="Times-Bold", font_size=20))

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph_with_custom_font_justified.txt")

    def test_paragraph_with_header_and_footer(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        header = script.with_header()
        header.text("Test asdf" * 10)

        footer = script.with_footer()
        footer.text("Test asdf" * 10)

        script.text("Test asdf" * 20, TextStyle(font_size=16))

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph_with_header_and_footer.txt")

    def test_long_text(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph(WIKIPEDIA_TEXT)
        script.paragraph(WIKIPEDIA_TEXT)
        script.paragraph(WIKIPEDIA_TEXT)
        script.paragraph(WIKIPEDIA_TEXT)

        script.render_as_file("simple.pdf", interceptor)
        interceptor.save(f"{get_local_dir(__file__)}/test_long_text2.txt")

    def test_long_paragraphs(self):
        bbox_listener = BBoxListener("text")
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph("Wikimedia Commons – repository of images, sounds, videos, and general media")
        script.paragraph("Wikispecies – taxonomic catalog of species")

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_long_paragraphs.txt")

    def test_text_overflow(self):
        bbox_listener = BBoxListener("text")
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph("This is an example text. " * 200)

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_text_overflow.txt")

    def test_bold(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.bold(WIKIPEDIA_TEXT, listener=BBoxListener("text", draw=True))

        script.render_as_file("simple.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_bold.txt")
