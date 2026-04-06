import tkinter.ttk as ttk
import tkinter as tk
import os
from tkinter import colorchooser


class FormatBar(ttk.Frame):
    def __init__(self, main_win, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_win = main_win

        self.font_paddingx = 4
        self.format_paddingx = 4

        self.bold_image = tk.PhotoImage(file=os.path.join('gui', 'icons', 'bold_icon.png'))
        self.bold_btn = ttk.Button(self, image=self.bold_image, style='TButton', command=self.toggle_bold)

        self.italics_image = tk.PhotoImage(file=os.path.join('gui', 'icons', 'italics_icon.png'))
        self.italics_btn = ttk.Button(self, image=self.italics_image, style='TButton', command=self.toggle_italics)

        self.underline_image = tk.PhotoImage(file=os.path.join('gui', 'icons', 'underline_icon.png'))
        self.underline_btn = ttk.Button(self, image=self.underline_image, style='TButton', command=self.toggle_underline)

        self.strike_image = tk.PhotoImage(file=os.path.join('gui', 'icons', 'strikethrough_icon.png'))
        self.strike_btn = ttk.Button(self, image=self.strike_image, style='TButton', command=self.toggle_strikethrough)

        self.background_lab = ttk.Label(self, text="Background:")
        self.background_btn = tk.Button(self, background='white', width=2, activebackground='white', command=self.set_bg)

        self.foreground_lab = ttk.Label(self, text="Foreground:")
        self.foreground_btn = tk.Button(self, background='black', width=2, activebackground='black', command=self.set_fg)

        self.format_lab = ttk.Label(self, text="Number Format: ")
        self.format_combo = ttk.Combobox(self,
                                         state="readonly",
                                         values=("Plain Text", "Scientific", "Financial"), exportselection=0)

        self.format_combo.set("Plain Text")

        self.bold_btn.grid(row=0, column=0, padx=self.main_win.padx, pady=self.main_win.pady)
        self.italics_btn.grid(row=0, column=1, padx=self.main_win.padx, pady=self.main_win.pady)
        self.underline_btn.grid(row=0, column=2, padx=self.main_win.padx, pady=self.main_win.pady)
        self.strike_btn.grid(row=0, column=3, padx=self.main_win.padx, pady=self.main_win.pady)
        self.background_lab.grid(row=0, column=4, padx=self.main_win.padx, pady=self.main_win.pady)
        self.background_btn.grid(row=0, column=5, padx=self.main_win.padx, pady=self.main_win.pady)
        self.foreground_lab.grid(row=0, column=6, padx=self.main_win.padx, pady=self.main_win.pady)
        self.foreground_btn.grid(row=0, column=7, padx=self.main_win.padx, pady=self.main_win.pady)
        self.format_lab.grid(row=0, column=10, padx=self.format_paddingx, pady=self.main_win.pady)
        self.format_combo.grid(row=0, column=11, padx=self.main_win.padx, pady=self.main_win.pady)

        self.format_combo.bind("<<ComboboxSelected>>", self.on_format_combo_select)

    def on_format_combo_select(self, *args):
        num_format = self.format_combo.get()
        current_cell = self.main_win.current_cell
        if num_format == "Plain Text":
            current_cell.to_plain_text()
        elif num_format == "Financial":
            current_cell.to_financial()
        elif num_format == "Scientific":
            current_cell.to_scientific()

    def set_format_combo(self, option):
        self.format_combo.set(option)

    def set_fg_button_color(self, color):
        self.foreground_btn.configure(bg=color)

    def set_bg_button_color(self, color):
        self.background_btn.configure(bg=color)

    def toggle_bold(self):
        self.main_win.current_cell.toggle_bold()

    def toggle_italics(self):
        self.main_win.current_cell.toggle_italics()

    def toggle_underline(self):
        self.main_win.current_cell.toggle_underline()

    def toggle_strikethrough(self):
        self.main_win.current_cell.toggle_strikethrough()

    def set_bg(self):
        color = colorchooser.askcolor()
        self.main_win.current_cell.configure(background=color[1])
        self.set_bg_button_color(color[1])

    def set_fg(self):
        color = colorchooser.askcolor()
        self.main_win.current_cell.configure(foreground=color[1])
        self.set_fg_button_color(color[1])
