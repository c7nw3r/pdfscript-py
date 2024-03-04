from pdfscript.__spi__.pdf_api import PDFApi
from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_evaluation import PDFEvaluation, SpaceSupplier
from pdfscript.__spi__.pdf_writable import Writable
from pdfscript.__spi__.styles import ImageStyle
from pdfscript.__spi__.types import Space, BoundingBox


class Image(Writable):
    def __init__(self, src: str, style: ImageStyle):
        self.src = src
        self.style = style

    def evaluate(self, context: PDFContext) -> PDFEvaluation:
        def space(_api: PDFApi, _box: BoundingBox):
            return Space(self.style.width, self.style.height)

        def instr(api: PDFApi, box: BoundingBox, get_space: SpaceSupplier):
            width, height = get_space(api, box)

            x = box.x
            if self.style.align == "center":
                x += ((box.max_x - box.min_x) / 2) - (width / 2)

            api.add_image(self.src, box, self.style)

            if self.style.display == "block":
                box.x = box.min_x
                box.y += height
            else:
                box.x = x + width

        return PDFEvaluation(space, instr)
