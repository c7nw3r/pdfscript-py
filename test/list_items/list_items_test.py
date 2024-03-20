from unittest import TestCase

from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from pdfscript.stream.listener.bbox_listener import BBoxListener
from test import get_local_dir
from test.consts import WIKIPEDIA_TEXT


class ListItemsTest(TestCase):

    def test_unordered_list(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        ul = script.list_items()
        ul.list_item(WIKIPEDIA_TEXT, listener=BBoxListener(draw=True, seed=1))
        ul.list_item(WIKIPEDIA_TEXT[0:200], listener=BBoxListener(draw=True, seed=1))
        ul.list_item(WIKIPEDIA_TEXT, listener=BBoxListener(draw=True, seed=1))
        ul.list_item(WIKIPEDIA_TEXT[0:200], listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_unordered_list_v2.txt")

    def test_one_line_items(self):
        interceptor = AuditInterceptor()
        script = PDFScript.a4()

        ul = script.list_items()
        ul.list_item(WIKIPEDIA_TEXT[0:24], listener=BBoxListener(draw=True, seed=1))
        ul.list_item(WIKIPEDIA_TEXT[0:24], listener=BBoxListener(draw=True, seed=1))

        script.render_as_stream(interceptor)
        interceptor.save(f"{get_local_dir(__file__)}/test_one_line_items.txt")