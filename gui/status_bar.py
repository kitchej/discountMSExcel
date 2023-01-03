import tkinter.ttk as ttk
import tkinter as tk

class StatusBar(ttk.Frame):
    def __init__(self, parent, style):
        ttk.Frame.__init__(self)
        self.parent = parent
        self.style = style