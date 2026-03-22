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

    def set_content(self, content):
        self.delete(0, tk.END)
        self.insert(0, content)

    def get_content(self):
        return self.get()

    def get_row(self):
        if len(self.id) <= 2:
            return self.id[-1]
        else:
            return self.id[1:]

    def get_column(self):
        return self.id[0]

    def highlight(self):
        self.configure(background='#add8e6')

    def clear_highlight(self):
        self.configure(background=self.formatting["bg"])

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
        self.column_labels = list('ABCDEFGHIJKLMNOP')
        self.row_count = 60
        self.cell_dict = {}
        self.iterator_pos = 0
        self.cell_count = 0
        self.default_cell_foreground = "#000000"
        self.default_cell_background = "#FFFFFF"
        self.root_entry = None
        self.entered_cells = []
        self.clipboard = []
        self.cell_keys = []

        for i, label in enumerate(self.column_labels):
            column_label = ttk.Label(self, text=label)
            column_label.grid(row=0, column=i + 1)
            for j in range(self.row_count):
                row_num = f"{j + 1}"
                row_label = ttk.Label(self, text=row_num)
                row_label.grid(row=row_num, column=0, padx=1)
                cell_id = f"{label}{row_num}"
                cell = Cell(self, cell_id, master=self, relief=tk.FLAT, borderwidth=5, border=2, highlightthickness=1)
                self.cell_dict.update({cell_id: cell})
                cell.grid(row=row_num, column=i + 1)
                self.cell_count += 1
                self.cell_keys.append(cell_id)

    def copy_to_clipboard(self):
        self.clipboard.clear()
        self.entered_cells.sort(key=lambda x: x.id[1:])
        for cell in self.entered_cells:
            cell.clear_highlight()
            self.clipboard.append({
                "id": cell.id,
                "content": cell.get_content(),
                "equ": cell.get_equ()
            })

    def revise_equation(self, equ, equ_src_cell_id, dest_root_row, dest_root_column):
        _, _, cell_strs = self.parent.parse_equation(equ)
        src_column = equ_src_cell_id[0]
        dest_root_row = int(dest_root_row)
        smallest_cell_row = min([int(cell_str[1:]) for cell_str in cell_strs if cell_str[0] == src_column])
        relative_dist = int(dest_root_row) - smallest_cell_row
        for cell_str in cell_strs:
            if cell_str[0] == src_column:
                src_row = int(cell_str[1:])
                if relative_dist != 0:
                    row = src_row + relative_dist
                else:
                    row = src_row
                new_id = f"{dest_root_column}{row}"
                equ = equ.replace(cell_str, new_id)
        return equ

    def reset_multi_cell_select(self):
        self.root_entry = None
        for cell in self.entered_cells:
            cell.clear_highlight()
        self.entered_cells.clear()

    def select_cells(self, *args):
        x, y = self.winfo_pointerxy()
        entry = self.winfo_containing(x, y)
        if not isinstance(entry, Cell):
            return
        if self.root_entry is None:
            self.root_entry = entry
            return
        elif entry is self.root_entry and len(self.entered_cells) == 0:
            return

        if self.root_entry not in self.entered_cells:
            self.root_entry.highlight()
            self.entered_cells.append(self.root_entry)
        if entry.get_column() != self.root_entry.get_column():
            return
        if entry not in self.entered_cells:
            entry.focus_set()
            entry.highlight()
            self.entered_cells.append(entry)
        if entry != self.entered_cells[-1]:  # for deselecting cells when the cursor moves out of a cell
            entry.focus_set()
            self.entered_cells[-1].clear_highlight()
            self.entered_cells.pop()

    def multi_copy(self, *args):
        self.copy_to_clipboard()
        self.entered_cells.clear()
        return 'break' # override default copy behavior

    def multi_cut(self, *args):
        self.copy_to_clipboard()
        for cell in self.entered_cells:
            cell.set_content("")
            cell.set_equ("")
        self.entered_cells.clear()
        return 'break'  # override default cut behavior

    def multi_paste(self, *args):
        root_dest_cell = self.focus_get()
        if not isinstance(root_dest_cell, Cell):
            return 'break'
        dest_cell_index = self.get_cell_index(root_dest_cell.id)
        cells_with_new_equ = []
        for cell in self.clipboard:
            try:
                dest_cell = self.cell_dict[self.cell_keys[dest_cell_index]]
            except KeyError:
                break
            if cell["equ"] == "":
                dest_cell.set_content(cell["content"])
            else:
                new_equ = self.revise_equation(cell["equ"], cell["id"], root_dest_cell.get_row(), root_dest_cell.get_column())
                dest_cell.set_equ(new_equ)
                cells_with_new_equ.append(dest_cell)
            dest_cell_index += 1

        for cell in cells_with_new_equ:
            cell.set_content(self.parent.compute_equation(cell.get_equ()))
        return 'break' # override default paste behavior

    def multi_delete(self, *args):
        for cell in self.entered_cells:
            cell.set_content("")
            cell.set_equ("")
            cell.clear_highlight()

    def get_cell_by_index(self, index):
        return self.cell_dict[self.cell_keys[index]]

    def get_cell_index(self, cell_id):
        return self.cell_keys.index(cell_id)

    def get_all_cells_attributes(self):
        out = {}
        for cell_id in self.cell_dict.keys():
            out.update(
                {cell_id:
                     {"content": self.get_cell_content(cell_id),
                      "formatting": self.get_cell_formating(cell_id),
                      "equation": self.get_cell_equ(cell_id)
                      }}
            )
        return out

    def clear_all_cells_attributes(self):
        for cell_id in self.cell_dict.keys():
            self.set_cell_equ(cell_id, "")
            self.set_cell_content(cell_id, "")
            self.reset_cell_formatting(cell_id)

    def set_all_cells_attributes(self, attr_dict):
        for cell_id in attr_dict.keys():
            self.set_cell_equ(cell_id, attr_dict[cell_id]["equation"])
            self.set_cell_formatting(cell_id, attr_dict[cell_id]["formatting"])
            self.set_cell_content(cell_id, attr_dict[cell_id]["content"])

    def set_cell_foreground(self, cell_id, color):
        cell = self.cell_dict[cell_id]
        cell.configure(background=self.default_cell_foreground)

    def set_cell_background(self, cell_id, color):
        cell = self.cell_dict[cell_id]
        cell.configure(background=self.default_cell_background)

    def set_cell_content(self, cell_id, content):
        cell = self.cell_dict[cell_id]
        cell.delete(0, tk.END)
        cell.insert(0, content)

    def set_cell_equ(self, cell_id, equ):
        cell = self.cell_dict[cell_id]
        cell.set_equ(equ)

    def set_cell_formatting(self, cell_id, formatting_dict):
        cell = self.cell_dict[cell_id]
        cell.set_formatting(formatting_dict)

    def reset_cell_formatting(self, cell_id):
        cell = self.cell_dict[cell_id]
        cell.reset_formatting()

    def get_cell_equ(self, cell_id):
        return self.cell_dict[cell_id].get_equ()

    def get_cell_content(self, cell_id):
        return self.cell_dict[cell_id].get()

    def get_cell_formating(self, cell_id):
        return self.cell_dict[cell_id].get_formatting()

    def nav_left(self, *args):
        if not isinstance(self.parent.focus_get(), Cell):
            return 'break'
        cell_index = self.get_cell_index(self.parent.current_cell.id)
        new_index = cell_index - 60
        if new_index < 0:
            return 'break'
        try:
            cell = self.get_cell_by_index(new_index)
        except KeyError:
            return 'break'
        cell.focus_set()
        self.parent.update_cells(None)
        return 'break'

    def nav_right(self, *args):
        if not isinstance(self.parent.focus_get(), Cell):
            return 'break'
        cell_index = self.get_cell_index(self.parent.current_cell.id)
        new_index = cell_index + 60
        if new_index >= self.cell_count:
            return 'break'
        try:
            cell = self.get_cell_by_index(new_index)
        except KeyError:
            return 'break'
        cell.focus_set()
        self.parent.update_cells(None)
        return 'break'

    def nav_up(self, *args):
        if not isinstance(self.parent.focus_get(), Cell):
            return 'break'
        cell_index = self.get_cell_index(self.parent.current_cell.id)
        new_index = cell_index - 1
        if new_index < 0:
            return 'break'
        try:
            cell = self.get_cell_by_index(new_index)
        except KeyError:
            return 'break'
        cell.focus_set()
        self.parent.update_cells(None)
        return 'break'

    def nav_down(self, *args):
        if not isinstance(self.parent.focus_get(), Cell):
            return 'break'
        cell_index = self.get_cell_index(self.parent.current_cell.id)
        new_index = cell_index + 1
        if new_index > self.cell_count:
            return 'break'
        try:
            cell = self.get_cell_by_index(new_index)
        except KeyError:
            return 'break'
        cell.focus_set()
        self.parent.update_cells(None)
        return 'break'

