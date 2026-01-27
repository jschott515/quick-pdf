import tkinter
import tkinter.ttk
from tkinter import filedialog

from ._core import QpdfTool


class PdfAppend(QpdfTool):
    BRIEF = "Combine multiple PDF files into one!"

    def __init__(self, parent: tkinter.ttk.Notebook) -> None:
        super().__init__(parent)

        self._label = tkinter.ttk.Label(self, text="Select files to append:", font=("Arial", 10, "bold"))
        self._label.pack(anchor="w", padx=10, pady=5)

        # Show only the tree (#0) column; store the path in the 'values' list
        self._tree = tkinter.ttk.Treeview(self, columns=("path",), show="tree")
        self._tree.pack(anchor="n", padx=10, pady=5, expand=True, fill="both")

        # Hide the technical 'path' column from view
        self._tree.column("path", width=0, stretch=False)

        self._tooltip_win = None
        self._tree.bind("<Motion>", self._on_hover)
        self._tree.bind("<Leave>", lambda e: self._hide_tooltip())

        btn_frame = tkinter.ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        tkinter.ttk.Button(btn_frame, text="Add Files", command=self._add_files).pack(side="left", padx=2)
        tkinter.ttk.Button(btn_frame, text="Delete", command=self._delete_selected).pack(side="left", padx=2)
        tkinter.ttk.Button(btn_frame, text="Move Up", command=lambda: self._move_item(-1)).pack(side="left", padx=2)
        tkinter.ttk.Button(btn_frame, text="Move Down", command=lambda: self._move_item(1)).pack(side="left", padx=2)

    def _on_hover(self, event: tkinter.Event[tkinter.ttk.Treeview]) -> None:
        item_id = self._tree.identify_row(event.y)
        if item_id:
            path = self._tree.item(item_id, "values")[0]
            self._show_tooltip(event.x_root + 15, event.y_root + 10, path)
        else:
            self._hide_tooltip()

    def _show_tooltip(self, x: int, y: int, text: str) -> None:
        if self._tooltip_win:
            self._tooltip_label.config(text=text)
            self._tooltip_win.geometry(f"+{x}+{y}")
            return

        self._tooltip_win = tkinter.Toplevel(self)
        self._tooltip_win.wm_overrideredirect(True)
        self._tooltip_win.geometry(f"+{x}+{y}")
        self._tooltip_label = tkinter.ttk.Label(
            self._tooltip_win, text=text, relief="solid", borderwidth=1, background="#ffffca"
        )
        self._tooltip_label.pack()

    def _hide_tooltip(self) -> None:
        if self._tooltip_win:
            self._tooltip_win.destroy()
            self._tooltip_win = None

    def _add_files(self) -> None:
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for f in files:
            name = f.split("/")[-1]
            self._tree.insert("", "end", text=name, values=(f,))

    def _delete_selected(self) -> None:
        for item in self._tree.selection():
            self._tree.delete(item)

    def _move_item(self, direction) -> None:
        leaves = self._tree.selection()
        if not leaves:
            return
        for i in (leaves if direction == -1 else reversed(leaves)):
            idx = self._tree.index(i)
            self._tree.move(i, self._tree.parent(i), idx + direction)
