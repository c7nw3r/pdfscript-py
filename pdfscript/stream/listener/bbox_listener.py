from pdfscript.__spi__.protocols import PDFListener, PDFOpset
from pdfscript.__spi__.styles import RectStyle
from pdfscript.__spi__.types import BoundingBox, Space


class BBoxListener(PDFListener):
    def __init__(self, bbox_type: str, draw: bool = False):
        self.type = bbox_type
        self.bboxes = []
        self.draw = draw

    def on_space(self, space: Space, ops: PDFOpset):
        pass

    def on_instr(self, bbox: BoundingBox, ops: PDFOpset):
        if self.draw:
            ops.draw_rect(bbox.x1, bbox.y1, bbox.x2, bbox.y2, RectStyle(fill_color="red", fill_opacity=0.1))

        self.bboxes.append(bbox)
