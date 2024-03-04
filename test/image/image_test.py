from unittest import TestCase

from pdfscript.__spi__.styles import ImageStyle
from pdfscript.pdf_script import PDFScript
from pathlib import Path

from pdfscript.stream.interceptor.audit_interceptor import AuditInterceptor


class ImageTest(TestCase):

    def test_image(self):
        interceptor = AuditInterceptor()
        path = Path(__file__).parent.as_posix() + "/email.png"

        script = PDFScript.a4()
        script.text("abcd")
        script.image(path, ImageStyle(width=50, height=30))

        script.execute("image.pdf", interceptor)
        interceptor.verify("./test_image.txt")
