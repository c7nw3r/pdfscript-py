from pathlib import Path
from unittest import TestCase

from pdfscript.__spi__.styles import ImageStyle
from pdfscript.pdf_script import PDFScript
from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor
from test import get_local_dir


class ImageTest(TestCase):

    def test_image(self):
        interceptor = AuditInterceptor()
        path = Path(__file__).parent.as_posix() + "/email.png"

        script = PDFScript.a4()
        script.text("abcd")
        script.image(path, ImageStyle(width=50, height=30))

        script.execute("image.pdf", interceptor)
        interceptor.verify(f"{get_local_dir(__file__)}/test_image.txt")
