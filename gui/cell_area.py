import decimal
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import font as tkfont

DEFAULT_FONT_FAMILY = "Helvetica"
DEFAULT_FONT_SIZE = 12


class Cell(tk.Entry):
    def __init__(self, main_win, cell_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_win = main_win
        self.id = cell_id
        self.equ = ""
        self.num_format = "Plain Text"
        self.current_background = "#FFFFFF"
        self.font = tkfont.Font(family=DEFAULT_FONT_FAMILY, size=DEFAULT_FONT_SIZE)
        self.configure(font=self.font)
        self.is_highlighted = False
        self.decimal_value = None
        self.bind("<KeyRelease>", self._parse_decimal_value)

    def _parse_decimal_value(self, *args):
        self.main_win.is_edited = True
        try:
            self.decimal_value = decimal.Decimal(self.get())
        except decimal.InvalidOperation:
            self.decimal_value = None

    def configure(self, cnf = None, **kwargs):
        try:
            background_color = kwargs["background"]
            if not self.is_highlighted:
                self.current_background = background_color
        except KeyError:
            pass
        super().configure(cnf, **kwargs)

    def insert(self, index, string):
        super().insert(index, string)
        self._parse_decimal_value()
        self.main_win.set_is_edited()

    def refresh_cell(self):
        if self.num_format == "Plain Text":
            self.to_plain_text()
        elif self.num_format == "Scientific":
            self.to_scientific()
        elif self.num_format == "Financial":
            self.to_financial()

    def get_decimal_value(self):
        return self.decimal_value

    def set_decimal_value(self, value):
        self.decimal_value = value

    def to_plain_text(self):
        self.num_format = "Plain Text"
        if self.decimal_value is not None:
            self.delete(0, tk.END)
            super().insert(0, self.decimal_value)
            self.main_win.set_is_edited()

    def to_scientific(self):
        self.num_format = "Scientific"
        if self.decimal_value is not None:
            self.delete(0, tk.END)
            super().insert(0, f"{self.decimal_value:e}")
            self.main_win.set_is_edited()

    def to_financial(self):
        self.num_format = "Financial"
        if self.decimal_value is not None:
            self.delete(0, tk.END)
            super().insert(0, f"${self.decimal_value:.2f}")
            self.main_win.set_is_edited()

    def set(self, content):
        self.delete(0, tk.END)
        self.insert(0, content)

    def get_row(self):
        return self.id[1:]

    def get_column(self):
        return self.id[0]

    def highlight(self):
        self.is_highlighted = True
        self.configure(background='#add8e6')

    def clear_highlight(self):
        self.is_highlighted = False
        self.configure(background=self.current_background)

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
        self.configure(background=formatting_dict["bg"])
        self.configure(foreground=formatting_dict["fg"])
        if formatting_dict["num_format"] == "Plain Text":
            self.to_plain_text()
        elif formatting_dict["num_format"] == "Financial":
            self.to_financial()
        elif formatting_dict["num_format"] == "Scientific":
            self.to_scientific()

    def get_formatting(self):
        return {
            "font": {
                "family": self.font.cget("family"),
                "size": self.font.cget("size"),
                "slant":  self.font.cget("slant"),
                "weight": self.font.cget("weight"),
                "underline": self.font.cget("underline"),
                "strikethrough": self.font.cget("overstrike")
            },
            "bg": self.current_background,
            "fg": self.cget("foreground"),
            "num_format": self.num_format  # "Plain Text", "Scientific", "Financial"
        }

    def reset_formatting(self):
        self.font = tkfont.Font(family=DEFAULT_FONT_FAMILY, size=DEFAULT_FONT_SIZE)
        self.configure(background="#FFFFFF")
        self.configure(foreground="#000000")
        
    def toggle_bold(self):
        if self.font.cget('weight') == 'normal':
            self.font.configure(weight='bold')
        else:
            self.font.configure(weight='normal')

    def toggle_italics(self):
        if self.font.cget('slant') == 'italic':
            self.font.configure(slant='roman')
        else:
            self.font.configure(slant='italic')

    def toggle_underline(self):
        if self.font.cget('underline') == 0:
            self.font.configure(underline=1)
        else:
            self.font.configure(underline=0)

    def toggle_strikethrough(self):
        if self.font.cget('overstrike') == 0:
            self.font.configure(overstrike=1)
        else:
            self.font.configure(overstrike=0)


class CellArea(ttk.Frame):
    def __init__(self, main_win, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_win = main_win
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
                cell = Cell(self.main_win, cell_id, master=self, relief=tk.FLAT, borderwidth=5, border=2, highlightthickness=1)
                self.cell_dict.update({cell_id: cell})
                cell.grid(row=row_num, column=i + 1)
                self.cell_count += 1
                self.cell_keys.append(cell_id)

    def copy_to_clipboard(self):
        self.clipboard.clear()
        self.entered_cells.sort(key=lambda x: x.get_row())
        for cell in self.entered_cells:
            cell.clear_highlight()
            self.clipboard.append({
                "id": cell.id,
                "content": cell.get(),
                "equ": cell.get_equ()
            })

    def revise_equation(self, equ, equ_src_cell_id, dest_root_row, dest_root_column):
        _, _, cell_strs = self.main_win.parse_equation(equ)
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
            cell.set("")
            cell.set_equ("")
        self.entered_cells.clear()
        return 'break'  # override default cut behavior

    def multi_paste(self, *args):
        root_dest_cell = self.focus_get()
        if not isinstance(root_dest_cell, Cell):
            return 'break'
        dest_cell_index = self.index_of(root_dest_cell.id)
        cells_with_new_equ = []
        for cell in self.clipboard:
            try:
                dest_cell = self.cell_dict[self.cell_keys[dest_cell_index]]
            except KeyError:
                break
            if cell["equ"] == "":
                dest_cell.set(cell["content"])
            else:
                new_equ = self.revise_equation(cell["equ"], cell["id"], root_dest_cell.get_row(), root_dest_cell.get_column())
                dest_cell.set_equ(new_equ)
                cells_with_new_equ.append(dest_cell)
            dest_cell_index += 1

        for cell in cells_with_new_equ:
            cell.set(self.main_win.compute_equation(cell.get_equ()))
        return 'break' # override default paste behavior

    def multi_delete(self, *args):
        for cell in self.entered_cells:
            cell.set("")
            cell.set_equ("")
            cell.clear_highlight()

    def get_cell_by_index(self, index):
        return self.cell_dict[self.cell_keys[index]]

    def index_of(self, cell_id):
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
            self.set_cell_content(cell_id, attr_dict[cell_id]["content"]["text"], attr_dict[cell_id]["content"]["decimal value"])
            self.set_cell_equ(cell_id, attr_dict[cell_id]["equation"])
            self.set_cell_formatting(cell_id, attr_dict[cell_id]["formatting"])

    def set_cell_foreground(self, cell_id, color):
        self.cell_dict[cell_id].configure(background=color)

    def set_cell_background(self, cell_id, color):
        self.cell_dict[cell_id].configure(background=color)

    def set_cell_content(self, cell_id, text, decimal_value=None):
        self.cell_dict[cell_id].set(text)
        self.cell_dict[cell_id].set_decimal_value(decimal_value)

    def set_cell_equ(self, cell_id, equ):
        self.cell_dict[cell_id].set_equ(equ)

    def set_cell_formatting(self, cell_id, formatting_dict):
        self.cell_dict[cell_id].set_formatting(formatting_dict)

    def reset_cell_formatting(self, cell_id):
        self.cell_dict[cell_id].reset_formatting()

    def get_cell_equ(self, cell_id):
        return self.cell_dict[cell_id].get_equ()

    def get_cell_content(self, cell_id):
        return {
                "text": self.cell_dict[cell_id].get(),
                "decimal value": self.cell_dict[cell_id].get_decimal_value()
                }

    def get_cell_formating(self, cell_id):
        return self.cell_dict[cell_id].get_formatting()

    def get_cell_decimal_value(self, cell_id):
        return self.cell_dict[cell_id].get_decimal_value()

    def _index_of_current_cell(self):
        if not isinstance(self.main_win.focus_get(), Cell):
            return 'break'
        return self.index_of(self.main_win.current_cell.id)

    def _set_focused_cell(self, new_index):
        cell = self.get_cell_by_index(new_index)
        cell.focus_set()
        self.main_win.update_cells(None)

    def nav_left(self, *args):
        new_index = self._index_of_current_cell() - 60
        if new_index < 0:
            return 'break'
        try:
            self._set_focused_cell(new_index)
        except KeyError:
            pass
        return 'break'

    def nav_right(self, *args):
        new_index = self._index_of_current_cell() + 60
        if new_index >= self.cell_count:
            return 'break'
        try:
            self._set_focused_cell(new_index)
        except KeyError:
            pass
        return 'break'

    def nav_up(self, *args):
        new_index = self._index_of_current_cell() - 1
        if new_index < 0:
            return 'break'
        try:
            self._set_focused_cell(new_index)
        except KeyError:
            pass
        return 'break'

    def nav_down(self, *args):
        new_index = self._index_of_current_cell() + 1
        try:
            self._set_focused_cell(new_index)
        except KeyError:
            pass
        return 'break'

