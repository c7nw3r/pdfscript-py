from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable, PDFEvaluation
from pdfscript.__spi__.styles import TextStyle
from pdfscript.__spi__.types import Space, BoundingBox


class Text(Writable):
    def __init__(self, text: str, style: TextStyle):
        self.text = text
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        y_offset = self.style.margin.top
        x_offset = self.style.margin.left

        def space(stream: PDFApi, box: BoundingBox):
            w = stream.get_width_of_text(self.text, self.style.font_name, self.style.font_size) + x_offset
            h = stream.get_height_of_text(self.text, self.style, box.max_x) + y_offset

            return Space(w, h + self.style.space_after)

        def instr(stream: PDFApi, box: BoundingBox, get_space: SpaceSupplier):
            width, height = get_space(stream, box)
            one_line = height <= stream.get_height_of_text(".", self.style)

            box.move_y_offset(y_offset)

            if not one_line:
                if (box.y - height) < box.min_y:  # page overflow
                    stream.add_page()
                    box.y = box.min_y
                    box.x = context.page_margin.left
                    stream.add_text(self.text, box.with_x_offset(x_offset), self.style)
                else:
                    stream.add_text(self.text, box.with_x_offset(x_offset), self.style)
                    box.y += height
                    box.x = box.min_x
            else:
                stream.add_text(self.text, box.with_x_offset(x_offset), self.style)
                box.x += width

            print("text", box.x, box.y, width, height)

        return PDFEvaluation(space, instr)
