import math

from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.__spi__.pdf_writer_api import Configurer
from pdfscript.__spi__.styles import VStackStyle
from pdfscript.__spi__.types import BoundingBox, Space


class HStack(Writable):

    def __init__(self, configurer: Configurer, style: VStackStyle):
        self.configurer = configurer
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = PDFWriter(context)
        self.configurer(writer)
        evaluations = writer.write()

        def space(ops: PDFApi, pos: BoundingBox):
            spaces = evaluations.get_spaces(ops, pos, True, False)

            width = sum([e.width for e in spaces]) + self.style.gap
            height = max([e.height for e in spaces]) + self.style.margin.bottom
            return Space(width, height)

        def instr(ops: PDFApi, pos: BoundingBox, get_space: SpaceSupplier):
            if self.style.align == "right":
                pos.x += math.floor(pos.max_x - pos.x - get_space(ops, pos).width)
                evaluations.execute(ops, pos)

            elif self.style.align == "justify":
                width, _ = get_space(ops, pos)
                gap = math.floor((pos.max_x - pos.x) - width) / (len(evaluations) - 1)

                def postprocess():
                    pos.x += gap

                evaluations.execute(ops, pos, postprocess)

            else:
                def postprocess():
                    pos.x += self.style.gap

                evaluations.execute(ops, pos, postprocess)

        return PDFEvaluation(space, instr)
