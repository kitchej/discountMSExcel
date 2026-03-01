import re
import tkinter.ttk as ttk
import tkinter as tk

import backend.equations as equ

class EquInput(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.equations = {
            "SUM": equ.get_sum,
            "DIFF": equ.get_difference,
            "MULT": equ.get_product,
            "DIV": equ.get_quotient,
            "FLOOR": equ.get_floor,
            "CEIL": equ.get_ceiling,
            "TRUNC": equ.get_trunc,
            "ROUND": equ.get_round,
            "AVG": equ.get_average
        }

        self.parent = parent
        self.cell_coord_pattern = re.compile(r'[A-K]\d{1,2}')

        self.insert_btn = ttk.Button(self, text="Insert", command=self.insert_equ)
        self.cell_entry = tk.Entry(self, exportselection=0, width=4, relief=tk.FLAT, borderwidth=5, border=2, highlightthickness=1)
        self.cell_entry.insert(0, 'A1')
        self.equal_lab = ttk.Label(self, text="=")
        self.function_btn = ttk.Button(self, text="𝑓(𝑥)")
        self.equ_entry = tk.Entry(self, exportselection=0, width=100, relief=tk.FLAT, borderwidth=5, border=2, highlightthickness=1)

        self.insert_btn.grid(row=0, column=0, padx=self.parent.padx, pady=self.parent.pady)
        self.cell_entry.grid(row=0, column=1, padx=self.parent.padx, pady=self.parent.pady)
        self.equal_lab.grid(row=0, column=2, padx=self.parent.padx, pady=self.parent.pady)
        self.function_btn.grid(row=0, column=3, padx=self.parent.padx, pady=self.parent.pady)
        self.equ_entry.grid(row=0, column=4, padx=self.parent.padx, pady=self.parent.pady)

    def set_current_cell(self, cell_id):
        self.cell_entry.configure(background="white", foreground="black")
        self.cell_entry.delete(0, tk.END)
        self.cell_entry.insert(0, cell_id)

    def set_equ(self, equ):
        self.equ_entry.delete(0, tk.END)
        self.equ_entry.insert(0, equ)

    def parse_equation(self, equation):
        if equation == "":
            return 'ERROR'
        equation = equation.upper()
        equation = equation.split('(')
        if len(equation) == 0:
            return 'ERROR'
        operator = equation[0]
        args = equation[1].strip(')')

        if len(args.split("::")) > 1:
            args = args.split('::')
            start_value = int(args[0][1])
            end_value = int(args[1][1])
            column = args[0][0]
            number_of_cells = end_value - start_value
            included_cells = [args[0]]
            for _ in range(number_of_cells):
                start_value += 1
                included_cells.append(f"{column}{start_value}")
            args = included_cells
        else:
            arg_strings = args.split(',')
            args = []
            for arg in arg_strings:
                args.append(arg.strip())

        if len(args) == 0:
            return 'ERROR'
        values = []
        for arg in args:
            if re.fullmatch(self.cell_coord_pattern, arg):
                try:
                    values.append(self.parent.cell_area.get_cell_content(arg))
                except (KeyError, ValueError):
                    return 'ERROR'
            else:
                values.append(arg)
        return self.equations[operator](values)

    def insert_equ(self):
        result = self.parse_equation(self.equ_entry.get())
        try:
            cell_id = self.cell_entry.get().upper()
            self.parent.cell_area.set_cell_content(cell_id, result)
            self.parent.cell_area.set_cell_equ(cell_id, self.equ_entry.get())
            self.set_current_cell(cell_id)
        except KeyError:
            self.cell_entry.configure(background="red", foreground="white")

