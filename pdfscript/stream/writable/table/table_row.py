from pdfscript.__spi__.adapter import PDFOpsetAdapter
from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.pdf_writer import PDFWriter
from pdfscript.__spi__.protocols import PDFOpset, PDFListener
from pdfscript.__spi__.styles import TableRowStyle, TextStyle
from pdfscript.__spi__.types import PDFPosition, Space, BoundingBox, PDFCoords
from pdfscript.__util__.array_util import flatten
from pdfscript.stream.listener.noop_listener import NoOpListener
from pdfscript.stream.writable.table.table_col_writer import TableColWriter


class TableRow(Writable):

    def __init__(self, configurer: TableColWriter, style: TableRowStyle, listener: PDFListener = NoOpListener()):
        self.configurer = configurer
        self.style = style
        self.listener = listener

    @property
    def gap(self):
        return (len(self.configurer.objects) - 1) * self.style.gap

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = TableColWriter(context)
        writer.objects = self.configurer.objects
        evaluations = writer.write()

        def space(ops: PDFOpset, pos: PDFPosition):
            col_width = (pos.max_x - pos.min_x - self.gap) / len(evaluations)

            spaces = []
            new_pos = pos.copy()
            for evaluation in evaluations:
                new_pos = new_pos.with_max_x(new_pos.x + col_width)
                col_space = evaluation.space(ops, new_pos)

                new_pos.x += col_width
                spaces.append(col_space)
                new_pos.x += self.style.gap

            max_height = max([e.height for e in spaces])
            return Space(pos.max_x - pos.x, max_height).emit(self.listener, ops)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            col_width = (pos.max_x - pos.min_x - self.gap) / len(evaluations)

            width, height = get_space(ops, pos)
            bbox = BoundingBox(ops.page(), pos.x, pos.y, pos.x + width, pos.y - height)

            new_pos = pos.copy()
            replay_buffer = []
            for evaluation in evaluations:
                new_pos = new_pos.with_max_x(new_pos.x + col_width)
                ops_adapter = NewPageReplayBuffer(ops)

                evaluation.instr(ops_adapter, new_pos, evaluation.space, row_height=height)

                new_pos.x += col_width
                new_pos.min_x += col_width

                replay_buffer.append(ops_adapter)
                new_pos.x += self.style.gap

            if len(flatten(replay_buffer)) > 0:
                ops.add_page()
                pos.pos_zero()

                # create synthetic table row
                col_writer = TableColWriter(context)

                for i, col_items in enumerate(replay_buffer):
                    col_ref = self.configurer.objects[i]

                    col = col_writer.col(col_ref.style)
                    for item in col_items:
                        item(col, col_ref.listener)

                row = TableRow(col_writer, self.style, self.listener)
                _space, _instr = row.evaluate(context)
                _instr(ops, pos, _space)
            else:
                pos.x = pos.min_x
                pos.y -= height

            return bbox.emit(self.listener, ops)

        return PDFEvaluation(space, instr)


class NewPageReplayBuffer(PDFOpsetAdapter, list):
    """
    tbd
    """

    def __init__(self, opset: PDFOpset):
        super().__init__(opset)
        self.store = False

    def add_text(self, text: str, coords: PDFCoords, styling: TextStyle):
        """
        tbd
        """

        if not self.store:
            return super().add_text(text, coords, styling)

        def wrapper(ops: PDFWriter, listener: PDFListener):
            ops.text(text, styling, listener=listener)

        self.append(wrapper)

    def add_page(self):
        """
        tbd
        """
        self.store = True
