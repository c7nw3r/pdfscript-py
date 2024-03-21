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

        def space(ops: PDFOpset, pos: PDFPosition):
            top, right, bottom, left = self.style.margin
            new_pos = pos.with_max_x(pos.max_x - right).with_x_offset(left)

            spaces = evaluations.get_spaces(ops, new_pos)

            height = sum([e.height for e in spaces]) + top + bottom
            w = pos.max_x - pos.x  # do not consider margin and gap

            return Space(w, height).emit(self.listener, ops)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier, **kwargs):
            width, height = get_space(ops, pos)
            top, right, bottom, left = self.style.margin

            height = kwargs.get("row_height", height)
            height = min(height, pos.y - pos.min_y)

            bbox = BoundingBox(ops.page(), pos.x, pos.y, pos.x + width, pos.y - height)

            ops.draw_line(pos.x, pos.y, pos.x + width, pos.y, self.style.border)  # top
            ops.draw_line(pos.x, pos.y, pos.x, pos.y - height, self.style.border)  # left
            ops.draw_line(pos.x + width, pos.y, pos.x + width, pos.y - height, self.style.border)  # right
            ops.draw_line(pos.x, pos.y - height, pos.x + width, pos.y - height, self.style.border)  # bottom

            x, y = pos
            pos.x += left
            pos.y -= top
            evaluations.execute(ops, pos.with_max_x(pos.max_x - right))

            pos.move_to(x, y)

            return bbox.emit(self.listener, ops)

        return PDFEvaluation(space, instr)
