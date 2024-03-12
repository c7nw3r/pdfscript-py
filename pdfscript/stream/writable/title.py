from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import SpaceSupplier
from pdfscript.__spi__.pdf_writable import PDFEvaluation
from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.styles import TextStyle
from pdfscript.__spi__.types import PDFPosition
from pdfscript.stream.listener.noop_listener import NoOpListener
from pdfscript.stream.writable.text import Text


class Title(Text):
    def __init__(self, text: str, style: TextStyle, order: int = 1, listener: PDFListener = NoOpListener()):
        super().__init__(text, style, listener)
        self.order = order

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        self.style.font_name = context.fonts.get_bold(self.style.font_name)
        self.style.font_size = context.sizes[f"title{self.order}"]
        super_space, super_instr = super().evaluate(context)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            _, height = get_space(ops, pos)
            super_instr(ops, pos, get_space)
            pos.x = pos.min_x
            pos.y -= height

        return PDFEvaluation(super_space, instr)
