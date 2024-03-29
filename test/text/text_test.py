from unittest import TestCase

from pdfscript.__spi__.styles import TextStyle, ParagraphStyle
from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from pdfscript.stream.listener.bbox_listener import BBoxListener
from test import get_local_dir
from test.consts import WIKIPEDIA_TEXT


class TextTest(TestCase):

    def test_paragraph(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.text(WIKIPEDIA_TEXT, listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph.txt")

    def test_paragraph_with_custom_font(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.text(WIKIPEDIA_TEXT, TextStyle(font_name="Times-Bold", font_size=20), listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph_with_custom_font_justified.txt")

    def test_paragraph_with_header_and_footer(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        header = script.with_header()
        header.text("Test asdf" * 10, listener=BBoxListener(draw=True, seed=1))

        footer = script.with_footer()
        footer.text("Test asdf" * 10, listener=BBoxListener(draw=True, seed=1))

        script.text("Test asdf" * 20, TextStyle(font_size=16), listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph_with_header_and_footer.txt")

    def test_long_text(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph(WIKIPEDIA_TEXT, listener=BBoxListener(draw=True, seed=1))
        script.paragraph(WIKIPEDIA_TEXT, listener=BBoxListener(draw=True, seed=1))
        script.paragraph(WIKIPEDIA_TEXT, listener=BBoxListener(draw=True, seed=1))
        script.paragraph(WIKIPEDIA_TEXT, listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_long_text.txt")

    def test_long_paragraphs(self):
        listener = BBoxListener(draw=True, seed=1)
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph("Wikimedia Commons – repository of images, sounds, videos, and general media", listener=listener)
        script.paragraph("Wikispecies – taxonomic catalog of species", listener=listener)

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_long_paragraphs.txt")

    def test_text_overflow(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph("This is an example text. " * 200, listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_text_overflow.txt")

    def test_bold(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.bold(WIKIPEDIA_TEXT, listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_bold.txt")

    def test_paragraph_col2_layout(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph(WIKIPEDIA_TEXT, style=ParagraphStyle(layout="col2", gap=5), listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_paragraph_col2_layout.txt")

    def test_paragraph_col3_layout(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph(WIKIPEDIA_TEXT, style=ParagraphStyle(layout="col3", gap=5), listener=BBoxListener(draw=True, seed=1))
        script.paragraph(WIKIPEDIA_TEXT, style=ParagraphStyle(layout="col3", gap=5), listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.save(f"{get_local_dir(__file__)}/test_paragraph_col3_layout.txt")

    def test_short_paragraph_col2_layout(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph("Wiktionary – online dictionary and thesaurus", style=ParagraphStyle(layout="block"))
        script.paragraph("Wikibooks – a collection of books, mostly textbooks", style=ParagraphStyle(layout="col3"))
        script.paragraph("Wikiquote – a collection of quotations", style=ParagraphStyle(layout="block"))
        script.paragraph("Wikivoyage – travel guide", style=ParagraphStyle(layout="col3"))
        script.paragraph("Wikisource – digital library", style=ParagraphStyle(layout="block"))

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_short_paragraph_col2_layout.txt")

    def test_long_paragraph_col3_layout(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph(WIKIPEDIA_TEXT * 5, style=ParagraphStyle(layout="col3"), listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.save(f"{get_local_dir(__file__)}/test_long_paragraph_col3_layout.txt")

    def test_newline_separator(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph("text\ntext\n" * 100, style=ParagraphStyle(layout="col3"), listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.save(f"{get_local_dir(__file__)}/test_newline_separator.txt")
