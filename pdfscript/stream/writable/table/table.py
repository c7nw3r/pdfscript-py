from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.styles import RectStyle
from pdfscript.__spi__.types import PDFPosition, Space, BoundingBox
from pdfscript.stream.listener.noop_listener import NoOpListener
from pdfscript.stream.writable.table.table_row_writer import TableRowWriter


class Table(Writable):

    def __init__(self, configurer: TableRowWriter, listener: PDFListener = NoOpListener()):
        self.configurer = configurer
        self.listener = listener

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = TableRowWriter(context)
        writer.objects = self.configurer.objects
        evaluations = writer.write()

        def space(ops: PDFOpset, pos: PDFPosition):
            spaces = evaluations.get_spaces(ops, pos)
            width = pos.max_x - pos.x
            height = sum([e.height for e in spaces])
            return Space(width, height).emit(self.listener, ops)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            width, height = get_space(ops, pos)

            if pos.x > pos.min_x:
                pos.x = pos.min_x
                pos.y -= 20  # FIXME: magic number

            bbox = BoundingBox(pos.x, pos.y, pos.x + width, pos.y - height)
            if context.draw_bbox:
                ops.draw_rect(bbox.x1, bbox.y1, bbox.x2, bbox.y2, RectStyle(stroke_color="red"))

            evaluations.execute(ops, pos)
            return bbox.emit(self.listener, ops)

        return PDFEvaluation(space, instr)
