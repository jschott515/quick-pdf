import tkinter
import tkinter.ttk
import typing

from .core import QpdfToolsMetadata


class QpdfPreview(tkinter.ttk.Frame):
    def __init__(self, parent: tkinter.ttk.Frame, title: str, description: str, on_click: typing.Callable[[], None]):
        super().__init__(parent)

        tkinter.ttk.Button(self, text=title, command=on_click).pack(anchor="w")
        tkinter.ttk.Label(self, text=description, wraplength=200).pack(pady=5, anchor="w")


class QpdfHome(tkinter.ttk.Frame):
    def __init__(self, parent: tkinter.ttk.Frame, supported_tools: typing.Sequence[QpdfToolsMetadata]) -> None:
        super().__init__(parent)

        tkinter.ttk.Label(self, text="Welcome to Quick PDF!", font=("Arial", 14, "bold")).pack(
            anchor="w", padx=20, pady=20
        )

        container = tkinter.ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        for tool in supported_tools:
            QpdfPreview(container, title=str(tool.name), description=tool.desc, on_click=tool.launch).pack(
                pady=10, fill="x"
            )
