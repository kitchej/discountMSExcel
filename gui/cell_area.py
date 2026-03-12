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
                "font": tkfont.Font(family="Helvetica", size=12),
                "bg": "#000000",
                "fg": "#FFFFFF"
            }
        self.set_bg(self.formatting["bg"])
        self.set_bg(self.formatting["fg"])
        self.configure(font=self.formatting["font"])


    def get_equ(self):
        return self.equ

    def set_equ(self, equ):
        self.equ = equ

    def set_formatting(self, font_dict):
        font_obj = tkfont.Font()
        font_obj.configure(
            family=font_dict["family"],
            size=font_dict["size"],
            slant=font_dict["slant"],
            weight=font_dict["weight"],
            underline=font_dict["underline"],
            overstrike=font_dict["strikethrough"]
        )
        self.formatting["font"] = font_obj
        self.configure(font=self.formatting["font"])


    def get_formatting(self):
        font_obj = self.formatting["font"]
        font_dict = {
            "family": font_obj.cget("family"),
            "size": font_obj.cget("size"),
            "slant": font_obj.cget("slant"),
            "weight": font_obj.cget("weight"),
            "underline": font_obj.cget("underline"),
            "strikethrough": font_obj.cget("overstrike")
        }

        return font_dict

    def reset_formatting(self):
        self.formatting = {
            "font": tkfont.Font(family="Helvetica", size=12),
            "bg": "#000000",
            "fg": "#FFFFFF"
        }
        self.configure(font=self.formatting["font"])

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
        if font.cget('overstrike') == 1:
            font.configure(overstrike=0)
        else:
            font.configure(overstrike=1)
        self.configure(font=font)
        self.formatting.update({"font": font})


class CellArea(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.parent = parent
        self.labels_columns = 'ABCDEFGHIJKLMNOP'
        self.row_count = 60
        self.cells_dict = {}
        self.iterator_pos = 0
        self.cell_count = 0
        self.default_cell_foreground = "#ffffff"
        self.default_cell_background = "#000000"

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
            self.reset_cell_formatting(cell_id)
            self.set_cell_content(cell_id, "")
            self.set_cell_background(cell_id, self.default_cell_background)
            self.set_cell_foreground(cell_id, self.default_cell_foreground)

    def set_all_cells_attributes(self, attr_dict):
        for cell_id in attr_dict.keys():
            self.set_cell_equ(cell_id, attr_dict[cell_id]["equation"])
            self.set_cell_formatting(cell_id, attr_dict[cell_id]["formatting"])
            self.set_cell_content(cell_id, attr_dict[cell_id]["content"])
            self.set_cell_background(cell_id, attr_dict[cell_id]["background"])
            self.set_cell_background(cell_id, attr_dict[cell_id]["foreground"])

    def reset_cell_formatting(self, cell_id):
        cell = self.cells_dict[cell_id]
        cell.reset_formatting()

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

    def get_cell_equ(self, cell_id):
        return self.cells_dict[cell_id].get_equ()

    def get_cell_content(self, cell_id):
        return self.cells_dict[cell_id].get()

    def get_cell_formating(self, cell_id):
        return self.cells_dict[cell_id].get_formatting()

