import tkinter.ttk as ttk
import tkinter as tk
import os

class Cell(ttk.Entry):
    def __init__(self, formatting, parent):
        ttk.Entry.__init__(self)
        self.parent = parent
        self.formatting = formatting
        parse_formatting()

    def parse_formatting(self):
        for setting in self.formatting:
            self.configure(setting)


class CellArea(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.parent = parent
        self.labels_columns = 'ABCDEFGHIJK'
        self.cells_dict = {}
        self.cells = []

        for i, label in enumerate(self.labels_columns):
            column_label = ttk.Label(self, text=label)
            column_label.grid(row=0, column=i + 1)
            for j in range(40):
                row_label = ttk.Label(self, text=f"{j + 1}")
                row_label.grid(row=j + 1, column=0, padx=1)
                cell = ttk.Entry(self, style="default.TEntry")
                self.cells.append([cell,
                                   [
                                       cell.get(),
                                       cell.cget("font"),
                                       cell.cget("background"),
                                       cell.cget("foreground"),
                                       '']
                                   ])
                self.cells_dict.update({f"{label}{j + 1}": cell})
                cell.grid(row=j + 1, column=i + 1)
