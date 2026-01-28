import tkinter
import tkinter.ttk
import typing
import webbrowser

from .core import QpdfToolsMetadata

ASCII_LOGO = r"""
  ██████╗ ██╗   ██╗██╗ ██████╗██╗  ██╗
 ██╔═══██╗██║   ██║██║██╔════╝██║ ██╔╝
 ██║   ██║██║   ██║██║██║     █████╔╝ 
 ██║▄▄ ██║██║   ██║██║██║     ██╔═██╗ 
 ╚██████╔╝╚██████╔╝██║╚██████╗██║  ██╗
  ╚══▀▀═╝  ╚═════╝ ╚═╝ ╚═════╝╚═╝  ╚═╝
           QUICK  PDF  TOOLS
"""


class QpdfWidget(tkinter.ttk.Frame):
    def __init__(
        self,
        parent: tkinter.ttk.Frame,
        title: str,
        description: str,
        on_click: typing.Callable[[], None],
    ):
        super().__init__(parent, padding=16, style="Card.TFrame")

        self.on_click = on_click

        style = tkinter.ttk.Style()
        style.configure("CardLabel.TLabel", background="white")
        style.configure("CardHoverLabel.TLabel", background="#f2f8ff")

        self._title = tkinter.ttk.Label(
            self,
            text=title,
            font=("Segoe UI", 12, "bold"),
            style="CardLabel.TLabel",
        )
        self._title.pack(anchor="w")

        self._desc = tkinter.ttk.Label(
            self,
            text=description,
            wraplength=300,
            foreground="#555",
            style="CardLabel.TLabel",
        )
        self._desc.pack(anchor="w", pady=(6, 12))

        self._on_click = tkinter.ttk.Label(
            self,
            text="▶ Open",
            foreground="#0066cc",
            style="CardLabel.TLabel",
        )
        self._on_click.pack(anchor="e")

        self._bind_hover_click(self)

    def _bind_hover_click(self, widget: tkinter.Widget | tkinter.Toplevel) -> None:
        # Bind to the widget itself
        widget.bind("<Enter>", lambda e: self._hover_on())
        widget.bind("<Leave>", lambda e: self._hover_off())
        widget.bind("<Button-1>", lambda e: self.on_click())

        # Recursively bind to all children
        for child in widget.winfo_children():
            self._bind_hover_click(child)

    def _hover_on(self) -> None:
        self.configure(style="CardHover.TFrame")
        self._title.configure(style="CardHoverLabel.TLabel")
        self._desc.configure(style="CardHoverLabel.TLabel")
        self._on_click.configure(style="CardHoverLabel.TLabel")

    def _hover_off(self) -> None:
        self.configure(style="Card.TFrame")
        self._title.configure(style="CardLabel.TLabel")
        self._desc.configure(style="CardLabel.TLabel")
        self._on_click.configure(style="CardLabel.TLabel")


class QpdfHome(tkinter.ttk.Frame):
    def __init__(
        self,
        parent: tkinter.ttk.Frame,
        supported_tools: typing.Sequence[QpdfToolsMetadata],
    ):
        super().__init__(parent)
        self._setup_styles()

        banner = tkinter.ttk.Frame(self, padding=20)
        banner.pack(fill="x")

        tkinter.Label(
            banner,
            text=ASCII_LOGO,
            font=("Courier New", 10),
            justify="left",
            fg="#222",
        ).pack(anchor="center")

        tkinter.ttk.Label(
            banner,
            text="Simple PDF utilities — pick a tool to get started",
            foreground="#444",
        ).pack(pady=(10, 0))

        tkinter.ttk.Separator(self).pack(fill="x", padx=40, pady=10)

        tools_area = tkinter.ttk.Frame(self, padding=30)
        tools_area.pack(fill="both", expand=True)

        for i, tool in enumerate(supported_tools):
            QpdfWidget(
                tools_area,
                title=str(tool.name),
                description=tool.desc,
                on_click=tool.launch,
            ).grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=15,
                pady=15,
            )
            tools_area.columnconfigure(i, weight=1)

        github_widget = QpdfWidget(
            tools_area,
            title="Contribute",
            description="More tools comming soon...",
            on_click=lambda: webbrowser.open("https://github.com/jschott515/quick-pdf"),
        )
        github_widget.grid(row=0, column=len(supported_tools), sticky="nsew", padx=15, pady=15)
        tools_area.columnconfigure(len(supported_tools), weight=1)

        footer = tkinter.ttk.Frame(self, padding=5)
        footer.pack(side="bottom", fill="x")

        tkinter.ttk.Label(
            footer,
            text="v0.1.0 - @jschott515",
            foreground="#777",
        ).pack(anchor="center")

    def _setup_styles(self):
        style = tkinter.ttk.Style()

        style.configure(
            "Card.TFrame",
            background="white",
            relief="solid",
            borderwidth=1,
        )

        style.configure(
            "CardHover.TFrame",
            background="#f2f8ff",
            relief="solid",
            borderwidth=1,
        )
