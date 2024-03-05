from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.styles import TableColStyle
from pdfscript.__spi__.types import PDFPosition, Space, BoundingBox
from pdfscript.stream.listener.noop_listener import NoOpListener


class TableCol(Writable):

    def __init__(self, configurer: PDFWriter, style: TableColStyle, listener: PDFListener = NoOpListener()):
        self.configurer = configurer
        self.style = style
        self.listener = listener

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        new_context = PDFContext(context.format, context.margin)

        writer = PDFWriter(new_context)
        writer.objects = self.configurer.objects
        evaluations = writer.write()

        def get_gap(pos: PDFPosition):
            is_first = pos.x == context.margin.left
            is_last = pos.max_x == context.format.value[0] - context.margin.right
            return [0 if is_first else self.style.gap, 0 if is_last else self.style.gap]

        def space(ops: PDFOpset, pos: PDFPosition):
            spaces = evaluations.get_spaces(ops, pos)

            top, _, bottom, _ = self.style.margin
            height = sum([e.height for e in spaces]) + top + bottom

            return Space(pos.max_x - pos.x - self.style.gap, height).emit(self.listener)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            width, height = get_space(ops, pos)

            bbox = BoundingBox(pos.x, pos.y, pos.x + width, pos.y - height)
            pos.with_x_offset(get_gap(pos)[0])

            ops.draw_line(pos.x, pos.y, pos.x + width, pos.y, self.style.border)  # top
            ops.draw_line(pos.x, pos.y, pos.x, pos.y - height, self.style.border)  # left
            ops.draw_line(pos.x + width, pos.y, pos.x + width, pos.y - height, self.style.border)  # right
            ops.draw_line(pos.x, pos.y - height, pos.x + width, pos.y - height, self.style.border)  # bottom

            x, y = pos
            pos.x += self.style.margin.left
            evaluations.execute(ops, pos.with_max_x(pos.max_x - self.style.margin.right - self.style.gap))
            pos.move_to(x, y)

            pos.x += width + get_gap(pos)[1]
            return bbox.emit(self.listener)

        return PDFEvaluation(space, instr)
