from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.protocols import PDFOpset
from pdfscript.__spi__.styles import ImageStyle, Align
from pdfscript.__spi__.types import Number, PDFPosition, Space, PDFCoords


class CanvasImage(Writable):

    def __init__(self, src: str, x: Number, y: Number, style: ImageStyle):
        self.src = src
        self.x = x
        self.y = y
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        def space(_ops: PDFOpset, _pos: PDFPosition):
            return Space(self.style.width, self.style.height)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            width, height = get_space(ops, pos)

            x = pos.x

            if self.style.align == Align.CENTER:
                x += ((pos.max_x - pos.min_x) / 2) - (width / 2)

            pos.move_y_offset(self.style.margin.top)

            ops.add_image(self.src, PDFCoords(x, pos.y), self.style)

            if self.style.display == "block":
                pos.x = pos.min_x
                pos.y += height
            else:
                pos.x += width

        return PDFEvaluation(space, instr)