from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import SpaceSupplier
from pdfscript.__spi__.pdf_opset import PDFOpset
from pdfscript.__spi__.pdf_writable import Writable, PDFEvaluation
from pdfscript.__spi__.styles import TextStyle
from pdfscript.__spi__.types import Space, PDFPosition


class Text(Writable):
    def __init__(self, text: str, style: TextStyle):
        self.text = text
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        y_offset = self.style.margin.top
        x_offset = self.style.margin.left

        def space(ops: PDFOpset, pos: PDFPosition):
            w = ops.get_width_of_text(self.text, self.style.font_name, self.style.font_size) + x_offset
            h = ops.get_height_of_text(self.text, self.style, pos.max_x) + y_offset

            # FIXME
            return Space(w, h + self.style.space_after)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            width, height = get_space(ops, pos)
            one_line = height <= ops.get_height_of_text(".", self.style)

            pos.move_y_offset(y_offset)

            if not one_line:
                if (pos.y - height) < pos.min_y:  # page overflow
                    ops.add_page()
                    pos.y = pos.min_y
                    pos.x = context.page_margin.left
                    ops.add_text(self.text, pos.with_x_offset(x_offset), self.style)
                else:
                    ops.add_text(self.text, pos.with_x_offset(x_offset), self.style)
                    pos.y += height
                    pos.x = pos.min_x
            else:
                ops.add_text(self.text, pos.with_x_offset(x_offset), self.style)
                pos.x += width

            # print("text", pos.x, pos.y, width, height)

        return PDFEvaluation(space, instr)
