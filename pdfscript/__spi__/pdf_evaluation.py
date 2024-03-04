from typing import Callable

from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.types import BoundingBox, Space

ExecutionSpace = Callable[[PDFApi, BoundingBox], Space]
ExecutionInstr = Callable[[PDFApi, BoundingBox, ExecutionSpace], None]
SpaceSupplier = Callable[[PDFApi, BoundingBox], Space]


class PDFEvaluation:
    def __init__(self, space: ExecutionSpace, instr: ExecutionInstr):
        self.space = space
        self.instr = instr