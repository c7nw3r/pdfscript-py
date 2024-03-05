from pdfscript.__spi__.protocols import PDFListener
from pdfscript.__spi__.types import BoundingBox, Space


class NoOpListener(PDFListener):

    def on_space(self, space: Space):
        pass

    def on_instr(self, bbox: BoundingBox):
        pass
