import math

from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_opset import PDFOpset
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.__spi__.styles import Align, HStackStyle
from pdfscript.__spi__.types import PDFPosition, Space


class HStack(Writable):

    def __init__(self, configurer: PDFWriter, style: HStackStyle):
        self.configurer = configurer
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = PDFWriter(context)
        writer.objects = self.configurer.objects
        evaluations = writer.write()

        def space(ops: PDFOpset, pos: PDFPosition):
            spaces = evaluations.get_spaces(ops, pos, True, False)

            width = sum([e.width for e in spaces]) + self.style.gap
            height = max([e.height for e in spaces]) + self.style.margin.bottom
            return Space(width, height)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            original_y = pos.y

            if self.style.align == Align.RIGHT:
                pos.x += math.floor(pos.max_x - pos.x - get_space(ops, pos).width)
                evaluations.execute(ops, pos)

            elif self.style.align == Align.JUSTIFY:
                width, _ = get_space(ops, pos)
                gap = math.floor((pos.max_x - pos.x) - width) / (len(evaluations) - 1)

                def postprocess():
                    pos.x += gap

                evaluations.execute(ops, pos, postprocess)

            else:
                def postprocess():
                    pos.x += self.style.gap

                evaluations.execute(ops, pos, postprocess)

            pos.y = original_y

        return PDFEvaluation(space, instr)
