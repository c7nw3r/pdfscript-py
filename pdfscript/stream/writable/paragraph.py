from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import SpaceSupplier
from pdfscript.__spi__.pdf_writable import PDFEvaluation
from pdfscript.__spi__.protocols import PDFListener, PDFOpset
from pdfscript.__spi__.styles import TextStyle
from pdfscript.__spi__.types import PDFPosition
from pdfscript.stream.listener.noop_listener import NoOpListener
from pdfscript.stream.writable.text import Text


class Paragraph(Text):
    def __init__(self, text: str, style: TextStyle, listener: PDFListener = NoOpListener()):
        super().__init__(text, style, listener)

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        super_space, super_instr = super().evaluate(context)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            super_instr(ops, pos, get_space)
            pos.x = pos.min_x
            pos.y -= self.style.space_after

        return PDFEvaluation(super_space, instr)
