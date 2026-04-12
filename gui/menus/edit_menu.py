import tkinter as tk

class EditMenu(tk.Menu):
    def __init__(self, main_win):
        super().__init__(tearoff=0)
        self.main_win = main_win
        self.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
        self.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        self.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)

    def copy(self):
        self.main_win.cell_area.multi_copy()

    def cut(self):
        self.main_win.cell_area.multi_cut()

    def paste(self):
        self.main_win.cell_area.multi_paste()
