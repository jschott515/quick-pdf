import tkinter
import tkinter.ttk


class PdfAppend(tkinter.ttk.Frame):
    def __init__(self, parent: tkinter.ttk.Frame):
        super().__init__(parent)

        self._label = tkinter.ttk.Label(self, text="")
        self._label.pack(anchor="w", padx=20, pady=20)
