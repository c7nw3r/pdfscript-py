from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.protocols import PDFOpset
from pdfscript.__spi__.styles import TextStyle
from pdfscript.__spi__.types import Number, PDFPosition, Space


class CanvasText(Writable):

    def __init__(self, text: str, x: Number, y: Number, style: TextStyle):
        self.text = text
        self.x = x
        self.y = y
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        def space(_ops: PDFOpset, _pos: PDFPosition):
            return Space(0, 0)

        def instr(ops: PDFOpset, pos: PDFPosition, _get_space: SpaceSupplier):
            ops.add_text(self.text, pos, TextStyle())

        return PDFEvaluation(space, instr)
