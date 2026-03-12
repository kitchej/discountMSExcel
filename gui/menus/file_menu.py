import pickle
from tkinter import filedialog, messagebox
import tkinter as tk
from datetime import datetime


class FileMenu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, tearoff=0)
        self.parent = parent
        self.filename = "Untitled.dme"
        self.add_command(label="Open", accelerator="Ctrl+O", command=self.open)
        self.add_command(label="Save", accelerator="Ctrl+S", command=self.save)
        self.add_command(label="Save As", accelerator="Ctrl+S", command=self.save_as)
        self.add_command(label="New",command=self.new)

    def save(self):
        old_filename = self.filename  # in case save operations fail, we can reset the file name
        if self.filename == "Untitled.dme":
            self.filename = filedialog.asksaveasfilename(filetypes=(('*.dme', '*.dme'), ('*.csv', '*.csv')))
            if self.filename == ():
                self.filename = old_filename
                return
        save_data = self.parent.cell_area.get_all_cells_attributes()

        try:
            with open(self.filename, 'wb') as save_file:
                pickle.dump(save_data, save_file)
            self.parent.title(self.filename.split("/")[-1])
            self.parent.set_last_save()
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File not found")
            self.filename = old_filename
        except PermissionError:
            messagebox.showerror(title="Error", message="Current user does not have permission to save this to this"
                                                        "directory")
            self.filename = old_filename
        except OSError:
            messagebox.showerror(title="Error", message="Cannot save file")
            self.filename = old_filename


    def save_as(self):
        old_filename = self.filename
        self.filename = filedialog.asksaveasfilename(filetypes=(('*.dme', '*.dme'), ('*.csv', '*.csv')))
        if self.filename == ():
            self.filename = old_filename
            return
        self.save()

    def open(self, filename=None):
        old_filename = self.filename  # in case open operations fail, we can reset the file name
        if not filename:
            self.filename = filedialog.askopenfilename(filetypes=(('*.dme', '*.dme'), ('*.csv', '*.csv')))
            if self.filename == ():
                return
        else:
            self.filename = filename
        try:
            with open(self.filename, 'rb') as open_file:
                save_data = pickle.load(open_file)
                self.parent.cell_area.set_all_cells_attributes(save_data)
            self.parent.title(self.filename.split("/")[-1])
            self.parent.set_last_save(clear_time=True)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File not found")
            self.filename = old_filename
        except PermissionError:
            messagebox.showerror(title="Error", message="Current user does not have permission to save this to this"
                                                        "directory")
            self.filename = old_filename
        except OSError:
            messagebox.showerror(title="Error", message="Cannot save file")
            self.filename = old_filename

    def new(self):
        answer = messagebox.askyesnocancel(title='Save?', message=f"Save {self.filename} before creating new file?")
        if answer:
            self.save()
            self.filename = "Untitled.dme"
            self.parent.title(self.filename)
        elif answer is None:
            return
        self.parent.cell_area.clear_all_cells_attributes()
        self.parent.set_last_save(clear_time=True)



