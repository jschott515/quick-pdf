import abc
import tkinter
import tkinter.messagebox
import tkinter.ttk

import pymupdf

import qpdf


class QpdfTool(abc.ABC, tkinter.ttk.Frame):
    BRIEF = "Quick-PDF Tool"

    def get_pdf(self) -> pymupdf.Document | None:
        try:
            return self._get_pdf()
        except qpdf.QpdfException as e:
            tkinter.messagebox.showwarning("Quick PDF Error", repr(e))
        return None

    @abc.abstractmethod
    def _get_pdf(self) -> pymupdf.Document:
        """Return a PDFWriter with the result of the tool's operation."""

    @abc.abstractmethod
    def reset(self) -> None:
        """Reset the tool."""
