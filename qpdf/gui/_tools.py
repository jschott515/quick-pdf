import tkinter
import tkinter.ttk
import typing

import PIL.Image
import PIL.ImageTk
import pymupdf

from ._pdf_tools import PdfAppend, QpdfTool
from .core import QpdfToolsMetadata, QpdfToolType


class QpdfTools(tkinter.ttk.Frame):
    def __init__(self, parent: tkinter.ttk.Frame, home_action: typing.Callable[[], None]) -> None:
        super().__init__(parent)
        self._zoom_level = 1.0
        self._img_refs: typing.List[PIL.ImageTk.PhotoImage] = []

        self._sidebar = tkinter.ttk.Frame(self)
        self._sidebar.pack(side="right", fill="y", padx=5, pady=5)
        tkinter.ttk.Button(self._sidebar, text="Home", command=home_action).pack(fill="x", pady=2)

        self._zoom_frame = tkinter.ttk.LabelFrame(self._sidebar, text="Zoom")
        tkinter.ttk.Button(self._zoom_frame, text="+", width=3, command=lambda: self._change_zoom(0.1)).pack(
            side="left", padx=2
        )
        tkinter.ttk.Button(self._zoom_frame, text="-", width=3, command=lambda: self._change_zoom(-0.1)).pack(
            side="left", padx=2
        )

        self._view_select = tkinter.ttk.Button(self._sidebar)
        self._view_select.pack(side="bottom", fill="x", pady=2)
        self._preview_enable = False

        container = tkinter.ttk.Frame(self)
        container.pack(side="left", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._notebook = tkinter.ttk.Notebook(container)
        self._tools: typing.MutableMapping[QpdfToolType, QpdfTool] = {
            QpdfToolType.PDF_APPEND: PdfAppend(self._notebook)
        }
        for tool, tab in self._tools.items():
            self._notebook.add(tab, text=tool.value)
        self._active_tool = QpdfToolType.PDF_APPEND

        self._preview = tkinter.ttk.Frame(container)
        self._canvas = tkinter.Canvas(self._preview, background="gray", highlightthickness=0)
        self._scrollbar = tkinter.ttk.Scrollbar(self._preview, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._canvas.bind("<Configure>", lambda e: self.render_pdf())
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self._canvas.bind_all("<Button-4>", self._on_mousewheel)
        self._canvas.bind_all("<Button-5>", self._on_mousewheel)

        self._notebook.grid(row=0, column=0, sticky="nsew")
        self._preview.grid(row=0, column=0, sticky="nsew")
        self.hide_preview()

    def _change_zoom(self, delta: float) -> None:
        # 1.0 is "Fit to Width". Do not allow zoom > 1.0 to ensure horizontal fit.
        new_zoom = self._zoom_level + delta
        self._zoom_level = max(0.1, min(1.0, new_zoom))
        self.render_pdf()

    def _on_mousewheel(self, event: tkinter.Event[tkinter.Misc]) -> None:
        if not self._preview_enable:
            return

        if event.num == 4:
            delta = 1.0
        elif event.num == 5:
            delta = -1.0
        else:
            delta = event.delta / 120
        if isinstance(event.state, int):
            if event.state & 0x0004:  # Ctrl held
                self._change_zoom(0.1 if delta > 0 else -0.1)
            else:
                self._canvas.yview_scroll(int(-1 * delta), "units")

    def render_pdf(self) -> None:
        self._canvas.delete("all")
        self._img_refs.clear()

        if not self._preview_enable:
            return

        tool = self._tools[self._active_tool]
        doc = tool.get_pdf()
        if not doc or len(doc) == 0:
            return

        padding = 20
        canvas_width = self._canvas.winfo_width() - padding
        if canvas_width < 50:
            return

        current_y = 10
        for i in range(doc.page_count):
            page = doc[i]
            fit_scale = canvas_width / page.rect.width
            total_scale = fit_scale * self._zoom_level

            pix = page.get_pixmap(matrix=pymupdf.Matrix(total_scale, total_scale))
            img = PIL.Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            photo = PIL.ImageTk.PhotoImage(img)

            x_pos = (self._canvas.winfo_width() - pix.width) // 2
            self._canvas.create_image(x_pos, current_y, anchor="nw", image=photo)
            self._img_refs.append(photo)
            current_y += pix.height + 10

        self._canvas.configure(scrollregion=(0, 0, canvas_width, current_y))

    def select_tab(self, tool: QpdfToolType) -> None:
        self._active_tool = tool
        self._notebook.select(self._tools.get(tool, None))
        self.hide_preview()
        self.tkraise()

    def get_metadata(self) -> typing.Sequence[QpdfToolsMetadata]:
        return [
            QpdfToolsMetadata(name, tool.BRIEF, lambda: self.select_tab(name)) for name, tool in self._tools.items()
        ]

    def show_preview(self) -> None:
        self._preview_enable = True
        self._view_select.configure(text="Hide Preview", command=self.hide_preview)
        self._zoom_frame.pack(fill="x", pady=10, before=self._view_select)
        self._preview.tkraise()

    def hide_preview(self) -> None:
        self._preview_enable = False
        self._view_select.configure(text="Show Preview", command=self.show_preview)
        self._zoom_frame.pack_forget()
        self._notebook.tkraise()
