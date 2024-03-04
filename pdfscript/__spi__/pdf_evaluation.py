from typing import Callable

from pdfscript.__spi__.pdf_opset import PDFOpset
from pdfscript.__spi__.types import PDFPosition, Space

ExecutionSpace = Callable[[PDFOpset, PDFPosition], Space]
ExecutionInstr = Callable[[PDFOpset, PDFPosition, ExecutionSpace], None]
SpaceSupplier = Callable[[PDFOpset, PDFPosition], Space]


class PDFEvaluation:
    def __init__(self, space: ExecutionSpace, instr: ExecutionInstr):
        self.space = space
        self.instr = instr