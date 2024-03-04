from abc import ABC, abstractmethod
from typing import Callable

from pdfscript.__spi__.pdf_writable import PDFEvaluations
from pdfscript.__spi__.styles import TextStyle, ImageStyle, VStackStyle


class PDFWriterApi(ABC):

    @abstractmethod
    def text(self, content: str, style: TextStyle = TextStyle()):
        pass

    @abstractmethod
    def image(self, src: str, style: ImageStyle = ImageStyle()):
        pass

    @abstractmethod
    def v_stack(self, configurer: 'Configurer', style: VStackStyle = VStackStyle()):
        pass

    @abstractmethod
    def write(self) -> PDFEvaluations:
        pass


Configurer = Callable[[PDFWriterApi], None]
