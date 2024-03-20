from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.protocols import PDFListener, PDFOpset
from pdfscript.__spi__.types import PDFPosition, Space
from pdfscript.stream.listener.noop_listener import NoOpListener
from pdfscript.stream.writable.list.list_items_writer import ListItemsWriter


class ListItems(Writable):

    def __init__(self, configurer: ListItemsWriter, listener: PDFListener = NoOpListener()):
        self.configurer = configurer
        self.listener = listener

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = ListItemsWriter(context)
        writer.objects = self.configurer.objects
        evaluations = writer.write()

        def space(ops: PDFOpset, pos: PDFPosition):
            spaces = evaluations.get_spaces(ops, pos)
            width = pos.max_x - pos.x
            height = sum([e.height for e in spaces])
            return Space(width, height).emit(self.listener, ops)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):

            evaluations.execute(ops, pos)
            # return bbox.emit(self.listener, ops)

        return PDFEvaluation(space, instr)

