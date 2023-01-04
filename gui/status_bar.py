import tkinter.ttk as ttk
import tkinter as tk
import os

class StatusBar(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.parent = parent