import abc
import tkinter
import tkinter.ttk

import pymupdf


class QpdfTool(abc.ABC, tkinter.ttk.Frame):
    BRIEF = "Quick-PDF Tool"

    @abc.abstractmethod
    def get_pdf(self) -> pymupdf.Document:
        """Return a PDFWriter with the result of the tool's operation."""
