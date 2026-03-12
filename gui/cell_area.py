import tkinter.ttk as ttk
import tkinter as tk
from tkinter import font as tkfont


class Cell(tk.Entry):
    def __init__(self, parent, cell_id, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        self.parent = parent
        self.id = cell_id
        self.equ = ""
        self.formatting = {
            "font": {
                "family": "Helvetica",
                "size": 12,
                "slant": "roman",
                "weight": "normal",
                "underline": 0,
                "strikethrough": 0
            },
            "bg": "#FFFFFF",
            "fg": "#000000"
        }
        self.font = tkfont.Font(family=self.formatting["font"]["family"], size=self.formatting["font"]["size"])
        self.configure(font=self.font)


    def get_equ(self):
        return self.equ

    def set_equ(self, equ):
        self.equ = equ

    def set_formatting(self, formatting_dict):
        self.font.configure(
            family=formatting_dict["font"]["family"],
            size=formatting_dict["font"]["size"],
            slant=formatting_dict["font"]["slant"],
            weight=formatting_dict["font"]["weight"],
            underline=formatting_dict["font"]["underline"],
            overstrike=formatting_dict["font"]["strikethrough"]
        )
        self.configure(font=self.font)
        self.set_bg(formatting_dict["bg"])
        self.set_fg(formatting_dict["fg"])


    def get_formatting(self):
        return self.formatting

    def reset_formatting(self):
        self.formatting = {
            "font": {
                "family": "Helvetica",
                "size": 12,
                "slant": "roman",
                "weight": "normal",
                "underline": 0,
                "strikethrough": 0
            },
            "bg": "#FFFFFF",
            "fg": "#000000"
        }
        self.font = tkfont.Font(family=self.formatting["font"]["family"], size=self.formatting["font"]["size"])
        self.configure(font=self.font)
        self.set_bg(self.formatting["bg"])
        self.set_fg(self.formatting["fg"])

    def set_bg(self, color: str):
        self.configure(background=color)
        self.formatting["bg"] = color

    def set_fg(self, color):
        self.configure(foreground=color)
        self.formatting["fg"] = color

    def get_fg(self):
        return self.formatting["fg"]

    def get_bg(self):
        return self.formatting["bg"]

    def toggle_bold(self):
        if self.font.cget('weight') == 'normal':
            self.font.configure(weight='bold')
            self.formatting["font"]["weight"] = 'bold'
        else:
            self.font.configure(weight='normal')
            self.formatting["font"]["weight"] = 'normal'
        self.configure(font=self.font)


    def toggle_italics(self):
        if self.font.cget('slant') == 'italic':
            self.font.configure(slant='roman')
            self.formatting["font"]["slant"] = 'roman'
        else:
            self.font.configure(slant='italic')
            self.formatting["font"]["slant"] = 'italic'
        self.configure(font=self.font)


    def toggle_underline(self):
        if self.font.cget('underline') == 0:
            self.font.configure(underline=1)
            self.formatting["font"]["underline"] = 1
        else:
            self.font.configure(underline=0)
            self.formatting["font"]["underline"] = 0
        self.configure(font=self.font)


    def toggle_strikethrough(self):
        if self.font.cget('overstrike') == 0:
            self.font.configure(overstrike=1)
            self.formatting["font"]["strikethrough"] = 1
        else:
            self.font.configure(overstrike=0)
            self.formatting["font"]["strikethrough"] = 0
        self.configure(font=self.font)


class CellArea(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.parent = parent
        self.labels_columns = 'ABCDEFGHIJKLMNOP'
        self.row_count = 60
        self.cells_dict = {}
        self.iterator_pos = 0
        self.cell_count = 0
        self.default_cell_foreground = "#000000"
        self.default_cell_background = "#FFFFFF"

        for i, label in enumerate(self.labels_columns):
            column_label = ttk.Label(self, text=label)
            column_label.grid(row=0, column=i + 1)
            for j in range(self.row_count):
                row_num = f"{j + 1}"
                row_label = ttk.Label(self, text=row_num)
                row_label.grid(row=row_num, column=0, padx=1)
                cell = Cell(self, f"{label}{row_num}", master=self, relief=tk.FLAT, borderwidth=5, border=2, highlightthickness=1)
                self.cells_dict.update({f"{label}{row_num}": cell})
                cell.grid(row=row_num, column=i + 1)
                self.cell_count += 1

    def get_all_cells_attributes(self):
        out = {}
        for cell_id in self.cells_dict.keys():
            out.update(
                {cell_id:
                     {"content": self.get_cell_content(cell_id),
                      "formatting": self.get_cell_formating(cell_id),
                      "equation": self.get_cell_equ(cell_id)
                      }}
            )
        return out

    def clear_all_cells_attributes(self):
        for cell_id in self.cells_dict.keys():
            self.set_cell_equ(cell_id, "")
            self.set_cell_content(cell_id, "")
            self.reset_cell_formatting(cell_id)

    def set_all_cells_attributes(self, attr_dict):
        for cell_id in attr_dict.keys():
            self.set_cell_equ(cell_id, attr_dict[cell_id]["equation"])
            self.set_cell_formatting(cell_id, attr_dict[cell_id]["formatting"])
            self.set_cell_content(cell_id, attr_dict[cell_id]["content"])

    def set_cell_foreground(self, cell_id, color):
        cell = self.cells_dict[cell_id]
        cell.configure(background=self.default_cell_foreground)

    def set_cell_background(self, cell_id, color):
        cell = self.cells_dict[cell_id]
        cell.configure(background=self.default_cell_background)

    def set_cell_content(self, cell_id, content):
        cell = self.cells_dict[cell_id]
        cell.delete(0, tk.END)
        cell.insert(0, content)

    def set_cell_equ(self, cell_id, equ):
        cell = self.cells_dict[cell_id]
        cell.set_equ(equ)

    def set_cell_formatting(self, cell_id, formatting_dict):
        cell = self.cells_dict[cell_id]
        cell.set_formatting(formatting_dict)

    def reset_cell_formatting(self, cell_id):
        cell = self.cells_dict[cell_id]
        cell.reset_formatting()

    def get_cell_equ(self, cell_id):
        return self.cells_dict[cell_id].get_equ()

    def get_cell_content(self, cell_id):
        return self.cells_dict[cell_id].get()

    def get_cell_formating(self, cell_id):
        return self.cells_dict[cell_id].get_formatting()

