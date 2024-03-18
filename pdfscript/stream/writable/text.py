from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable, PDFEvaluation
from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.styles import TextStyle
from pdfscript.__spi__.types import Space, PDFPosition, BoundingBox
from pdfscript.stream.listener.noop_listener import NoOpListener


class Text(Writable):
    def __init__(self, text: str, style: TextStyle, listener: PDFListener = NoOpListener()):
        self.text = str(text)  # convert to str in case the argument is not of type str
        self.style = style
        self.listener = listener

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        # y_offset = self.style.margin.top
        x_offset = self.style.margin.left

        def space(ops: PDFOpset, pos: PDFPosition):
            w = ops.get_width_of_text(self.text, self.style, pos.max_x - pos.x) + x_offset
            h = ops.get_height_of_text(self.text, self.style, pos.max_x - pos.x) # + y_offset

            return Space(w, h).emit(self.listener, ops)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            width, height = get_space(ops, pos)
            one_line = height <= ops.get_height_of_text(".", self.style)

            pos.move_y_offset(-self.style.margin.top)

            if not one_line:
                if (pos.y - height) < pos.min_y:  # page overflow
                    _text = self.text
                    _height = height

                    while len(_text) > 0:
                        split_a, split_b = ops.split_text_by_height(_text, self.style, pos)

                        if split_a is not None:
                            ops.add_text(split_a.text, pos.with_x_offset(x_offset), self.style)
                            bbox = BoundingBox(ops.page(), pos.x, pos.y, pos.x + width, pos.y - split_a.height)
                            bbox.emit(self.listener, ops)

                        if split_b is not None:
                            ops.add_page()

                        _text = split_b.text if split_b is not None else ""
                        pos.y = pos.max_y - (0 if len(split_b or []) > 0 else split_a.height)
                        pos.x = context.margin.left

                else:
                    ops.add_text(self.text, pos.with_x_offset(x_offset), self.style)

                    bbox = BoundingBox(ops.page(), pos.x, pos.y, pos.x + (pos.max_x - pos.x), pos.y - height)
                    bbox.emit(self.listener, ops)

                    pos.y -= height
                    pos.x = pos.min_x
            else:
                if (pos.y - height) < pos.min_y:  # page overflow
                    ops.add_page()
                    pos.pos_zero()

                ops.add_text(self.text, pos.with_x_offset(x_offset), self.style)
                bbox = BoundingBox(ops.page(), pos.x, pos.y, pos.x + width, pos.y - height)
                bbox.emit(self.listener, ops)

                pos.x += width

            pos.move_y_offset(-self.style.margin.bottom)

        return PDFEvaluation(space, instr)
