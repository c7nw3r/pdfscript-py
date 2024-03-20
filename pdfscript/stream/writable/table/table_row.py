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

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        writer = TableColWriter(context)
        writer.objects = self.configurer.objects
        evaluations = writer.write()

        def space(ops: PDFOpset, pos: PDFPosition):
            new_pos = pos.with_max_x(pos.x + (pos.max_x - pos.min_x) / len(evaluations))

            def postprocess(_pos: PDFPosition, _space: Space):
                _pos.max_x += ((pos.max_x - pos.min_x) / len(evaluations))
                _pos.x += ((pos.max_x - pos.min_x) / len(evaluations))

            spaces = evaluations.get_spaces(ops, new_pos, True, False, postprocess)
            return Space(pos.max_x - pos.x, max([e.height for e in spaces])).emit(self.listener, ops)

        def instr(ops: PDFOpset, pos: PDFPosition, get_space: SpaceSupplier):
            width, height = get_space(ops, pos)
            bbox = BoundingBox(ops.page(), pos.x, pos.y, pos.x + width, pos.y - height)

            # if (pos.y - height) < pos.min_y:
            #     ops.add_page()
            #     pos.y = pos.max_y

            col_max_x = pos.x + (pos.max_x - pos.min_x) / len(evaluations)
            new_pos = pos.with_max_x(col_max_x)  # .with_max_y(pos.y - height)

            # def preprocess(_ops: PDFOpset):
            #     return NewPageReplayBuffer(ops)

            # def postprocess(_ops: PDFOpset):
            #     new_pos.min_x += (pos.max_x - pos.min_x) / len(evaluations)
            #     new_pos.max_x += (pos.max_x - pos.min_x) / len(evaluations)
            #     return _ops
            replay_buffer = []
            for evaluation in evaluations:
                ops_adapter = NewPageReplayBuffer(ops)
                evaluation.instr(ops_adapter, new_pos, evaluation.space, row_height=height)
                new_pos.min_x += (pos.max_x - pos.min_x) / len(evaluations)
                new_pos.max_x += (pos.max_x - pos.min_x) / len(evaluations)
                replay_buffer.append(ops_adapter)

            # ops_adapter = NewPageReplayBuffer(ops)
            # evaluations.execute(ops, new_pos, postprocess, preprocess, row_height=height)

            if len(flatten(replay_buffer)) > 0:
                ops.add_page()
                pos.pos_zero()

                # create synthetic table row
                col_writer = TableColWriter(context)

                for i, col_items in enumerate(replay_buffer):
                    col_ref = self.configurer.objects[i]

                    col = col_writer.col(col_ref.style)
                    for item in col_items:
                        item(col)

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

        def wrapper(ops: PDFWriter):
            ops.text(text, styling)

        self.append(wrapper)

    def add_page(self):
        """
        tbd
        """
        self.store = True
