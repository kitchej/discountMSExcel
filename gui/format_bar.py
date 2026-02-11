import tkinter.ttk as ttk
import tkinter as tk
import os

class FormatBar(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.parent = parent

        self.font_paddingx = 4
        self.format_paddingx = 4

        self.bold_image = tk.PhotoImage(file=os.path.join('gui', 'icons', 'bold_icon.png'))
        self.bold_btn = ttk.Button(self, image=self.bold_image, style='TButton')

        self.italics_image = tk.PhotoImage(file=os.path.join('gui', 'icons', 'italics_icon.png'))
        self.italics_btn = ttk.Button(self, image=self.italics_image, style='TButton')

        self.underline_image = tk.PhotoImage(file=os.path.join('gui', 'icons', 'underline_icon.png'))
        self.underline_btn = ttk.Button(self, image=self.underline_image, style='TButton')

        self.strike_image = tk.PhotoImage(file=os.path.join('gui', 'icons', 'strikethrough_icon.png'))
        self.strike_btn = ttk.Button(self, image=self.strike_image, style='TButton')

        self.background_lab = ttk.Label(self, text="Background:")
        self.background_btn = tk.Button(self, background='white', width=2, activebackground='white')

        self.foreground_lab = ttk.Label(self, text="Foreground:")
        self.foreground_btn = tk.Button(self, background='black', width=2, activebackground='black')

        self.font_combo = ttk.Combobox(self,
                                       state='readonly',
                                       values=("Arial", "Helvetica", "Times"),
                                       exportselection=0)
        self.font_combo.set("Arial")
        self.font_size_combo = ttk.Combobox(self,
                                            state='readonly',
                                            values=("10", '11', '12', '14', '16', '20', '24'),
                                            exportselection=0)

        self.font_size_combo.set("11")

        self.format_lab = ttk.Label(self, text="Number Format: ")
        self.format_combo = ttk.Combobox(self,
                                         state="readonly",
                                         values=("Plain Text", "Scientific", "Financial"), exportselection=0)

        self.format_combo.set("Plain Text")

        self.bold_btn.grid(row=0, column=0, padx=self.parent.padx, pady=self.parent.pady)
        self.italics_btn.grid(row=0, column=1, padx=self.parent.padx, pady=self.parent.pady)
        self.underline_btn.grid(row=0, column=2, padx=self.parent.padx, pady=self.parent.pady)
        self.strike_btn.grid(row=0, column=3, padx=self.parent.padx, pady=self.parent.pady)
        self.background_lab.grid(row=0, column=4, padx=self.parent.padx, pady=self.parent.pady)
        self.background_btn.grid(row=0, column=5, padx=self.parent.padx, pady=self.parent.pady)
        self.foreground_lab.grid(row=0, column=6, padx=self.parent.padx, pady=self.parent.pady)
        self.foreground_btn.grid(row=0, column=7, padx=self.parent.padx, pady=self.parent.pady)
        self.font_combo.grid(row=0, column=8, padx=self.font_paddingx, pady=self.parent.pady)
        self.font_size_combo.grid(row=0, column=9, padx=self.font_paddingx, pady=self.parent.pady)
        self.format_lab.grid(row=0, column=10, padx=self.format_paddingx, pady=self.parent.pady)
        self.format_combo.grid(row=0, column=11, padx=self.parent.padx, pady=self.parent.pady)

