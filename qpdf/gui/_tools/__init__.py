from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from qpdf.gui import QuickPdf

import enum
import tkinter
import tkinter.ttk
import typing

from ._append import PdfAppend


class QpdfToolType(enum.StrEnum):
    PDF_APPEND = "PDF Append"


class QpdfTools(tkinter.ttk.Frame):
    def __init__(self, parent: tkinter.ttk.Frame, app: QuickPdf):
        super().__init__(parent)
        self._app = app

        self._notebook = tkinter.ttk.Notebook(self)
        self._notebook.pack(fill="both", expand=True)

        self._tabs: typing.MutableMapping[QpdfTools, tkinter.ttk.Frame] = {
            QpdfToolType.PDF_APPEND: PdfAppend(self._notebook)
        }

        for tool, tab in self._tabs.items():
            self._notebook.add(tab, text=tool)

        tkinter.ttk.Button(self, text="Home", command=app.get_home().tkraise).pack(anchor="e", padx=5, pady=5)

    def select_tab(self, tool: QpdfToolType):
        # FIXME Fails silently...
        self._notebook.select(self._tabs.get(tool, None))
