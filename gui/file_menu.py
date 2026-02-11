import tkinter.ttk as ttk
import tkinter as tk


class FileMenu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, tearoff=0)
        self.parent = parent
        self.add_command(label="Open", accelerator="Ctrl+O", command=self.open)
        self.add_command(label="Save", accelerator="Ctrl+S", command=self.save)
        self.add_command(label="Save As", accelerator="Ctrl+S", command=self.save_as)
        self.add_command(label="New",command=self.new)

    def save(self):
        pass

    def save_as(self):
        pass

    def open(self):
        pass

    def new(self):
        pass



