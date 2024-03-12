from pdfscript.__spi__.protocols import PDFListener, PDFOpset
from pdfscript.__spi__.types import BoundingBox, Space


class NoOpListener(PDFListener):

    def on_space(self, space: Space, ops: PDFOpset):
        pass

    def on_instr(self, bbox: BoundingBox, ops: PDFOpset):
        pass


DEV_NULL = NoOpListener()
