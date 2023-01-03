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

class MainWindow(tk.Tk):
    def __init__(self, in_file=None):
        tk.Tk.__init__(self)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style = None
        self.title("Discount MS Excel")
        self.iconphoto = tk.PhotoImage(False, file=os.path.join('gui', 'icons', 'main_icon.png'))

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

        self.format_bar = FormatBar(self, self.style)
        self.cell_area = CellArea(self, self.style)
        self.equ_bar = EquInput(self, self.style, self.cell_area)
        self.status_bar = StatusBar(self, self.style)

        self.format_bar.grid(row=0, column=0)
        self.equ_bar.grid(row=1, column=0)
        self.cell_area.grid(row=2, column=0)
        self.status_bar.grid(row=2, column=0)

