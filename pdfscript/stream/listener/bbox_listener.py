from typing import Optional

from pdfscript.__spi__.protocols import PDFListener, PDFOpset
from pdfscript.__spi__.styles import RectStyle
from pdfscript.__spi__.types import BoundingBox, Space


class BBoxListener(PDFListener):
    def __init__(self, bbox_type: Optional[str] = None, draw: bool = False, seed=None):
        self.type = bbox_type
        self.draw = draw
        self.list = []
        self.seed = seed

    def on_space(self, space: Space, ops: PDFOpset):
        pass

    def on_instr(self, bbox: BoundingBox, ops: PDFOpset):
        if self.draw:
            import random
            random.seed(self.seed)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = f"rgb({r},{g},{b})"
            ops.draw_rect(bbox.x1, bbox.y1, bbox.x2, bbox.y2, RectStyle(fill_color=color, fill_opacity=0.1))

        self.list.append((self.type, bbox))
