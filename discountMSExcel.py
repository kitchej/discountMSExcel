from tkinter import *
import tkinter.ttk as ttk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from decimal import Decimal
from datetime import datetime
import re
import os
import pickle
from PIL import Image, ImageTk

"""
Discount Microsoft Excel
Written by Joshua Kitchen - July 2020

How the .dme file extension works 
----------------------------------------------------------------------------------------------------------------------

Some files can be saved as a .dme. it was made up by me as a solution to saving the users formatting. When a file is 
saved, all the cell text, formatting, colors, and equations are saved to a list (in that order). The list is then 
pickled. When a file is opened, the the attributes from the pickled file are looped through and added to their 
respective cell (attributes are saved in the same order, so indexes in the attributes list line up with the list of 
entry objects) """


# master list for all entry objects acting as cells. Each cell can be accessed by this list. The function
# 'get_cell_index' will return the index of cell given the actual entry object, and the CommandLine.get_cell_index
# method will return the index of a cell given it's coordinates. Each value in the list is a list containing two
# values: the entry object and an equation associated with it ('' by default). To access the entry box itself,
# one must write: cells[cell_index][0]

cells = []

if os.name == 'nt':
    font_size = 11
else:
    font_size = 12


class File:
    def __init__(self, master):
        self.master = master
        self.file_path = ""
        self.fileName = "Untitled.dme"
        self.master.title(self.fileName)

    def save(self, *args):
        fileNameOld = self.fileName  # in case save operations fail, we can reset the file name
        if self.fileName == "Untitled.dme":
            self.fileName = filedialog.asksaveasfilename(filetypes=(('*.dme', '*.dme'), ('*.csv', '*.csv')))
            if self.fileName == ():
                return
        save_data = []
        for cell in cells:
            save_data.append(
                [cell[0].get(), cell[0].cget("font"), cell[0].cget("background"), cell[0].cget("foreground"), cell[1]] # cell[1] == and equation associated with the cell
            )
        try:
            with open(self.fileName, 'wb') as save_file:
                pickle.dump(save_data, save_file)
            self.master.title(self.fileName.split("/")[-1])
            last_save.set(f"Last Save: {datetime.now().strftime('%I:%M %p')}")
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File not found")
            self.fileName = fileNameOld
        except PermissionError:
            messagebox.showerror(title="Error", message="Current user does not have permission to save this to this"
                                                        "directory")
            self.fileName = fileNameOld
        except OSError:
            messagebox.showerror(title="Error", message="Cannot save file")
            self.fileName = fileNameOld

    def open(self, *args):
        fileNameOld = self.fileName  # in case open operations fail, we can reset the file name
        self.fileName = filedialog.askopenfilename(filetypes=(('*.dme', '*.dme'), ('*.csv', '*.csv')))
        if self.fileName == ():
            return
        try:
            with open(self.fileName, 'rb') as open_file:
                save_data = pickle.load(open_file)
            for cell, data in zip(cells, save_data):
                cell[0].insert(0, data[0])
                cell[0].configure(font=data[1], background=data[2], foreground=data[3])
                cell[1] = data[4]
            self.master.title(self.fileName.split("/")[-1])
            last_save.set(f"Last Save: ")
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File not found")
            self.fileName = fileNameOld
        except PermissionError:
            messagebox.showerror(title="Error", message="Current user does not have permission to open files"
                                                        "from this directory")
            self.fileName = fileNameOld
        except OSError:
            messagebox.showerror(title="Error", message="Cannot open file")
            self.fileName = fileNameOld

    def new(self, *args):
        answer = messagebox.askyesnocancel(title='Save?', message=f"Save {self.fileName} before creating new file?")
        if answer is True:
            self.save()
            self.fileName = "Untitled.dme"
            self.master.title(self.fileName)
            for cell in cells:
                cell[0].delete(0, END)
                cell[0].configure(font=('Helvetica', font_size), background='#FFFFFF', foreground='#000000')
        elif answer is None:
            return
        else:
            self.fileName = "Untitled.dmw"
            self.master.title(self.fileName)
            for cell in cells:
                cell[0].delete(0, END)
                cell[0].configure(font=('Helvetica', font_size), background='#FFFFFF', foreground='#000000')
            last_save.set(f"Last Save: ")


class CommandLine:
    def __init__(self, master):
        # dict that converts column letters into an index for the 'cells' list
        self.letter_map = {'A': 0, 'B': 40, 'C': 80, 'D': 120, 'E': 160, 'F': 200, 'G': 240, 'H': 280, 'I': 320,
                           'J': 360, 'K': 400}
        self.cell_coord_pattern = re.compile(r'[A-K]\d{1,2}')
        self.paddingx = 5
        self.paddingy = 0
        self.master = master
        self.insert_button = ttk.Button(self.master, text="Insert", command=self.insert)
        self.cell_entry = ttk.Entry(self.master, width=5)
        self.equal_sign = Label(self.master, text="=")
        self.equation_entry = ttk.Entry(self.master, width=40)
        self.cell_entry_label = Label(self.master, text="Cell")
        self.equation_entry_label = Label(self.master, text="Equation")

        self.cell_entry_label.grid(row=0, column=1, padx=self.paddingx, pady=self.paddingy)
        self.equation_entry_label.grid(row=0, column=3, padx=self.paddingx, pady=self.paddingy)
        self.insert_button.grid(row=1, column=0, padx=self.paddingx, pady=self.paddingy)
        self.cell_entry.grid(row=1, column=1, padx=self.paddingx, pady=self.paddingy)
        self.equal_sign.grid(row=1, column=2, padx=self.paddingx, pady=self.paddingy)
        self.equation_entry.grid(row=1, column=3, padx=self.paddingx, pady=self.paddingy)

    def get_cell_index(self, cell_coord):
        index = None
        if re.fullmatch(self.cell_coord_pattern, cell_coord):
            if len(cell_coord) == 2:
                letter = cell_coord[0]
                number = cell_coord[1]
                index = int(self.letter_map.get(letter)) + (int(number) - 1)
            else:
                letter = cell_coord[0]
                number = cell_coord[1] + cell_coord[2]
                index = int(self.letter_map.get(letter)) + (int(number) - 1)
        return index

    def parse_equation(self, in_equation):
        global cells
        matches = re.findall(self.cell_coord_pattern, in_equation)
        for match in matches:
            cell_index = self.get_cell_index(match)
            cell_value = cells[cell_index][0].get()
            if cell_value == '':
                in_equation = in_equation.replace(match, 0)
            else:
                in_equation = in_equation.replace(match, cell_value)
        try:
            answer = eval(in_equation, {})
            return answer
        except NameError:
            return "NameError"
        except SyntaxError:
            return "Syntax Error"

    def insert(self, saved_equation=None, cell_obj=None):
        if saved_equation:
            insert_value = self.parse_equation(saved_equation)
            if cell_obj.get():
                cell_obj.delete(0, END)
            cell_obj.insert(0, insert_value)
        else:
            insert_value = self.parse_equation(self.equation_entry.get())
            cell_index = self.get_cell_index(self.cell_entry.get())
            if cells[cell_index][0].get():
                cells[cell_index][0].delete(0, END)
            cells[cell_index][0].insert(0, insert_value)
            cells[cell_index][1] = self.equation_entry.get()


class Features:
    def __init__(self, master):
        self.master = master
        self.master.title("Features")
        self.text = Text(self.master, wrap=WORD)
        self.scrollbar = Scrollbar(self.master)
        self.text.pack(side=LEFT)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.configure(command=self.text.yview)
        try:
            with open('README', 'r') as readme_file:
                self.readme_text = readme_file.read()
        except FileNotFoundError:
            self.readme_text = "Your readme file was deleted. Guess you'll never know how this program works."
        self.text.insert(1.0, self.readme_text)
        self.text.configure(state='disabled')


root = Tk()

main_icon = PhotoImage(file=os.path.join('icons', 'main_icon.png'))

root.iconphoto(True, main_icon)

root.geometry('1500x950')


def get_cell_index(entry_obj):
    global cells
    index = 0
    for cell in cells:
        if cell[0] == entry_obj:
            return index
        index += 1


def update_cells(*args):
    global bg_color_button
    global fg_color_button

    entry = cell_frame.focus_get()

    # update color buttons to match the cell in focus
    bg = entry.cget("background")
    fg = entry.cget("foreground")
    bg_color_button.configure(background=bg)
    fg_color_button.configure(background=fg)

    # Update all cells with an equation
    for cell in cells:
        if cell[1] != '':
            if cell[0].get() == '':  # get rid of equation if the cell has been cleared
                cell[1] = ''
            else:
                command_line.insert(cell[1], cell[0])
        else:
            pass

    # Update the equation entry box to show equations or values (if there is no equation)
    #
    # find out the coordinates to the selected entry box
    index = get_cell_index(entry)
    coords = index / 40
    coords = Decimal(str(coords))
    row = Decimal(str(coords)) % 1
    column = coords - row
    row = (row*40) + 1
    row = int(row)
    column = int(column)
    letters = list(command_line.letter_map.keys())
    letter = letters[column]
    position = f"{letter}{row}"
    if cells[index][1] != '':  # if cell value determined by equation, show it
        command_line.equation_entry.delete(0, END)
        command_line.equation_entry.insert(0, cells[index][1])
    else:  # Else, show the value in the cell
        command_line.equation_entry.delete(0, END)
        command_line.equation_entry.insert(0, entry.get())
    command_line.cell_entry.delete(0, END)
    command_line.cell_entry.insert(0, position)


def bold_text(*args):
    entry = cell_frame.focus_get()
    if 'bold' in entry.cget('font'):
        entry.configure(font=('Helvetica', font_size))
    else:
        entry.configure(font=('Helvetica', font_size, 'bold'))
    return "break"


def italics_text(*args):
    entry = cell_frame.focus_get()
    if 'italic' in entry.cget('font'):
        entry.configure(font=('Helvetica', font_size))
    else:
        entry.configure(font=('Helvetica', font_size, 'italic'))
    return "break"


def underline_text(*args):
    entry = cell_frame.focus_get()
    if 'underline' in entry.cget('font'):
        entry.configure(font=('Helvetica', font_size))
    else:
        entry.configure(font=('Helvetica', font_size, 'underline'))
    return "break"


def strike_through_text(*args):
    entry = cell_frame.focus_get()
    if 'overstrike' in entry.cget('font'):
        entry.configure(font=('Helvetica', font_size))
    else:
        entry.configure(font=('Helvetica', font_size, 'overstrike'))
    return "break"


def change_bg(*args):
    entry = cell_frame.focus_get()
    color = colorchooser.askcolor()
    entry.configure(background=color[1])
    update_cells()


def change_fg(*args):
    entry = cell_frame.focus_get()
    color = colorchooser.askcolor()
    entry.configure(foreground=color[1])
    update_cells()


def copy(*args):
    entry = cell_frame.focus_get()
    entry.event_generate('<<Copy>>')


def cut(*args):
    entry = cell_frame.focus_get()
    entry.event_generate('<<Cut>>')


def paste(*args):
    entry = cell_frame.focus_get()
    entry.event_generate('<<Paste>>')


def nav_left(*args):
    global cells
    current_cell = cell_frame.focus_get()
    cell_index = get_cell_index(current_cell)
    try:
        new_index = cell_index - 40
    except TypeError:
        return
    if new_index < 0:
        return
    else:
        cells[new_index][0].focus_set()
        update_cells()


def nav_right(*args):
    global cells
    current_cell = cell_frame.focus_get()
    cell_index = get_cell_index(current_cell)
    try:
        new_index = cell_index + 40
    except TypeError:
        return
    if new_index > 440:
        return
    else:
        cells[new_index][0].focus_set()
        update_cells()


def nav_up(*args):
    global cells
    current_cell = cell_frame.focus_get()
    cell_index = get_cell_index(current_cell)
    try:
        new_index = cell_index - 1
    except TypeError:
        return
    if new_index < 0:
        return
    else:
        cells[new_index][0].focus_set()
        update_cells()


def nav_down(*args):
    global cells
    current_cell = cell_frame.focus_get()
    cell_index = get_cell_index(current_cell)
    try:
        new_index = cell_index + 1
    except TypeError:
        return
    if new_index > 440:
        return
    else:
        cells[new_index][0].focus_set()
        update_cells()

                          
def show_about():
    a = Toplevel()
    a.title("About Discount Microsoft Word™")
    help_text = "A poor man's Microsoft Word made with Tkinter and Python. Extremely simple with only\n" \
                "the most basic functions of a word processor.\n" \
                "\n" \
                "What more do you expect from something called \'Discount Microsoft Word™\'?"
    title_label = Label(a, text="Discount Microsoft Word™\nWritten by Joshua Kitchen - June 2020\n", font='bold',
                        justify='center')
    about_label = Label(a, text=help_text)
    title_label.pack()
    about_label.pack()


def show_features():
    b = Toplevel()
    b.minsize(width=50, height=75)
    b.title("Help")
    help_text = Features(b)


# File Obj

file = File(root)

# Menu Bar

menubar = Menu(root)

fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label='Open', accelerator="Ctrl+O", command=file.open)
fileMenu.add_command(label='Save', accelerator="Ctrl+S", command=file.save)
fileMenu.add_command(label='New', accelerator="Ctrl+N", command=file.new)
menubar.add_cascade(menu=fileMenu, label='File')

editMenu = Menu(menubar, tearoff=0)
editMenu.add_command(label="Copy", accelerator="Ctrl+C", command=copy)
editMenu.add_command(label="Cut", accelerator="Ctrl+X", command=cut)
editMenu.add_command(label="Paste", accelerator="Ctrl+V", command=paste)
menubar.add_cascade(menu=editMenu, label='Edit')

formatMenu = Menu(menubar, tearoff=0)
formatMenu.add_command(label="Bold", accelerator="Ctrl+B", command=bold_text)
formatMenu.add_command(label="Underline", accelerator="Ctrl+U", command=underline_text)
formatMenu.add_command(label="Italics", accelerator="Ctrl+U", command=italics_text)
formatMenu.add_command(label="Strikethrough", accelerator="Ctrl+T", command=strike_through_text)
formatMenu.add_command(label="Text Color", command=change_fg)
formatMenu.add_command(label="Background Color", command=change_bg)
menubar.add_cascade(menu=formatMenu, label='Format')

helpMenu = Menu(menubar, tearoff=0)
helpMenu.add_command(label='Features', command=show_features)
helpMenu.add_command(label='About', command=show_about)
menubar.add_cascade(menu=helpMenu, label='Help')
root.config(menu=menubar)

# Frames

tool_bar_frame = Frame(root)
command_line_frame = Frame(root)
cell_frame_master = Frame(root)
status_frame = Frame(root)

tool_bar_frame.pack(fill=X, side=TOP)
command_line_frame.pack(fill=X, side=TOP)
status_frame.pack(fill=X, side=BOTTOM)
cell_frame_master.pack(fill=X, side=BOTTOM)

# Tool Bar

paddingx = 1
paddingy = 1

save_image = Image.open(os.path.join("icons", "save_icon.png"))
bold_image = Image.open(os.path.join("icons", "bold_icon.png"))
italics_image = Image.open(os.path.join("icons", "italics_icon.png"))
underline_image = Image.open(os.path.join("icons", "underline_icon.png"))
strike_through_image = Image.open(os.path.join("icons", "strikethrough_icon.png"))
open_image = Image.open(os.path.join("icons", "open_icon.png"))
new_image = Image.open(os.path.join("icons", "new_icon.png"))

save_icon = ImageTk.PhotoImage(image=save_image)
bold_icon = ImageTk.PhotoImage(image=bold_image)
italics_icon = ImageTk.PhotoImage(image=italics_image)
underline_icon = ImageTk.PhotoImage(image=underline_image)
strike_through_icon = ImageTk.PhotoImage(image=strike_through_image)
open_icon = ImageTk.PhotoImage(image=open_image)
new_icon = ImageTk.PhotoImage(image=new_image)

new_button = Button(tool_bar_frame, image=new_icon, command=file.new)
open_button = Button(tool_bar_frame, image=open_icon, command=file.open)
save_button = Button(tool_bar_frame, image=save_icon, command=file.save)
bold_button = Button(tool_bar_frame, image=bold_icon, command=bold_text)
italics_button = Button(tool_bar_frame, image=italics_icon, command=italics_text)
underline = Button(tool_bar_frame, image=underline_icon, command=underline_text)
strikethrough_button = Button(tool_bar_frame, image=strike_through_icon, command=strike_through_text)
bg_label = Label(tool_bar_frame, text="Background")
fg_label = Label(tool_bar_frame, text="Text Color")
bg_color_button = Button(tool_bar_frame, background='white', command=change_bg)
fg_color_button = Button(tool_bar_frame, background='black', command=change_fg)

new_button.pack(side=LEFT, padx=paddingx, pady=paddingy)
open_button.pack(side=LEFT, padx=paddingx, pady=paddingy)
save_button.pack(side=LEFT, padx=paddingx, pady=paddingy)
bold_button.pack(side=LEFT, padx=paddingx, pady=paddingy)
italics_button.pack(side=LEFT, padx=paddingx, pady=paddingy)
underline.pack(side=LEFT, padx=paddingx, pady=paddingy)
strikethrough_button.pack(side=LEFT, padx=paddingx, pady=paddingy)
bg_label.pack(side=LEFT, padx=paddingx, pady=paddingy)
bg_color_button.pack(side=LEFT, padx=paddingx, pady=paddingy)
fg_label.pack(side=LEFT, padx=paddingx, pady=paddingy)
fg_color_button.pack(side=LEFT, padx=paddingx, pady=paddingy)

# Command Line

command_line = CommandLine(command_line_frame)

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
        cell = Entry(column_frame)
        if os.name == 'nt':
            cell.configure(font=('Helvetica', font_size))
        else:
            cell.configure(font=('Helvetica', font_size), borderwidth=0)
        cells.append([cell, ""])
        cell.pack()

# Status
last_save = StringVar()
last_save.set("Last Save: ")
status_bar = Label(status_frame, textvariable=last_save, justify=LEFT)
status_bar.pack(fill=X, side=LEFT)

# Bindings

root.bind('<Control_L>o', file.open)
root.bind('<Control_L>s', file.save)
root.bind('<Control_L>n', file.new)
root.bind('<Control_L>b', bold_text)
root.bind('<Control_L>u', underline_text)
root.bind('<Control_L>i', italics_text)
root.bind('<Control_L>t', strike_through_text)
root.bind('<Button-1>', update_cells)
root.bind('<Left>', nav_left)
root.bind('<Right>', nav_right)
root.bind('<Up>', nav_up)
root.bind('<Down>', nav_down)


def close():
    name = file.fileName.split("/")[-1]
    answer = messagebox.askyesnocancel(title="Save?", message=f"Do you want to save {name} before quitting?")
    if answer is True:
        file.save()
        root.quit()
    elif answer is None:
        return
    else:
        root.quit()


root.protocol('WM_DELETE_WINDOW', close)

root.mainloop()
