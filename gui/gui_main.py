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


class MainWindow(tk.Tk):
    def __init__(self, in_file=None):
        tk.Tk.__init__(self)
        self.padx = 2
        self.pady = 2

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

        self.cell_area.bind('<Configure>', self.on_cell_area_configure)
        self.bind('<Button-1>', self.update_cells)
        self.bind('<Left>', self.nav_left)
        self.bind('<Right>', self.nav_right)
        self.bind('<Up>', self.nav_up)
        self.bind('<Down>', self.nav_down)
        self.bind('<B1-Motion>', self.cell_area.select_cells)
        self.bind('<Control_L>c', self.cell_area.multi_copy)
        self.bind('<Control_L>x', self.cell_area.multi_cut)
        self.bind('<Control_L>v', self.cell_area.multi_paste)

        if in_file is not None:
            self.file_menu.open(in_file)

    def nav_left(self, *args):
        cell_index = self.cell_area.get_cell_index(self.current_cell.id)
        new_index = cell_index - 60
        if new_index < 0:
            return
        try:
            cell = self.cell_area.get_cell_by_index(new_index)
        except KeyError:
            return
        cell.focus_set()
        self.update_cells(None)

    def nav_right(self, *args):
        cell_index = self.cell_area.get_cell_index(self.current_cell.id)
        new_index = cell_index + 60
        if new_index >= self.cell_area.cell_count:
            return
        try:
            cell = self.cell_area.get_cell_by_index(new_index)
        except KeyError:
            return
        cell.focus_set()
        self.update_cells(None)

    def nav_up(self, *args):
        cell_index = self.cell_area.get_cell_index(self.current_cell.id)
        new_index = cell_index - 1
        if new_index < 0:
            return
        try:
            cell = self.cell_area.get_cell_by_index(new_index)
        except KeyError:
            return
        cell.focus_set()
        self.update_cells(None)

    def nav_down(self, *args):
        cell_index = self.cell_area.get_cell_index(self.current_cell.id)
        new_index = cell_index + 1
        if new_index > self.cell_area.cell_count:
            return
        try:
            cell = self.cell_area.get_cell_by_index(new_index)
        except KeyError:
            return
        cell.focus_set()
        self.update_cells(None)


    def set_last_save(self, clear_time=False):
        self.status_bar.set_last_save(f"Last Save: {datetime.now().strftime('%I:%M %p')}")

    def on_cell_area_configure(self, event):
        """Update scroll region when cell area size changes"""
        self.cell_canvas.configure(scrollregion=self.cell_canvas.bbox("all"))

    def update_cells(self, event):
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



