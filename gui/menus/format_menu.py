import tkinter as tk
from tkinter import colorchooser

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
        self.parent.current_cell.toggle_bold()

    def underline_text(self):
        self.parent.current_cell.toggle_underline()

    def italics_text(self):
        self.parent.current_cell.toggle_italics()

    def strike_through_text(self):
        self.parent.current_cell.toggle_strikethrough()

    def change_fg(self):
        color = colorchooser.askcolor()
        self.parent.current_cell.set_fg(color[1])

    def change_bg(self):
        color = colorchooser.askcolor()
        self.parent.current_cell.set_bg(color[1])

