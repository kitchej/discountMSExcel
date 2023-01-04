import tkinter.ttk as ttk
import tkinter as tk
import os

from gui.file_menu import FileMenu
from gui.edit_menu import EditMenu
from gui.format_menu import FormatMenu
from gui.help_menu import HelpMenu
from gui.format_bar import FormatBar
from gui.equ_input import EquInput
from gui.cell_area import CellArea
from gui.status_bar import StatusBar


class Style:
    def __init__(self):
        # style names must be "newname.oldname"
        self.btn_style = ttk.Style()
        self.btn_style.configure("TButton", margin=1)

        self.test = ttk.Style()
        self.test.configure("new.TFrame", background="blue")


class MainWindow(tk.Tk):
    def __init__(self, in_file=None):
        tk.Tk.__init__(self)
        self.style = Style()
        self.title("Discount MS Excel")
        self.geometry('1550x950')
        self.iconphoto = tk.PhotoImage(False, file=os.path.join('gui', 'icons', 'main_icon.png'))

        self.padx = 2
        self.pady = 2

        self.main_menu = tk.Menu(self)
        self.file_menu = FileMenu(self)
        self.edit_menu = EditMenu(self)
        self.format_menu = FormatMenu(self)
        self.help_menu = HelpMenu(self)
        self.main_menu.add_cascade(menu=self.file_menu, label='File')
        self.main_menu.add_cascade(menu=self.edit_menu, label='Edit')
        self.main_menu.add_cascade(menu=self.format_menu, label='Format')
        self.main_menu.add_cascade(menu=self.format_menu, label='Help')
        self.configure(menu=self.main_menu)

        self.format_bar = FormatBar(self)
        self.cell_area = CellArea(self)
        self.equ_bar = EquInput(self)
        self.status_bar = StatusBar(self)

        self.format_bar.grid(row=0, column=0, sticky=tk.W)
        self.equ_bar.grid(row=1, column=0, sticky=tk.W)
        self.cell_area.grid(row=2, column=0, sticky=tk.W)
        self.status_bar.grid(row=3, column=0, sticky=tk.W)

