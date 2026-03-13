import tkinter as tk
import tkinter.ttk as ttk

class CommandSelection:
    def __init__(self, parent, equation_input):
        self.parent = parent
        self.equation_input = equation_input
        self.command_list_frame = tk.Frame(self.parent)
        self.equation_frame = tk.Frame(self.parent)
        self.preview_frame = tk.Frame(self.parent)
        self.command_list_frame.pack()
        self.equation_frame.pack()
        self.preview_frame.pack()

        self.equation_error = tk.StringVar()
        self.commands = self.equation_input.equations.keys()

        self.label = tk.Label(self.command_list_frame, text="Select equation by double-clicking")
        self.command_list = tk.Listbox(self.command_list_frame,
                                       selectmode=tk.SINGLE,
                                       width=75,
                                       relief=tk.FLAT,
                                       borderwidth=5,
                                       border=2,
                                       highlightthickness=1
                                       )
        self.label.pack()
        self.command_list.pack()
        for command in self.commands:
            self.command_list.insert(tk.END, f"{command}()")

        self.preview_cell = tk.Entry(self.equation_frame, width=5)
        self.preview_cell.insert(tk.END, self.equation_input.cell_entry.get())
        self.equals = tk.Label(self.equation_frame, text="=")
        self.preview_equation = tk.Entry(self.equation_frame,
                                         width=40, relief=tk.FLAT,
                                         borderwidth=5,
                                         border=2,
                                         highlightthickness=1)
        self.preview_equation.insert(tk.END, self.equation_input.equ_entry.get())
        self.select_button = ttk.Button(self.equation_frame, text="Confirm", command=self.confirm)
        self.cancel_button = ttk.Button(self.equation_frame, text='Cancel', command=self.cancel)

        self.select_button.grid(row=0, column=0, padx=5, pady=5)
        self.preview_cell.grid(row=0, column=1, padx=5, pady=5)
        self.equals.grid(row=0, column=2, padx=5, pady=5)
        self.preview_equation.grid(row=0, column=4, padx=5, pady=5)
        self.cancel_button.grid(row=0, column=5, padx=5, pady=5)

        self.answer_label = tk.Label(self.preview_frame, text='Answer: ', padx=5, pady=5)
        self.equation_answer_preview = tk.Label(self.preview_frame, textvariable=self.equation_error, padx=5, pady=5)
        self.answer_label.pack(side=tk.LEFT)
        self.equation_answer_preview.pack(side=tk.LEFT)

        self.parent.bind('<Key>', self.test_equation)
        self.parent.bind('<Return>', self.confirm)
        self.command_list.bind('<Double-Button-1>', self.get_selection)

    def get_selection(self, *args):
        command = self.command_list.get(self.command_list.curselection())
        command = command.split(" ")[0]
        self.preview_equation.delete(0, tk.END)
        self.preview_equation.insert(tk.END, command)
        self.preview_equation.focus_set()
        self.preview_equation.icursor(len(self.preview_equation.get()) - 1)

    def cancel(self):
        self.parent.destroy()

    def confirm(self, *args):
        self.equation_input.equ_entry.delete(0, tk.END)
        self.equation_input.cell_entry.delete(0, tk.END)
        self.equation_input.equ_entry.insert(tk.END, self.preview_equation.get())
        self.equation_input.cell_entry.insert(tk.END, self.preview_cell.get())
        self.equation_input.insert_equ()
        self.parent.destroy()

    def test_equation(self, *args):
        equation = self.preview_equation.get()
        ans = self.equation_input.parse_equation(equation)
        self.equation_error.set(ans)
