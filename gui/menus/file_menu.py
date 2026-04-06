import pickle
from tkinter import filedialog, messagebox
import tkinter as tk


class FileMenu(tk.Menu):
    def __init__(self, main_win):
        super().__init__(tearoff=0)
        self.main_win = main_win
        self.filepath = "Untitled.dme"
        self.add_command(label="Open", accelerator="Ctrl+O", command=self.open)
        self.add_command(label="Save", accelerator="Ctrl+S", command=self.save)
        self.add_command(label="Save As", accelerator="Ctrl+S", command=self.save_as)
        self.add_command(label="New",command=self.new)

    def save(self):
        if self.filepath == "Untitled.dme":
            new_filename = filedialog.asksaveasfilename(filetypes=(('*.dme', '*.dme'), ('*.csv', '*.csv')))
            if new_filename  == ():
                return
            self.filepath = new_filename

        save_data = self.main_win.cell_area.get_all_cells_attributes()
        try:
            with open(self.filepath, 'wb') as save_file:
                pickle.dump(save_data, save_file)
            self.main_win.title(self.filepath.split("/")[-1])
            self.main_win.set_last_save()
        except (FileNotFoundError, OSError, pickle.PicklingError):
            messagebox.showerror(title="Error", message=f"Could not save to {self.filepath}")
        except PermissionError:
            messagebox.showerror(title="Error", message=f"You do not have permission to save to {self.filepath}")

    def save_as(self):
        new_filename = filedialog.asksaveasfilename(filetypes=(('*.dme', '*.dme'), ('*.csv', '*.csv')))
        if new_filename == ():
            return
        self.filepath = new_filename
        self.save()

    def open(self, filename=None):
        old_filepath = self.filepath
        if not filename:
            self.filepath = filedialog.askopenfilename(filetypes=(('*.dme', '*.dme'), ('*.csv', '*.csv')))
            if self.filepath == ():
                return
        else:
            self.filepath = filename
        try:
            with open(self.filepath, 'rb') as open_file:
                save_data = pickle.load(open_file)
        except (FileNotFoundError, OSError, pickle.UnpicklingError):
            messagebox.showerror(title="Error", message=f"Could not open {self.filepath}")
            self.filepath = old_filepath
        except PermissionError:
            messagebox.showerror(title="Error", message=f"You do not have permission to save to {self.filepath}")
            self.filepath = old_filepath

        self.main_win.cell_area.clear_all_cells_attributes()
        self.main_win.set_last_save(clear_time=True)
        self.main_win.cell_area.set_all_cells_attributes(save_data)
        self.main_win.title(self.filepath.split("/")[-1])
        self.main_win.set_last_save(clear_time=True)

    def new(self):
        answer = messagebox.askyesnocancel(title='Save?', message=f"Save {self.filepath} before creating new file?")
        if answer:
            self.save()
            self.filepath = "Untitled.dme"
            self.main_win.title(self.filepath)
        elif answer is None:
            return
        self.main_win.cell_area.clear_all_cells_attributes()
        self.main_win.set_last_save(clear_time=True)



