from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Literal

from pdfscript.__spi__.types import Margin, Number


class Align(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    JUSTIFY = 4


@dataclass
class TextStyle:
    font_name: str = "Courier"
    font_size: int = 14
    align: Align = Align.LEFT
    color: Optional[str] = None
    margin: Margin = field(default_factory=lambda: Margin(0, 0, 0, 0))
    line_clamp: Optional[float] = None
    left_indent: Number = 0

    @property
    def space_after(self):
        return self.font_size * 1.25

    def to_paragraph_style(self):
        from reportlab.lib.styles import ParagraphStyle
        return ParagraphStyle("Normal",
                              fontName=self.font_name,
                              fontSize=self.font_size,
                              leading=self.space_after,
                              leftIndent=self.left_indent,
                              # bulletIndent=50,
                              alignment=self.align.value)


@dataclass
class ParagraphStyle(TextStyle):
    layout: Literal["block", "col2", "col3"] = "block"
    gap: Number = 0
    margin: Margin = field(default_factory=lambda: Margin(0, 0, 10, 0))


@dataclass
class TitleStyle(TextStyle):
    margin: Margin = field(default_factory=lambda: Margin(10, 0, 10, 0))


@dataclass
class ImageStyle:
    width: int = 100
    height: int = 100
    align: Align = Align.CENTER
    display: Optional[Literal["block"]] = None
    margin: Margin = field(default_factory=lambda: Margin(0, 0, 0, 0))


@dataclass
class HStackStyle:
    align: Optional[Literal['center', 'justify', 'left', 'right']] = None
    margin: Margin = field(default_factory=lambda: Margin(0, 0, 0, 0))
    gap: Number = 10


@dataclass
class VStackStyle:
    gap: Number = 10
    margin: Margin = field(default_factory=lambda: Margin(0, 0, 0, 0))
    align: Align = Align.LEFT


@dataclass
class TableRowStyle:
    gap: Number = 0
    margin: Margin = field(default_factory=lambda: Margin(0, 0, 0, 0))


@dataclass
class LineStyle:
    stroke_color: Optional[str] = None
    stroke_opacity: float = 1


@dataclass
class TableColStyle:
    margin: Margin = field(default_factory=lambda: Margin(5, 5, 5, 5))
    border: LineStyle = field(default_factory=lambda: LineStyle())
    # TODO: remove
    gap: Number = 0


@dataclass
class RectStyle:
    stroke_color: Optional[str] = None
    stroke_opacity: float = 1
    fill_color: Optional[str] = None
    fill_opacity: float = 1
