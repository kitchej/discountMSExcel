import tkinter.ttk as ttk
import tkinter as tk



class EquInput(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.parent = parent

        self.insert_btn = ttk.Button(self, text="Insert", command=self.insert_equ)
        self.cell_entry = tk.Entry(self, exportselection=0,
                                   width=4,
                                   relief=tk.FLAT,
                                   borderwidth=5,
                                   border=2,
                                   highlightthickness=1)
        self.cell_entry.insert(0, 'A1')
        self.equal_lab = ttk.Label(self, text="=")
        self.equ_entry = ttk.Combobox(self,
                                  exportselection=0,
                                  width=100,
                                  values=list(self.parent.equations.keys()))

        self.insert_btn.grid(row=0, column=0, padx=self.parent.padx, pady=self.parent.pady)
        self.cell_entry.grid(row=0, column=1, padx=self.parent.padx, pady=self.parent.pady)
        self.equal_lab.grid(row=0, column=2, padx=self.parent.padx, pady=self.parent.pady)
        self.equ_entry.grid(row=0, column=3, padx=self.parent.padx, pady=self.parent.pady)
        self.equ_entry.bind("<<ComboboxSelected>>", self.get_selection)
        self.equ_entry.bind('<KeyRelease>', self.insert_equ)

    def get_selection(self, *args):
        equ = f"{self.equ_entry.get()}()"
        self.equ_entry.set(equ)
        self.equ_entry.focus_set()
        self.equ_entry.icursor(len(equ) - 1)
        self.equ_entry.selection_clear()

    def set_current_cell(self, cell_id):
        self.cell_entry.configure(background="white", foreground="black")
        self.cell_entry.delete(0, tk.END)
        self.cell_entry.insert(0, cell_id)

    def set_equ(self, equation):
        self.equ_entry.delete(0, tk.END)
        self.equ_entry.insert(0, equation)

    def insert_equ(self, *args):
        equ_str = self.equ_entry.get()
        if not equ_str:
            return
        result = self.parent.compute_equation(equ_str)
        cell_id = self.cell_entry.get().upper()
        try:
            self.parent.cell_area.set_cell_content(cell_id, result)
        except KeyError:
            self.cell_entry.configure(background="red", foreground="white")
            return
        self.parent.cell_area.set_cell_equ(cell_id, self.equ_entry.get())
        self.set_current_cell(cell_id)

