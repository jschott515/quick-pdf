from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from ._app import QuickPdf

import tkinter
import tkinter.ttk

from ._tools import QpdfToolType


class QpdfHome(tkinter.ttk.Frame):
    def __init__(self, parent: tkinter.ttk.Frame, app: QuickPdf):
        super().__init__(parent)
        self._app = app

        tkinter.ttk.Label(self, text="Welcome to Quick PDF!", font=("TkDefaultFont", 14, "bold")).pack(
            anchor="w", padx=20, pady=20
        )

        for tool in QpdfToolType:
            tkinter.ttk.Button(self, text=tool, command=lambda: self.open_tool(tool)).pack(anchor="w", padx=40, pady=5)

    def open_tool(self, tool: QpdfToolType):
        frame = self._app.get_tools()
        frame.select_tab(tool)
        frame.tkraise()
