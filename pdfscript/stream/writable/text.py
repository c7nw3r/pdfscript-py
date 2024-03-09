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
                    _text = self.text
                    _height = height

                    while len(_text) > 0:
                        split_a, split_b = ops.split_text_by_height(_text, self.style, pos)

                        if len(split_a) > 0:
                            ops.add_text(split_a, pos.with_x_offset(x_offset), self.style)
                        if len(split_b) > 0:
                            ops.add_page()

                        _text = split_b
                        pos.y = pos.max_y - (0 if len(split_b) > 0 else height)
                        pos.x = context.margin.left

                else:
                    ops.add_text(self.text, pos.with_x_offset(x_offset), self.style)
                    pos.y -= height
                    pos.x = pos.min_x

                    # ops.draw_line(0, pos.y, 1000, pos.y, LineStyle(stroke_color="red"))
            else:
                ops.add_text(self.text, pos.with_x_offset(x_offset), self.style)
                pos.x += width

            if context.draw_bbox:
                ops.draw_rect(bbox.x1, bbox.y1, bbox.x2, bbox.y2, RectStyle(stroke_color="red"))

        return PDFEvaluation(space, instr)
