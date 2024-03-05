from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.protocols import PDFOpset
from pdfscript.__spi__.styles import RectStyle
from pdfscript.__spi__.types import Number, PDFPosition, Space


class CanvasRect(Writable):
    def __init__(self, x: Number, y: Number, w: Number, h: Number, style: RectStyle = RectStyle()):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        def space(_ops: PDFOpset, _pos: PDFPosition):
            return Space(0, 0)

        def instr(ops: PDFOpset, _pos: PDFPosition, _get_space: SpaceSupplier):
            ops.draw_rect(self.x, self.y, self.w, self.y, self.style)

        return PDFEvaluation(space, instr)
