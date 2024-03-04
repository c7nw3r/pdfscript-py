from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_opset import PDFOpset
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.__spi__.styles import TableColStyle
from pdfscript.__spi__.types import PDFPosition, Space


class TableCol(Writable):

    def __init__(self, configurer: PDFWriter, style: TableColStyle):
        self.configurer = configurer
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        new_context = PDFContext(context.format, context.margin)

        writer = PDFWriter(new_context)
        writer.objects = self.configurer.objects
        evaluations = writer.write()

        def get_gap(pos: PDFPosition):
            is_first = pos.x == context.margin.left
            is_last = pos.max_x == context.format.value[0] - context.margin.right
            return [0 if is_first else self.style.gap / 2, 0 if is_last else self.style.gap / 2]

        def space(ops: PDFOpset, pos: PDFPosition):
            spaces = evaluations.get_spaces(ops, pos)

            top, _, bottom, _ = self.style.margin
            height = sum([e.height for e in spaces]) + top + bottom

            return Space(pos.max_x - pos.x + sum(get_gap(pos)), height)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            width, _ = get_space(ops, pos)
            height = pos.y - pos.max_y

            ops.draw_line(pos.x, pos.y, pos.x + width, pos.y, self.style.border)  # top
            ops.draw_line(pos.x, pos.y, pos.x, pos.y - height, self.style.border)  # left
            ops.draw_line(pos.x + width, pos.y, pos.x + width, pos.y - height, self.style.border)  # right
            ops.draw_line(pos.x, pos.y - height, pos.x + width, pos.y - height, self.style.border)  # bottom

            x, y = pos
            pos.x += self.style.margin.left + get_gap(pos)[0]
            evaluations.execute(ops, pos.with_max_x(pos.max_x - self.style.margin.right))
            pos.move_to(x, y)

            pos.x += width + get_gap(pos)[1]

        return PDFEvaluation(space, instr)
