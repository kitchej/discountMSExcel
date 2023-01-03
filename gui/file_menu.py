import tkinter.ttk as ttk
import tkinter as tk

class FileMenu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, tearoff=0)
        self.parent = parent