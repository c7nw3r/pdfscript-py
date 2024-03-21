from typing import List

from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.types import BoundingBox, Space
from pdfscript.stream.writable.table.table_row import LastBoundingBoxOnPage


class BBoxMergerListener(PDFListener):

    def __init__(self, listener: PDFListener):
        super().__init__()
        self.listener = listener
        self.buffer: List[BoundingBox] = []

    def on_space(self, space: Space, ops: PDFOpset):
        self.listener.on_space(space, ops)

    def on_instr(self, bbox: BoundingBox, ops: PDFOpset):
        if len(self.buffer) == 0:
            self.buffer.append(bbox)
        elif self.buffer[-1].page == bbox.page:
            self.buffer.append(bbox)
        else:
            self.flush(ops)

        if isinstance(bbox, LastBoundingBoxOnPage):
            self.flush(ops)

    def flush(self, ops: PDFOpset):
        if len(self.buffer) > 0:
            page = self.buffer[0].page
            x1 = min([e.x1 for e in self.buffer])
            y1 = max([e.y1 for e in self.buffer])
            x2 = max([e.x2 for e in self.buffer])
            y2 = min([e.y2 for e in self.buffer])
            self.buffer = []

            self.listener.on_instr(BoundingBox(page, x1, y1, x2, y2), ops)
