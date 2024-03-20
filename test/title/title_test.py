from unittest import TestCase

from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from pdfscript.stream.listener.bbox_listener import BBoxListener
from test import get_local_dir
from test.consts import WIKIPEDIA_TEXT


class TitleTest(TestCase):

    def test_title1(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph(WIKIPEDIA_TEXT[0:24])
        script.title1(WIKIPEDIA_TEXT[0:24], listener=BBoxListener(draw=True, seed=1))
        script.paragraph(WIKIPEDIA_TEXT)

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_title1.txt")

    def test_title2(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph(WIKIPEDIA_TEXT[0:24])
        script.title2(WIKIPEDIA_TEXT[0:24], listener=BBoxListener(draw=True, seed=1))
        script.paragraph(WIKIPEDIA_TEXT)

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_title2.txt")

    def test_title3(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.paragraph(WIKIPEDIA_TEXT[0:24])
        script.title3(WIKIPEDIA_TEXT[0:24], listener=BBoxListener(draw=True, seed=1))
        script.paragraph(WIKIPEDIA_TEXT)

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_title3.txt")
