from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_opset import PDFOpset
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.styles import LineStyle
from pdfscript.__spi__.types import Number, PDFPosition, Space


class CanvasLine(Writable):
    def __init__(self, x1: Number, y1: Number, x2: Number, y2: Number, style: LineStyle = LineStyle()):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        def space(_ops: PDFOpset, _pos: PDFPosition):
            return Space(0, 0)

        def instr(ops: PDFOpset, _pos: PDFPosition, _get_space: SpaceSupplier):
            ops.draw_line(self.x1, self.y1, self.x2, self.y2, self.style)

        return PDFEvaluation(space, instr)
