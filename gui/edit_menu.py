import tkinter.ttk as ttk
import tkinter as tk

class EditMenu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, tearoff=0)
        self.parent = parent
        self.add_command(label="Cut", accelerator="Ctrl+C", command=self.copy)
        self.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        self.add_command(label="Cut", accelerator="Ctrl+V", command=self.paste)

    def copy(self):
        pass

    def cut(self):
        pass

    def paste(self):
        pass
