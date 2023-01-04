import tkinter.ttk as ttk
import tkinter as tk
import os

import backend.equations as equ

class EquInput(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.parent = parent
        self.insert_btn = ttk.Button(self, text="Insert")
        self.cell_entry = ttk.Entry(self, exportselection=0, width=3)
        self.cell_entry.insert(0, 'A1')
        self.equal_lab = ttk.Label(self, text="=")
        self.function_btn = ttk.Button(self, text="𝑓(𝑥)")
        self.equ_entry = ttk.Entry(self, exportselection=0, width=100)

        self.insert_btn.grid(row=0, column=0, padx=self.parent.padx, pady=self.parent.pady)
        self.cell_entry.grid(row=0, column=1, padx=self.parent.padx, pady=self.parent.pady)
        self.equal_lab.grid(row=0, column=2, padx=self.parent.padx, pady=self.parent.pady)
        self.function_btn.grid(row=0, column=3, padx=self.parent.padx, pady=self.parent.pady)
        self.equ_entry.grid(row=0, column=4, padx=self.parent.padx, pady=self.parent.pady)
