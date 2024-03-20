from typing import Callable

from pdfscript.__spi__.pdf_context import PDFContext
from pdfscript.__spi__.pdf_writable import PDFEvaluations
from pdfscript.__spi__.protocols import PDFListener
from pdfscript.__spi__.styles import TextStyle
from pdfscript.stream.listener.noop_listener import NoOpListener
from pdfscript.stream.writable.list.list_item import ListItem

TableColConfigurer = Callable[['TableColWriter'], None]


class ListItemsWriter:

    def __init__(self, context: PDFContext):
        self.context = context
        self.objects = []

    def write(self) -> PDFEvaluations:
        return PDFEvaluations([e.evaluate(self.context) for e in self.objects])

    def list_item(self, content: str, style: TextStyle = TextStyle(), listener: PDFListener = NoOpListener()):
        self.objects.append(ListItem(content, style, listener))
