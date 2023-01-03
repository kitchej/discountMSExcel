import tkinter.ttk as ttk
import tkinter as tk

import equations as equ

class EquInput(ttk.Frame):
    def __init__(self, parent, style, cell_area):
        ttk.Frame.__init__(self)
        self.parent = parent
        self.style = style
        self.cell_area = cell_area