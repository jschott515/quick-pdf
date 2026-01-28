import ctypes
import tkinter
import tkinter.ttk
import typing

from qpdf._info import AUTHOR, ICON, VERSION_MAJOR, VERSION_MINOR, VERSION_REV

from ._home import QpdfHome
from ._tools import QpdfTools


class QuickPdf(tkinter.Tk):
    def __init__(self, window_size: str = "640x480") -> None:
        super().__init__()
        app_id = f"{AUTHOR}.QuickPdf.v{VERSION_MAJOR}_{VERSION_MINOR}_{VERSION_REV}"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        self.title("Quick PDF")
        self.geometry(window_size)

        self.iconbitmap(ICON)

        container = tkinter.ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._tools = QpdfTools(container, home_action=lambda: self._home.tkraise())
        self._home = QpdfHome(container, self._tools.get_metadata())

        frames: typing.Sequence[tkinter.ttk.Frame] = [self._home, self._tools]
        for frame in frames:
            frame.grid(row=0, column=0, sticky="nsew")

        self._home.tkraise()
