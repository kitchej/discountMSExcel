import tkinter.ttk as ttk
import tkinter as tk

class StatusBar(ttk.Frame):
    def __init__(self, main_win):
        super().__init__()
        self.main_win = main_win
        self.last_save_str = tk.StringVar()
        self.last_save_str.set("Not Saved")
        self.last_save_label = tk.Label(self, textvariable=self.last_save_str)
        self.last_save_label.pack(side=tk.LEFT)

    def set_last_save(self, text):
        self.last_save_str.set(text)