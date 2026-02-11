import tkinter.ttk as ttk
import tkinter as tk

COLUMN_COUNT = 40


class Cell(tk.Entry):
    def __init__(self, parent, formatting, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        self.parent = parent
        self.formatting = formatting
        # self.parse_formatting()

    def parse_formatting(self):
        for setting in self.formatting:
            self.configure(setting)

    def get_formatting(self):
        return self.formatting


class CellArea(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.parent = parent
        self.labels_columns = 'ABCDEFGHIJK'
        self.cells_dict = {}

        for i, label in enumerate(self.labels_columns):
            column_label = ttk.Label(self, text=label)
            column_label.grid(row=0, column=i + 1)
            for j in range(COLUMN_COUNT):
                row_label = ttk.Label(self, text=f"{j + 1}")
                row_label.grid(row=j + 1, column=0, padx=1)
                cell = Cell(self, "", master=self, relief=tk.FLAT, borderwidth=5, border=2, highlightthickness=1)
                self.cells_dict.update({f"{label}{j + 1}": cell})
                cell.grid(row=j + 1, column=i + 1)

    def get_cell_content(self, cell: str):
        return self.cells_dict[cell].get()

    def get_cell_formating(self, cell: str):
        return self.cells_dict[cell].get_formatting()

