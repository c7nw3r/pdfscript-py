from abc import ABC, abstractmethod
from typing import Callable, List

from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation
from pdfscript.__spi__.protocols import PDFOpset
from pdfscript.__spi__.types import PDFPosition, Space


class Writable(ABC):

    @abstractmethod
    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        pass


class PDFEvaluations:
    def __init__(self, evaluations: List[PDFEvaluation]):
        self.evaluations = evaluations

    def get_spaces(self,
                   stream: PDFOpset,
                   box: PDFPosition,
                   x_offset: bool = True,
                   y_offset: bool = True,
                   postprocess: Callable[[PDFPosition, Space], None] = lambda x, y: None):

        copy = box.copy()

        def to_space(evaluation: PDFEvaluation):
            space = evaluation.space(stream, copy)

            if x_offset:
                copy.move_x_offset(space.width)
            if y_offset:
                copy.move_y_offset(space.height)
            if postprocess:
                postprocess(copy, space)

            return space

        return [to_space(e) for e in self.evaluations]

    def execute(self,
                stream: PDFOpset,
                box: PDFPosition,
                postprocess: Callable[[], None] = lambda: None,
                **kwargs):
        for evaluation in self.evaluations:
            evaluation.instr(stream, box, evaluation.space, **kwargs)
            if postprocess:
                postprocess()

    def __len__(self):
        return len(self.evaluations)

    def __iter__(self):
        for evaluation in self.evaluations:
            yield evaluation
