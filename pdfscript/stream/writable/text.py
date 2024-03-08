from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable, PDFEvaluation
from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.styles import TextStyle, RectStyle
from pdfscript.__spi__.types import Space, PDFPosition, BoundingBox
from pdfscript.stream.listener.noop_listener import NoOpListener


class Text(Writable):
    def __init__(self, text: str, style: TextStyle, listener: PDFListener = NoOpListener()):
        self.text = str(text)  # convert to str in case the argument is not of type str
        self.style = style
        self.listener = listener

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        y_offset = self.style.margin.top
        x_offset = self.style.margin.left

        def space(ops: PDFOpset, pos: PDFPosition):
            w = ops.get_width_of_text(self.text, self.style, pos.max_x - pos.x) + x_offset
            h = ops.get_height_of_text(self.text, self.style, pos.max_x - pos.x) + y_offset

            return Space(w, h).emit(self.listener)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            width, height = get_space(ops, pos)
            one_line = height <= ops.get_height_of_text(".", self.style) + self.style.space_after

            pos.move_y_offset(y_offset)

            bbox = BoundingBox(pos.x, pos.y, pos.x + width, pos.y - height)
            bbox.emit(self.listener)

            if not one_line:
                if (pos.y - height) < pos.min_y:  # page overflow
                    ops.add_page()
                    pos.y = pos.min_y
                    pos.x = context.margin.left
                    ops.add_text(self.text, pos.with_x_offset(x_offset), self.style)
                else:
                    ops.add_text(self.text, pos.with_x_offset(x_offset), self.style)
                    pos.y -= height
                    pos.x = pos.min_x

                    # ops.draw_line(0, pos.y, 1000, pos.y)
            else:
                ops.add_text(self.text, pos.with_x_offset(x_offset), self.style)
                pos.x += width

            if context.draw_bbox:
                ops.draw_rect(bbox.x1, bbox.y1, bbox.x2, bbox.y2, RectStyle(stroke_color="red"))

        return PDFEvaluation(space, instr)
