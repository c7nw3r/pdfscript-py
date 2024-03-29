from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import SpaceSupplier
from pdfscript.__spi__.pdf_writable import PDFEvaluation
from pdfscript.__spi__.protocols import PDFListener, PDFOpset
from pdfscript.__spi__.styles import ParagraphStyle
from pdfscript.__spi__.types import PDFPosition, Space
from pdfscript.__util__.array_util import iterate
from pdfscript.__util__.string_util import chunk_text, split_text_by_height
from pdfscript.stream.listener.noop_listener import NoOpListener
from pdfscript.stream.writable.text import Text


class Paragraph(Text):
    def __init__(self, text: str, style: ParagraphStyle, listener: PDFListener = NoOpListener()):
        super().__init__(text, style, listener)
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        super_space, super_instr = super().evaluate(context)

        def get_gap(pos: PDFPosition):
            is_first = pos.x == context.margin.left
            is_last = pos.max_x == context.format.value[0] - context.margin.right
            if not is_first and not is_last:
                return [self.style.gap / 2, self.style.gap / 2]
            return [0 if is_first else self.style.gap, 0 if is_last else self.style.gap]

        def space(ops: PDFOpset, pos: PDFPosition):
            if self.style.layout in ["col2", "col3"]:
                w = pos.max_x - pos.x
                h = ops.get_height_of_text(self.text or ".", self.style, w)
                return Space(w, h)

            return super_space(ops, pos)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            if self.style.layout in ["col2", "col3"]:
                _, height = get_space(ops, pos)

                if (pos.y - height) < pos.min_y:  # page overflow
                    ops.add_page()
                    pos.pos_zero()

                splits = split_text_by_height(ops, self.style, pos, self.text, int(self.style.layout[-1]))

                for is_first, is_last, split in iterate(splits):
                    chunks = chunk_text(split.text, int(self.style.layout[-1]))

                    y_offsets = []
                    new_pos = pos.copy()
                    width = pos.max_x - pos.min_x
                    col_width = width / len(chunks)

                    for i in range(len(chunks)):
                        self.text = chunks[i]
                        new_pos.max_x = new_pos.x + col_width

                        gap_a, gap_b = get_gap(new_pos)
                        new_pos.x += gap_a
                        new_pos.max_x -= gap_b

                        y = pos.y
                        super_instr(ops, new_pos, get_space)
                        new_pos.x = new_pos.max_x + gap_b
                        new_pos.min_x = new_pos.x - gap_a
                        y_offsets.append(pos.y - new_pos.y)
                        new_pos.y = y

                    height = get_space(ops, pos).height
                    y_offset = max(y_offsets) if max(y_offsets) > 0 else height
                    pos.y -= y_offset if y_offset >= height else height

                    if not is_last:
                        ops.add_page()
                        pos.x = pos.min_x
                        pos.y = pos.max_y
            else:
                _, height = get_space(ops, pos)
                one_line = height <= ops.get_height_of_text(".", self.style) + self.style.space_after

                super_instr(ops, pos, get_space)
                pos.x = pos.min_x
                if one_line:
                    pos.y -= height

        return PDFEvaluation(space, instr)
