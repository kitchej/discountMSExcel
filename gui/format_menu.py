import tkinter.ttk as ttk
import tkinter as tk

class FormatMenu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, tearoff=0)
        self.parent = parent
        self.add_command(label="Bold", accelerator="Ctrl+B", command=self.bold_text)
        self.add_command(label="Underline", accelerator="Ctrl+U", command=self.underline_text)
        self.add_command(label="Italics", accelerator="Ctrl+U", command=self.italics_text)
        self.add_command(label="Strikethrough", accelerator="Ctrl+T", command=self.strike_through_text)
        self.add_command(label="Text Color", command=self.change_fg)
        self.add_command(label="Background Color", command=self.change_bg)

    def bold_text(self):
        pass

    def underline_text(self):
        pass

    def italics_text(self):
        pass

    def strike_through_text(self):
        pass

    def change_fg(self):
        pass

    def change_bg(self):
        pass

