from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.styles import TextStyle
from pdfscript.__spi__.types import PDFPosition
from pdfscript.stream.listener.noop_listener import NoOpListener
from pdfscript.stream.writable.text import Text


# TODO: nested list item support
class ListItem(Text):

    def __init__(self, text: str, style: TextStyle, listener: PDFListener = NoOpListener()):
        bullet = "<bullet>&bull;</bullet>"
        super().__init__(bullet + text, style, listener)

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        self.style.left_indent = 10
        super_space, super_instr = super().evaluate(context)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            _, height = get_space(ops, pos)
            super_instr(ops, pos, get_space)
            pos.x = pos.min_x

        return PDFEvaluation(super_space, instr)
