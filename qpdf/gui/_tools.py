import dataclasses
import tkinter
import tkinter.ttk
import typing

from ._pdf_tools import PdfAppend, QpdfTool
from .core import QpdfToolsMetadata, QpdfToolType


class QpdfTools(tkinter.ttk.Frame):
    def __init__(self, parent: tkinter.ttk.Frame, home_action: typing.Callable[[], None]) -> None:
        super().__init__(parent)

        tkinter.ttk.Button(self, text="Home", command=home_action).pack(side="right", anchor="n", padx=5)
        self._notebook = tkinter.ttk.Notebook(self)

        self._tabs: typing.MutableMapping[QpdfToolType, QpdfTool] = {QpdfToolType.PDF_APPEND: PdfAppend(self._notebook)}

        self._notebook.pack(fill="both", expand=True)
        for tool, tab in self._tabs.items():
            self._notebook.add(tab, text=tool)

    def select_tab(self, tool: QpdfToolType) -> None:
        self._notebook.select(self._tabs.get(tool, None))
        self.tkraise()

    def get_metadata(self) -> typing.Sequence[QpdfToolsMetadata]:
        return [QpdfToolsMetadata(name, tool.BRIEF, lambda: self.select_tab(name)) for name, tool in self._tabs.items()]
