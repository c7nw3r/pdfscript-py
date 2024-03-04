from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_opset import PDFOpset
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.__spi__.styles import VStackStyle
from pdfscript.__spi__.types import PDFPosition, Space


class VStack(Writable):

    def __init__(self, configurer: PDFWriter, style: VStackStyle):
        self.configurer = configurer
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = PDFWriter(context)
        writer.objects = self.configurer.objects
        evaluations = writer.write()

        def space(ops: PDFOpset, pos: PDFPosition):
            spaces = [e for e in evaluations.get_spaces(ops, pos, False)]

            # total_gap = self.style.gap * (len(evaluations) - 1)
            margin = self.style.margin.bottom + self.style.margin.top

            width = max([e.width for e in spaces])
            height = sum([e.height for e in spaces]) + margin + self.style.gap

            return Space(width, height)

        def instr(ops: PDFOpset, pos: PDFPosition, _get_space: SpaceSupplier):
            x = pos.x
            pos.move_y_offset(self.style.margin.top)

            index = 0
            for evaluation in evaluations:
                # is_last = index == len(evaluations) - 1
                height = evaluation.space(ops, pos).height

                y = pos.y
                evaluation.instr(ops, pos, evaluation.space)
                pos.x = x
                pos.y = y - height

                index += 1

        return PDFEvaluation(space, instr)
