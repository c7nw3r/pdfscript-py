from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.styles import TableStyle
from pdfscript.__spi__.types import BoundingBox, Space
from pdfscript.stream.writable.table.table_row_writer import TableRowWriter, TableRowConfigurer


class Table(Writable):

    def __init__(self, configurer: TableRowConfigurer, style: TableStyle):
        self.configurer = configurer
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = TableRowWriter(context)
        self.configurer(writer)
        evaluations = writer.write()

        def space(ops: PDFApi, pos: BoundingBox):
            spaces = evaluations.get_spaces(ops, pos)
            width = context.page_format.value[0]
            height = sum([e.height for e in spaces])
            return Space(width, height)

        def instr(ops: PDFApi, pos: BoundingBox, _get_space: SpaceSupplier):
            return evaluations.execute(ops, pos)

        return PDFEvaluation(space, instr)
