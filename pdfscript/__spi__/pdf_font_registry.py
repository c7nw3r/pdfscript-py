from typing import Optional

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from pdfscript.__spi__.types import FontFamily
from pdfscript.__util__.string_util import get_filename


class PDFFontRegistry:
    def __init__(self):
        self.fonts = {
            "courier": FontFamily("Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique"),
            "helvetica": FontFamily("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique"),
            "times-roman": FontFamily("Times-Roman", "Times-Bold", "Times-Italic", "TimesBoldItalic")
        }

    def register_font(self, font: FontFamily):
        pdfmetrics.registerFont(TTFont(get_filename(font.regular), font.regular))
        pdfmetrics.registerFont(TTFont(get_filename(font.bold), font.bold))
        pdfmetrics.registerFont(TTFont(get_filename(font.italic), font.italic))
        pdfmetrics.registerFont(TTFont(get_filename(font.bold_italic), font.bold_italic))
        self.fonts[get_filename(font.regular)] = font

    def get_available_fonts(self):
        return self.fonts

    def get_font_family(self, font_name: str) -> Optional[FontFamily]:
        for font in self.fonts.values():
            if font_name in font.regular:
                return font
            if font_name in font.bold:
                return font
            if font_name in font.italic:
                return font
            if font_name in font.bold_italic:
                return font

        raise ValueError(f"unknown font {font_name}")

    def get_bold(self, font_name: str) -> str:
        return get_filename(self.get_font_family(font_name).bold)
