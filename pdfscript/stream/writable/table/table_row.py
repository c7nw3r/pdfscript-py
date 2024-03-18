from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.styles import TableRowStyle
from pdfscript.__spi__.types import PDFPosition, Space, BoundingBox
from pdfscript.stream.listener.noop_listener import NoOpListener
from pdfscript.stream.writable.table.table_col_writer import TableColWriter


class TableRow(Writable):

    def __init__(self, configurer: TableColWriter, style: TableRowStyle, listener: PDFListener = NoOpListener()):
        self.configurer = configurer
        self.style = style
        self.listener = listener

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = TableColWriter(context)
        writer.objects = self.configurer.objects
        evaluations = writer.write()

        def space(ops: PDFOpset, pos: PDFPosition):
            new_pos = pos.with_max_x(pos.x + (pos.max_x - pos.min_x) / len(evaluations))

            def postprocess(_pos: PDFPosition, _space: Space):
                _pos.max_x += ((pos.max_x - pos.min_x) / len(evaluations))
                _pos.x += ((pos.max_x - pos.min_x) / len(evaluations))

            spaces = evaluations.get_spaces(ops, new_pos, True, False, postprocess)
            return Space(pos.max_x - pos.x, max([e.height for e in spaces])).emit(self.listener, ops)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            width, height = get_space(ops, pos)
            bbox = BoundingBox(ops.page(), pos.x, pos.y, pos.x + width, pos.y - height)

            if (pos.y - height) < pos.min_y:
                ops.add_page()
                pos.y = pos.max_y

            col_max_x = pos.x + (pos.max_x - pos.min_x) / len(evaluations)
            new_pos = pos.with_max_x(col_max_x).with_max_y(pos.y - height)

            def postprocess():
                new_pos.min_x += (pos.max_x - pos.min_x) / len(evaluations)
                new_pos.max_x += (pos.max_x - pos.min_x) / len(evaluations)

            evaluations.execute(ops, new_pos, postprocess)

            pos.x = pos.min_x
            pos.y -= height

            return bbox.emit(self.listener, ops)

        return PDFEvaluation(space, instr)
