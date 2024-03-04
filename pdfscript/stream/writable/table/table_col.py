from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.__spi__.pdf_writer_api import Configurer
from pdfscript.__spi__.styles import TableColStyle
from pdfscript.__spi__.types import BoundingBox, Space


class TableCol(Writable):

    def __init__(self, configurer: Configurer, style: TableColStyle):
        self.configurer = configurer
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        new_style = {}
        new_context = PDFContext(context.page_format, context.page_margin)

        # const newStyles = {...context.styles, ...{margin: {left: 2}}}
        # const newContext = new Context(context.format, context.margin, newStyles)

        writer = PDFWriter(new_context)
        self.configurer(writer)
        evaluations = writer.write()

        def space(ops: PDFApi, pos: BoundingBox):
            spaces = evaluations.get_spaces(ops, pos)

            margin = self.style.margin
            height = sum([e.height for e in spaces]) + margin.top + margin.bottom

            return Space(pos.max_x - pos.x, height)

        def instr(ops: PDFApi, pos: BoundingBox, get_space: SpaceSupplier):
            # border = None

            width, _ = get_space(ops, pos)
            height = pos.y - pos.max_y

            ops.draw_line(pos.x, pos.y, pos.x + width, pos.y)  # top
            ops.draw_line(pos.x, pos.y, pos.x, pos.y - height)  # left
            ops.draw_line(pos.x + width, pos.y, pos.x + width, pos.y - height)  # right
            ops.draw_line(pos.x, pos.y - height, pos.x + width, pos.y - height)  # bottom

            x, y = pos
            pos.x += self.style.margin.left
            evaluations.execute(ops, pos)
            pos.move_to(x, y)

            pos.x += width

        return PDFEvaluation(space, instr)
