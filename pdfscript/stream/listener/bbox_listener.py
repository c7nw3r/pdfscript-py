from pdfscript.__spi__.protocols import PDFListener
from pdfscript.__spi__.types import BoundingBox, Space


class BBoxListener(PDFListener):
    def __init__(self, bbox_type: str):
        self.type = bbox_type
        self.bboxes = []

    def on_space(self, space: Space):
        pass

    def on_instr(self, bbox: BoundingBox):
        self.bboxes.append(bbox)
