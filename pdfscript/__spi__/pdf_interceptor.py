from typing import Optional

from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.styles import TextStyle, ImageStyle
from pdfscript.__spi__.types import Number, BoundingBox


class DevNullInterceptor(PDFApi):

    def add_text(self, text: str, box: BoundingBox, styling: TextStyle):
        pass

    def add_image(self, src: str, box: BoundingBox, styling: ImageStyle):
        pass

    def get_width_of_text(self, text: str, font_name: str, font_size: int, consider_overflow: bool = True):
        pass

    def get_height_of_text(self, text: str, style: TextStyle, max_x: Optional[Number] = None):
        pass

    def add_page(self):
        pass
