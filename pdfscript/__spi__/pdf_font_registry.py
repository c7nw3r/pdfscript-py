from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class PDFFontRegistry:
    def __init__(self):
        self.fonts = [
            "Courier", "Courier-Oblique", "Courier-Bold", "Courier-BoldOblique",
            "Helvetica", "Helveticy-Oblique", "Helvetica-Bold", "Helveticy-BoldOblique",
            "Times-Roman", "Times-Italic", "Times-Bold", "TimesBoldItalic"
        ]

    def register_font(self, name: str, path: str):
        if name in self.fonts:
            raise ValueError(f"font with name {name} is already registered")

        pdfmetrics.registerFont(TTFont(name, path))
        self.fonts.append(name)

    def get_available_fonts(self):
        return self.fonts
