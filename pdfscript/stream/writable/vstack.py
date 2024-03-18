from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.styles import VStackStyle
from pdfscript.__spi__.types import PDFPosition, Space, BoundingBox
from pdfscript.stream.listener.noop_listener import NoOpListener


class VStack(Writable):

    def __init__(self, configurer: PDFWriter, style: VStackStyle, listener: PDFListener = NoOpListener()):
        self.configurer = configurer
        self.style = style
        self.listener = listener

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = PDFWriter(context)
        writer.objects = self.configurer.objects
        evaluations = writer.write()

        def space(ops: PDFOpset, pos: PDFPosition):
            spaces = [e for e in evaluations.get_spaces(ops, pos, False)]
            margin = self.style.margin.bottom + self.style.margin.top

            width = max([e.width for e in spaces])
            height = sum([e.height for e in spaces]) + margin + self.style.gap

            return Space(width, height).emit(self.listener, ops)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            x = pos.x
            width, height = get_space(ops, pos)
            pos.move_y_offset(self.style.margin.top)

            bbox = BoundingBox(ops.page(), pos.x, pos.y, pos.x + width, pos.y - height)

            index = 0
            for evaluation in evaluations:
                height = evaluation.space(ops, pos).height

                y = pos.y
                evaluation.instr(ops, pos, evaluation.space)
                pos.x = x
                pos.y = y - height

                index += 1

            return bbox.emit(self.listener, ops)

        return PDFEvaluation(space, instr)
