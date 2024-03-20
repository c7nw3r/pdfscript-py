from unittest import TestCase

from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from pdfscript.stream.listener.bbox_listener import BBoxListener
from test import get_local_dir
from test.consts import WIKIPEDIA_TEXT


class BoldTest(TestCase):

    def test_bold(self):
        interceptor = AuditInterceptor()

        script = PDFScript.a4()
        script.bold(WIKIPEDIA_TEXT, listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_bold.txt")
