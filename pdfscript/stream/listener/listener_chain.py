from typing import List

from pdfscript.__spi__.protocols import PDFListener, PDFOpset
from pdfscript.__spi__.types import BoundingBox, Space


class PDFListenerChain(PDFListener):

    def __init__(self, listeners: List[PDFListener]):
        self.listeners = listeners

    def on_space(self, space: Space, ops: PDFOpset):
        [e.on_space(space, ops) for e in self.listeners]

    def on_instr(self, bbox: BoundingBox, ops: PDFOpset):
        [e.on_instr(bbox, ops) for e in self.listeners]
