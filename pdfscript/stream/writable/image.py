from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_opset import PDFOpset
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.styles import ImageStyle, Align
from pdfscript.__spi__.types import Space, PDFPosition


class Image(Writable):
    def __init__(self, src: str, style: ImageStyle):
        self.src = src
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        def space(_ops: PDFOpset, _pos: PDFPosition):
            return Space(self.style.width, self.style.height)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            width, height = get_space(ops, pos)

            x = pos.x
            if self.style.align == Align.CENTER:
                x += ((pos.max_x - pos.min_x) / 2) - (width / 2)

            ops.add_image(self.src, pos, self.style)

            if self.style.display == "block":
                pos.x = pos.min_x
                pos.y += height
            else:
                pos.x = x + width

        return PDFEvaluation(space, instr)
