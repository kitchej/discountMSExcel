import tkinter.ttk as ttk
import tkinter as tk

class FormatMenu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, tearoff=0)
        self.parent = parent
        self.bold_btn = ttk.Button()
