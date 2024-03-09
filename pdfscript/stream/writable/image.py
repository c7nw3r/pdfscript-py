from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.styles import ImageStyle, Align, RectStyle
from pdfscript.__spi__.types import Space, PDFPosition, BoundingBox
from pdfscript.stream.listener.noop_listener import NoOpListener


class Image(Writable):
    def __init__(self, src: str, style: ImageStyle, listener: PDFListener = NoOpListener()):
        self.src = src
        self.style = style
        self.listener = listener

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        def space(ops: PDFOpset, _pos: PDFPosition):
            return Space(self.style.width, self.style.height).emit(self.listener, ops)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            width, height = get_space(ops, pos)
            bbox = BoundingBox(pos.x, pos.y, pos.x + width, pos.y - height)

            x = pos.x
            if self.style.align == Align.CENTER:
                x += ((pos.max_x - pos.min_x) / 2) - (width / 2)

            ops.add_image(self.src, pos, self.style)

            if self.style.display == "block":
                pos.x = pos.min_x
                pos.y += height
            else:
                pos.x = x + width

            if context.draw_bbox:
                ops.draw_rect(bbox.x1, bbox.y1, bbox.x2, bbox.y2, RectStyle(stroke_color="red"))

        return PDFEvaluation(space, instr)
