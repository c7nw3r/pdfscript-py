from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.styles import TableStyle
from pdfscript.__spi__.types import BoundingBox, Space
from pdfscript.stream.writable.table.table_col_writer import TableColWriter, TableColConfigurer


class TableRow(Writable):

    def __init__(self, configurer: TableColConfigurer, style: TableStyle):
        self.configurer = configurer
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = TableColWriter(context)
        self.configurer(writer)
        evaluations = writer.write()

        def space(ops: PDFApi, pos: BoundingBox):
            new_pos = pos.with_max_x(pos.x + pos.max_x / len(evaluations))

            def postprocess(_pos: BoundingBox, _space: Space):
                _pos.max_x += pos.max_x / len(evaluations)

            spaces = evaluations.get_spaces(ops, new_pos, True, False, postprocess)
            return Space(pos.max_x, max([e.height for e in spaces]))

        def instr(ops: PDFApi, pos: BoundingBox, get_space: SpaceSupplier):
            _, height = get_space(ops, pos.with_max_x(pos.max_x / len(evaluations)))

            if (pos.y - height) < pos.min_y:
                ops.add_page()
                pos.y = pos.min_y

            col_max_x = pos.x + (pos.max_x - pos.min_x) / len(evaluations)
            new_pos = pos.with_max_x(col_max_x).with_max_y(pos.y - height)

            # new_pos.move_y_offset() margin top

            def postprocess():
                new_pos.min_x += (pos.max_x - pos.min_x) / len(evaluations)
                new_pos.max_x += (pos.max_x - pos.min_x) / len(evaluations)

            evaluations.execute(ops, new_pos, postprocess)

            pos.x = pos.min_x
            pos.y -= height

        return PDFEvaluation(space, instr)
