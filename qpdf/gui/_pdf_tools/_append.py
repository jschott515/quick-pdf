import tkinter
import tkinter.ttk

from ._core import QpdfTool


class PdfAppend(QpdfTool):
    BRIEF = "Combine multiple PDF files into one!"

    def __init__(self, parent: tkinter.ttk.Notebook) -> None:
        super().__init__(parent)

        self._label = tkinter.ttk.Label(self, text="Select files to append:", font=("Arial", 10, "bold"))
        self._label.pack(anchor="w", padx=10, pady=5)

        self._tree = tkinter.ttk.Treeview(self)
        self._tree.pack(anchor="n", padx=10, pady=5, expand=True, fill="x")
