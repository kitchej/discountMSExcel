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
        self.test.configure("new.TLabel", background="blue", foregorund='White', borderwidth=12)

        self.cell = ttk.Style()
        self.cell.configure("default.TEntry", borderwidth=2)


class MainWindow(tk.Tk):
    def __init__(self, in_file=None):
        tk.Tk.__init__(self)
        self.padx = 2
        self.pady = 2

        self.style = Style()
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
        self.main_menu.add_cascade(menu=self.format_menu, label='Help')
        self.configure(menu=self.main_menu)

        self.canvas_frame = tk.Frame(self)
        self.toolbar_frame = tk.Frame(self)
        self.status_frame = tk.Frame(self)

        self.format_bar = FormatBar(self, master=self.toolbar_frame)
        self.equ_bar = EquInput(self, master=self.toolbar_frame)
        self.format_bar.pack(side=tk.TOP, anchor=tk.W)
        self.equ_bar.pack(side=tk.BOTTOM, anchor=tk.W)

        self.cell_canvas = tk.Canvas(master=self.canvas_frame)
        self.cell_area = CellArea(self, master=self.cell_canvas)
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
        self.status_bar.pack()

        self.toolbar_frame.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



        self.cell_area.bind('<Configure>', self._on_cell_area_configure)


    def _on_cell_area_configure(self, event):
        """Update scroll region when cell area size changes"""
        self.cell_canvas.configure(scrollregion=self.cell_canvas.bbox("all"))



