from tkinter import *
import tkinter.ttk as ttk
import re


class CommandLine:
    def __init__(self, master):
        self.key_words = ['AVERAGE', 'SUM', 'DIFFERENCE', 'PRODUCT', 'DIVIDEND']
        self.letter_map = {'A': 0, 'B': 40, 'C': 80, 'D': 120, 'E': 160, 'F': 200, 'G': 240, 'H': 280, 'I': 320, 'J': 360, 'K': 400}
        self.cell_pattern = re.compile(r'[A-K]\d{1,2}')
        self.paddingx = 5
        self.paddingy = 0
        self.master = master
        self.insert_button = ttk.Button(self.master, text="Insert", command=self.insert)
        self.cell_entry = ttk.Entry(self.master, width=5)
        self.equal_sign = Label(self.master, text="=")
        self.equation_entry = ttk.Entry(self.master, width=40)
        self.cell_entry_label = Label(self.master, text="Cell")
        self.equation_entry_label = Label(self.master, text="Equation/Value")

        self.cell_entry_label.grid(row=0, column=0, padx=self.paddingx, pady=self.paddingy)
        self.equation_entry_label.grid(row=0, column=3, padx=self.paddingx, pady=self.paddingy)
        self.insert_button.grid(row=1, column=0, padx=self.paddingx, pady=self.paddingy)
        self.cell_entry.grid(row=1, column=1, padx=self.paddingx, pady=self.paddingy)
        self.equal_sign.grid(row=1, column=2, padx=self.paddingx, pady=self.paddingy)
        self.equation_entry.grid(row=1, column=3, padx=self.paddingx, pady=self.paddingy)

    def average(self):
        pass

    def sum(self):
        pass

    def difference(self):
        pass

    def product(self):
        pass

    def dividend(self):
        pass

    def get_cell_index(self, value):
        index = None
        if re.fullmatch(self.cell_pattern, value):
            if len(value) == 2:
                letter = value[0]
                number = value[1]
                index = int(self.letter_map.get(letter)) + (int(number) - 1)
            else:
                letter = value[0]
                number = value[1] + value[2]
                index = int(self.letter_map.get(letter)) + (int(number) - 1)
        return index

    def get_equation(self, in_value):
        global cells
        matches = re.findall(self.cell_pattern, in_value)
        for match in matches:
            cell_index = self.get_cell_index(match)
            cell_value = cells[cell_index].get()
            in_value = in_value.replace(match, cell_value)
            try:
                eval(in_value, {})
                return eval(in_value, {})
            except NameError:
                return "Error"

    def insert(self):
        insert_value = self.get_equation(self.equation_entry.get())
        cell_index = self.get_cell_index(self.cell_entry.get())
        if cells[cell_index].get():
            cells[cell_index].delete(0, END)
        cells[cell_index].insert(0, insert_value)


root = Tk()
root.geometry('1500x950')

load_indicator = Toplevel()
load_indicator.geometry("500x500")
load_label = Label(load_indicator, text="Loading...", font="bold", justify=CENTER)
load_label.pack()


def kill_load_screen():
    load_indicator.destroy()


cells = []


tool_bar_frame = Frame(root)
command_line_frame = Frame(root)
cell_frame_master = Frame(root)
status_frame = Frame(root)

tool_bar_frame.pack(fill=X, side=TOP)
command_line_frame.pack(fill=X, side=TOP)
status_frame.pack(fill=X, side=BOTTOM)
cell_frame_master.pack(fill=X, side=BOTTOM)

# Tool Bar

for i in range(5):
    button = Button(tool_bar_frame, text=f"Button {i}")
    button.pack(side=LEFT)

# Command Line

comm = CommandLine(command_line_frame)

# Cells


def canvasResize(*args):
    canvas.configure(scrollregion=canvas.bbox("all"), width=1000, height=900)


scroll_y = ttk.Scrollbar(cell_frame_master)
scroll_y.pack(side=RIGHT, fill=Y, expand=0)

scroll_x = ttk.Scrollbar(cell_frame_master, orient=HORIZONTAL)
scroll_x.pack(side=BOTTOM, fill=X, expand=0)

canvas = Canvas(cell_frame_master, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
canvas.pack(fill=BOTH)
scroll_y.configure(command=canvas.yview)
scroll_x.configure(command=canvas.xview)

cell_frame = Frame(canvas)
canvas.create_window((0, 0), window=cell_frame, anchor='nw')
cell_frame.bind("<Configure>", canvasResize)

labels_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

row_frame = Frame(cell_frame)
row_frame.pack(side=LEFT, fill=Y)
whitespace = Label(row_frame)
whitespace.pack()

for i in range(40):
    row_label = Label(row_frame, text=f"{i + 1}", relief=RAISED, width=5)
    row_label.pack(fill=BOTH, side=TOP)

for label in labels_columns:
    column_frame = Frame(cell_frame)
    column_frame.pack(side=LEFT)
    column_label = Label(column_frame, text=label, justify='center', relief=RAISED)
    column_label.pack(fill=X)
    for i in range(40):
        cell = ttk.Entry(column_frame)
        cells.append(cell)
        cell.pack()


# Status
status_bar = Label(status_frame, text="This is the status bar", relief='sunken')
status_bar.pack(fill=X, side=BOTTOM)

root.after(0, kill_load_screen)
root.mainloop()
