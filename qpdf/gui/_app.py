import tkinter
import tkinter.ttk
import typing

from ._home import QpdfHome
from ._tools import QpdfTools


class QuickPdf(tkinter.Tk):
    def __init__(self, window_size: str = "640x480"):
        super().__init__()

        self.title("Quick PDF")
        self.geometry(window_size)

        container = tkinter.ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._home = QpdfHome(container, self)
        self._tools = QpdfTools(container, self)

        frames: typing.Sequence[tkinter.ttk.Frame] = [self._home, self._tools]
        for frame in frames:
            frame.grid(row=0, column=0, sticky="nsew")

        self._home.tkraise()

    def get_home(self) -> QpdfHome:
        return self._home

    def get_tools(self) -> QpdfTools:
        return self._tools
