from unittest import TestCase

from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from test import get_local_dir


class CanvasTest(TestCase):

    def test_canvas(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        canvas = script.with_canvas()
        canvas.draw_line(10, 10, 100, 100)
        canvas.draw_rect(10, 10, 100, 100)

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_canvas.txt")
