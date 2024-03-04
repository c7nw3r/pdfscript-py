from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.__spi__.pdf_writer_api import Configurer
from pdfscript.__spi__.styles import HStackStyle
from pdfscript.__spi__.types import BoundingBox, Space


class VStack(Writable):

    def __init__(self, configurer: Configurer, style: HStackStyle):
        self.configurer = configurer
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = PDFWriter(context)
        self.configurer(writer)
        evaluations = writer.write()

        def space(ops: PDFApi, pos: BoundingBox):
            spaces = [e for e in evaluations.get_spaces(ops, pos, False)]

            total_gap = self.style.gap * (len(evaluations) - 1)
            margin = self.style.margin.bottom + self.style.margin.top

            width = max([e.width for e in spaces])
            height = sum([e.height for e in spaces]) + margin + total_gap

            return Space(width, height)

        def instr(ops: PDFApi, pos: BoundingBox, _get_space: SpaceSupplier):
            x = pos.x
            pos.move_y_offset(self.style.margin.top)

            index = 0
            for evaluation in evaluations:
                is_last = index == len(evaluations) - 1
                height = evaluation.space(ops, pos).height + (0 if is_last else self.style.gap)

                y = pos.y
                evaluation.instr(ops, pos, evaluation.space)
                pos.x = x

                if (pos.y - y) < height:
                    pos.y += (height - (pos.y - y))

                index += 1

        return PDFEvaluation(space, instr)
