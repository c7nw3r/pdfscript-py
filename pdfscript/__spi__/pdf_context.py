from dataclasses import dataclass
from enum import Enum

from reportlab.lib import pagesizes
from reportlab.lib.units import inch

from pdfscript.__spi__.pdf_font_registry import PDFFontRegistry


class PageFormat(Enum):
    # ISO 216 standard page formats; see eg https://en.wikipedia.org/wiki/ISO_216
    A0 = pagesizes.A0
    A1 = pagesizes.A1
    A2 = pagesizes.A2
    A3 = pagesizes.A3
    A4 = pagesizes.A4
    A5 = pagesizes.A5
    A6 = pagesizes.A6
    A7 = pagesizes.A7
    A8 = pagesizes.A8
    A9 = pagesizes.A9
    A10 = pagesizes.A10
    B0 = pagesizes.B0
    B1 = pagesizes.B1
    B2 = pagesizes.B2
    B3 = pagesizes.B3
    B4 = pagesizes.B4
    B5 = pagesizes.B5
    B6 = pagesizes.B6
    B7 = pagesizes.B7
    B8 = pagesizes.B8
    B9 = pagesizes.B9
    B10 = pagesizes.B10
    C0 = pagesizes.C0
    C1 = pagesizes.C1
    C2 = pagesizes.C2
    C3 = pagesizes.C3
    C4 = pagesizes.C4
    C5 = pagesizes.C5
    C6 = pagesizes.C6
    C7 = pagesizes.C7
    C8 = pagesizes.C8
    C9 = pagesizes.C9
    C10 = pagesizes.C10
    # American page formats
    LETTER = pagesizes.LETTER
    LEGAL = pagesizes.LEGAL
    ELEVEN_SEVENTEEN = pagesizes.elevenSeventeen
    # Further page formats; see  https://en.wikipedia.org/wiki/Paper_size
    JUNIOR_LEGAL = pagesizes.JUNIOR_LEGAL
    HALF_LETTER = pagesizes.HALF_LETTER
    GOV_LETTER = pagesizes.GOV_LETTER
    GOV_LEGAL = pagesizes.GOV_LEGAL
    TABLOID = pagesizes.elevenSeventeen
    LEDGER = pagesizes.LEDGER


class PageMargin:
    def __init__(self,
                 top: float,
                 bottom: float,
                 left: float,
                 right: float,
                 header: float,
                 footer: float):
        self.top = top * inch
        self.bottom = bottom * inch
        self.left = left * inch
        self.right = right * inch
        self.header = header * inch
        self.footer = footer * inch

    def __iter__(self):
        yield self.top
        yield self.bottom
        yield self.left
        yield self.right
        yield self.header
        yield self.footer

    @staticmethod
    def default():
        return PageMargin(1, 1, 1, 1, 0.3, 0.3)


@dataclass
class PDFContext:
    format: PageFormat
    margin: PageMargin
    draw_bbox: bool = False
    tile1_size: int = 20
    tile2_size: int = 18
    tile3_size: int = 16

    def __post_init__(self):
        self.fonts = PDFFontRegistry()
        self.sizes = {
            "title1": self.tile1_size,
            "title2": self.tile2_size,
            "title3": self.tile3_size,
        }
