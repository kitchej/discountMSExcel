import tkinter.ttk as ttk
import tkinter as tk
from tkinter import font as tkfont

COLUMN_COUNT = 60


class Cell(tk.Entry):
    def __init__(self, parent, formatting, cell_id, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        self.parent = parent
        self.id = cell_id
        self.equ = ""
        if formatting is None:
            self.formatting = {
                "font": tkfont.Font(family="Helvetica", size=12),
                "bg": "#000000",
                "fg": "#FFFFFF"
            }
        else:
            self.formatting = formatting
    def get_equ(self):
        return self.equ

    def set_equ(self, equ):
        self.equ = equ

    def get_formatting(self):
        return self.formatting

    def set_bg(self, color: str):
        self.configure(background=color)
        self.formatting["bg"] = color

    def set_fg(self, color):
        self.configure(foreground=color)
        self.formatting["fg"] = color

    def toggle_bold(self):
        font = self.formatting["font"]
        if font.cget('weight') == 'normal':
            font.configure(weight='bold')
        else:
            font.configure(weight='normal')
        self.configure(font=font)
        self.formatting.update({"font": font})

    def toggle_italics(self):
        font = self.formatting["font"]
        if font.cget('slant') == 'italic':
            font.configure(slant='roman')
        else:
            font.configure(slant='italic')
        self.configure(font=font)
        self.formatting.update({"font": font})

    def toggle_underline(self):
        font = self.formatting["font"]
        if font.cget('underline') == 1:
            font.configure(underline=0)
        else:
            font.configure(underline=1)
        self.configure(font=font)
        self.formatting.update({"font": font})

    def toggle_strikethrough(self):
        font = self.formatting["font"]
        if font.cget('strikethrough') == 1:
            font.configure(strikethrough=0)
        else:
            font.configure(strikethrough=1)
        self.configure(font=font)
        self.formatting.update({"font": font})


class CellArea(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.parent = parent
        self.labels_columns = 'ABCDEFGHIJKLMNOP'
        self.cells_dict = {}

        for i, label in enumerate(self.labels_columns):
            column_label = ttk.Label(self, text=label)
            column_label.grid(row=0, column=i + 1)
            for j in range(COLUMN_COUNT):
                row_num = f"{j + 1}"
                row_label = ttk.Label(self, text=row_num)
                row_label.grid(row=row_num, column=0, padx=1)
                cell = Cell(self, "", f"{label}{row_num}", master=self, relief=tk.FLAT, borderwidth=5, border=2, highlightthickness=1)
                self.cells_dict.update({f"{label}{row_num}": cell})
                cell.grid(row=row_num, column=i + 1)

    def set_cell_content(self, cell_id, content):
        cell = self.cells_dict[cell_id]
        cell.delete(0, tk.END)
        cell.insert(0, content)

    def set_cell_equ(self, cell_id, equ):
        cell = self.cells_dict[cell_id]
        cell.set_equ(equ)

    def get_cell_content(self, cell_id):
        return self.cells_dict[cell_id].get()

    def get_cell_formating(self, cell_id):
        return self.cells_dict[cell_id].get_formatting()

