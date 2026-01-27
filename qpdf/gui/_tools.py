import tkinter
import tkinter.ttk
import typing

from ._pdf_tools import PdfAppend, QpdfTool
from .core import QpdfToolsMetadata, QpdfToolType


class QpdfTools(tkinter.ttk.Frame):
    def __init__(self, parent: tkinter.ttk.Frame, home_action: typing.Callable[[], None]) -> None:
        super().__init__(parent)

        self._sidebar = tkinter.ttk.Frame(self)
        self._sidebar.pack(side="right", fill="y", padx=5, pady=5)
        tkinter.ttk.Button(self._sidebar, text="Home", command=home_action).pack(fill="x", pady=2)
        self._view_select = tkinter.ttk.Button(self._sidebar)
        self._view_select.pack(side="bottom", fill="x", pady=2)

        container = tkinter.ttk.Frame(self)
        container.pack(side="left", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._notebook = tkinter.ttk.Notebook(container)
        self._tabs: typing.MutableMapping[QpdfToolType, QpdfTool] = {QpdfToolType.PDF_APPEND: PdfAppend(self._notebook)}
        for tool, tab in self._tabs.items():
            self._notebook.add(tab, text=tool.value)

        self._preview = tkinter.ttk.Frame(container)
        tkinter.ttk.Label(self._preview, text="PDF Preview Area").pack(expand=True)

        self._notebook.grid(row=0, column=0, sticky="nsew")
        self._preview.grid(row=0, column=0, sticky="nsew")
        self.hide_preview()

    def select_tab(self, tool: QpdfToolType) -> None:
        self._notebook.select(self._tabs.get(tool, None))
        self.hide_preview()
        self.tkraise()

    def get_metadata(self) -> typing.Sequence[QpdfToolsMetadata]:
        return [QpdfToolsMetadata(name, tool.BRIEF, lambda: self.select_tab(name)) for name, tool in self._tabs.items()]

    def show_preview(self) -> None:
        self._view_select.configure(text="Hide Preview", command=self.hide_preview)
        self._preview.tkraise()

    def hide_preview(self) -> None:
        self._view_select.configure(text="Show Preview", command=self.show_preview)
        self._notebook.tkraise()
