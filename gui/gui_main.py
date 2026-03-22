import tkinter as tk
import os
from datetime import datetime


from gui.menus.file_menu import FileMenu
from gui.menus.edit_menu import EditMenu
from gui.menus.format_menu import FormatMenu
from gui.menus.help_menu import HelpMenu
from gui.format_bar import FormatBar
from gui.equ_input import EquInput
from gui.cell_area import CellArea, Cell
from gui.status_bar import StatusBar
import backend.equations as equ


class MainWindow(tk.Tk):
    def __init__(self, in_file=None):
        tk.Tk.__init__(self)
        self.padx = 2
        self.pady = 2

        self.equations = {
            "SUM": equ.get_sum,
            "DIFF": equ.get_difference,
            "MULT": equ.get_product,
            "DIV": equ.get_quotient,
            "FLOOR": equ.get_floor,
            "CEIL": equ.get_ceiling,
            "TRUNC": equ.get_trunc,
            "ROUND": equ.get_round,
            "AVG": equ.get_average
        }

        self.title("Discount MS Excel")
        self.geometry('1400x950')
        self.iconphoto = tk.PhotoImage(False, file=os.path.join('gui', 'icons', 'main_icon.png'))

        self.main_menu = tk.Menu(self)
        self.file_menu = FileMenu(self)
        self.edit_menu = EditMenu(self)
        self.format_menu = FormatMenu(self)
        self.help_menu = HelpMenu(self)
        self.main_menu.add_cascade(menu=self.file_menu, label='File')
        self.main_menu.add_cascade(menu=self.edit_menu, label='Edit')
        self.main_menu.add_cascade(menu=self.format_menu, label='Format')
        self.main_menu.add_cascade(menu=self.help_menu, label='Help')
        self.configure(menu=self.main_menu)

        self.canvas_frame = tk.Frame(self)
        self.toolbar_frame = tk.Frame(self)
        self.status_frame = tk.Frame(self)

        self.format_bar = FormatBar(self, master=self.toolbar_frame)
        self.equ_bar = EquInput(self, master=self.toolbar_frame)
        self.format_bar.pack(side=tk.TOP, anchor=tk.W)
        self.equ_bar.pack(side=tk.BOTTOM, anchor=tk.W)

        self.cell_canvas = tk.Canvas(master=self.canvas_frame, relief=tk.FLAT, highlightthickness=0)
        self.cell_area = CellArea(self, master=self.cell_canvas)
        self.current_cell = self.cell_area.get_cell_by_index(0)
        self.cell_canvas.create_window((0, 0), window=self.cell_area, anchor=tk.NW)
        self.scrollbar_v = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.cell_canvas.yview)
        self.scrollbar_h = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.cell_canvas.xview)
        self.cell_canvas.configure(
            yscrollcommand=self.scrollbar_v.set,
            xscrollcommand=self.scrollbar_h.set
        )
        self.scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.cell_canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_bar = StatusBar(self.status_frame)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.toolbar_frame.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Remove default bindings for Entry boxes
        for seq in ("<<Cut>>", "<<Copy>>", "<<Paste>>", "<<PasteSelection>>"):
            self.unbind_class(tk.Entry.winfo_class(self), seq)

        self.cell_area.bind('<Configure>', self.on_cell_area_configure)
        self.bind('<Button-1>', self.update_cells)
        self.bind('<Left>', self.cell_area.nav_left)
        self.bind('<Right>', self.cell_area.nav_right)
        self.bind('<Up>', self.cell_area.nav_up)
        self.bind('<Down>', self.cell_area.nav_down)
        self.bind('<B1-Motion>', self.cell_area.select_cells)
        self.bind('<Control_L>c', self.cell_area.multi_copy)
        self.bind('<Control_L>x', self.cell_area.multi_cut)
        self.bind('<Control_L>v', self.cell_area.multi_paste)
        self.bind('<BackSpace>', self.cell_area.multi_delete)
        self.bind("<MouseWheel>", self._on_mousewheel)

        if in_file is not None:
            self.file_menu.open(in_file)

    def _on_mousewheel(self, event):
        self.cell_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def parse_equation(self, equation):
        error_output = 'ERROR', [], []
        if equation == "":
            return error_output
        equation = equation.upper()
        equation = equation.split('(')
        if len(equation) != 2:
            return error_output
        operator = equation[0]
        args = equation[1].strip(')')

        if len(args.split(":")) > 1:
            args = args.split(':')
            try:
                start_value = int(args[0][1:])
                end_value = int(args[1][1:])
            except (IndexError, ValueError):
                return error_output
            column = args[0][0]
            number_of_cells = end_value - start_value
            included_cells = [args[0]]
            for _ in range(number_of_cells):
                start_value += 1
                included_cells.append(f"{column}{start_value}")
            args = included_cells
        else:
            arg_strings = args.split(',')
            args = []
            for arg in arg_strings:
                args.append(arg.strip())

        if len(args) == 0:
            return error_output
        values = []
        cells = []
        for arg in args:
            try:
                arg_value = self.cell_area.get_cell_content(arg)
                cells.append(arg)
            except KeyError:
                try:
                    arg_value = int(arg)
                except ValueError:
                    return error_output
            values.append(arg_value)

        return operator, values, cells

    def compute_equation(self, equation):
        operator, values, _ = self.parse_equation(equation)
        if operator == 'ERROR':
            return 'ERROR'
        return self.equations[operator](values)

    def set_last_save(self, clear_time=False):
        self.status_bar.set_last_save(f"Last Save: {datetime.now().strftime('%I:%M %p')}")

    def on_cell_area_configure(self, *args):
        """Update scroll region when cell area size changes"""
        self.cell_canvas.configure(scrollregion=self.cell_canvas.bbox("all"))

    def update_cells(self, *args):
        # Update equation entry with current cell
        cell = self.focus_get()
        if not isinstance(cell, Cell):
            return
        self.equ_bar.set_current_cell(cell.id)
        self.equ_bar.set_equ(cell.equ)
        self.current_cell = cell
        self.format_bar.set_fg_button_color(self.current_cell.get_fg())
        self.format_bar.set_bg_button_color(self.current_cell.get_bg())

        self.cell_area.reset_multi_cell_select()




