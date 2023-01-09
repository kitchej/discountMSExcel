import tkinter.ttk as ttk
import tkinter as tk
import os


def get_attr(cell):
    keys = cell.keys()
    print("\n\n")
    for key in keys:
        print("Attribute: {:<20}".format(key), end=' ')
        value = cell[key]
        vtype = type(value)
        print('Type: {:<30} Value: {}'.format(str(vtype), value))


class CellInfo:
    def __init__(self, cell):
        self.cell_obj = cell
        self.font = cell.cget('font')
        self.background = cell.cget('background')
        self.foreground = cell.cget('foreground')
        self.equ = ''


class CellArea(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.parent = parent
        self.labels_columns = 'ABCDEFGHIJK'
        self.cells_dict = {}
        self.cells = []

        self.scroll_y = ttk.Scrollbar(self)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y, expand=0)

        self.scroll_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X, expand=0)

        self.canvas = tk.Canvas(self, yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set,highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH)
        self.scroll_y.configure(command=self.canvas.yview)
        self.scroll_x.configure(command=self.canvas.xview)

        self.cell_window = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.cell_window, anchor='w')
        self.bind("<Configure>", self.canvasResize)

        for i, label in enumerate(self.labels_columns):
            column_label = ttk.Label(self.cell_window, text=label)
            column_label.grid(row=0, column=i + 1)
            for j in range(40):
                row_label = ttk.Label(self.cell_window, text=f"{j + 1}")
                row_label.grid(row=j + 1, column=0, padx=1)
                cell = tk.Entry(self.cell_window, font=('Arial 11'))
                cell_info = CellInfo(cell)
                self.cells.append(cell_info)
                self.cells_dict.update({f"{label}{j + 1}": cell_info})
                cell.grid(row=j + 1, column=i + 1)

    def canvasResize(self, *args):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=1000, height=900)


