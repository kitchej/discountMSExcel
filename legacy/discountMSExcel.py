from tkinter import *
import tkinter.ttk as ttk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from decimal import Decimal
from datetime import datetime
from datetime import timedelta
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


# 'cells' is the master list for all entry objects acting as cells. Each cell can be accessed by this list. The function
# 'get_cell_index' will return the index of cell given the actual entry object, and the CommandLine.get_cell_index
# method will return the index of a cell given it's coordinates (A1, B3, F12, etc). Each value in the list is a list
# containing two values: the entry object and an equation associated with it ('' by default). To access the entry box
# itself, one must write: cells[cell_index][0]

cells = []

colored_cells = []  # needed to reset cell colors after selecting them

entered_cells = []  # keeps track of selected cells

clipboard = []

root_entry = None  # need for multi_select functionality

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
                print('self.filename == ()', self.fileName)
                return
        save_data = []
        for cell in cells:
            save_data.append(
                [cell[0].get(), cell[0].cget("font"), cell[0].cget("background"), cell[0].cget("foreground"), cell[1]] # cell[1] == an equation associated with the cell
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
                cell[0].delete(0, END)
                cell[0].configure(font=('Helvetica', font_size), background='#ffffff', foreground='#000000')
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
            self.fileName = "Untitled.dme"
            self.master.title(self.fileName)
            for cell in cells:
                cell[0].delete(0, END)
                cell[0].configure(font=('Helvetica', font_size), background='#FFFFFF', foreground='#000000')
            last_save.set(f"Last Save: ")


class CommandSelection:
    def __init__(self, master, CL_obj):
        self.master = master
        self.CL_obj = CL_obj
        self.command_list_frame = Frame(self.master)
        self.equation_frame = Frame(self.master)
        self.preview_frame = Frame(self.master)
        self.command_list_frame.pack()
        self.equation_frame.pack()
        self.preview_frame.pack()

        self.equation_error = StringVar()
        self.commands = [
            'ADD() - Finds the sum of its arguments',
            'SUB() - Finds the difference of its arguments',
            'MULTI() - Finds the product of its arguments',
            'DIV() - Finds the quotient of its arguments',
            'AVRG() - Finds the average of its arguments',
            'TIMEDIFF() - Finds the difference of two times',
            'TIMEADD() - Adds time values together',
            'PAYROLL() - Takes a pay rate and multiplies it with a time value'
        ]

        self.label = Label(self.command_list_frame, text="Select equation by double-clicking")
        self.command_list = Listbox(self.command_list_frame, selectmode=SINGLE, width=75)
        self.label.pack()
        self.command_list.pack()
        for command in self.commands:
            self.command_list.insert(END, command)

        self.preview_cell = Entry(self.equation_frame, width=5)
        self.preview_cell.insert(END, self.CL_obj.cell_entry.get())
        self.equals = Label(self.equation_frame, text="=")
        self.preview_equation = Entry(self.equation_frame, width=40)
        self.preview_equation.insert(END, self.CL_obj.equation_entry.get())
        self.select_button = Button(self.equation_frame, text="Confirm", command=self.confirm)
        self.cancel_button = Button(self.equation_frame, text='Cancel', command=self.cancel)

        self.select_button.grid(row=0, column=0, padx=5, pady=5)
        self.preview_cell.grid(row=0, column=1, padx=5, pady=5)
        self.equals.grid(row=0, column=2, padx=5, pady=5)
        self.preview_equation.grid(row=0, column=4, padx=5, pady=5)
        self.cancel_button.grid(row=0, column=5, padx=5, pady=5)

        self.answer_label = Label(self.preview_frame, text='Answer: ', padx=5, pady=5)
        self.equation_answer_preview = Label(self.preview_frame, textvariable=self.equation_error, padx=5, pady=5)
        self.answer_label.pack(side=LEFT)
        self.equation_answer_preview.pack(side=LEFT)

        self.master.bind('<Key>', self.test_equation)
        self.command_list.bind('<Double-Button-1>', self.get_selection)

    def get_selection(self, *args):
        command = self.command_list.get(self.command_list.curselection())
        command = command.split(" ")[0]
        self.preview_equation.delete(0, END)
        self.preview_equation.insert(END, command)

    def cancel(self):
        self.master.destroy()

    def confirm(self):
        self.CL_obj.equation_entry.delete(0, END)
        self.CL_obj.cell_entry.delete(0, END)
        self.CL_obj.equation_entry.insert(END, self.preview_equation.get())
        self.CL_obj.cell_entry.insert(END, self.preview_cell.get())
        self.CL_obj.insert()
        self.master.destroy()

    def test_equation(self, *args):
        equation = self.preview_equation.get()
        ans = self.CL_obj.compute_equation(equation)
        self.equation_error.set(ans)


class CommandLine:
    def __init__(self, master):
        # dict that converts column letters into an index for the 'cells' list
        self.letter_map = {'A': 0, 'B': 40, 'C': 80, 'D': 120, 'E': 160, 'F': 200, 'G': 240, 'H': 280, 'I': 320,
                           'J': 360, 'K': 400}
        self.cell_coord_pattern = re.compile(r'[A-K]\d{1,2}')
        self.paddingx = 5
        self.paddingy = 0
        self.master = master
        self.insert_button = Button(self.master, text="Insert", command=self.insert)
        self.cell_entry = Entry(self.master, width=5)
        self.equal_sign = Label(self.master, text="=")
        self.equation_entry = Entry(self.master, width=40)
        self.cell_entry_label = Label(self.master, text="Cell")
        self.equation_entry_label = Label(self.master, text="Equation")
        self.equation_select_button = Button(self.master, text="⨍(x)", command=self.open_equation_wizard)

        self.cell_entry_label.grid(row=0, column=1, padx=self.paddingx, pady=self.paddingy)
        self.equation_entry_label.grid(row=0, column=4, padx=self.paddingx, pady=self.paddingy)
        self.insert_button.grid(row=1, column=0, padx=self.paddingx, pady=self.paddingy)
        self.cell_entry.grid(row=1, column=1, padx=self.paddingx, pady=self.paddingy)
        self.equal_sign.grid(row=1, column=2, padx=self.paddingx, pady=self.paddingy)
        self.equation_select_button.grid(row=1, column=3, padx=self.paddingx, pady=self.paddingy)
        self.equation_entry.grid(row=1, column=4, padx=self.paddingx, pady=self.paddingy)

    def open_equation_wizard(self):
        win = Toplevel()
        win.title("Function Wizard")
        c = CommandSelection(win, self)

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

    def add(self, in_args, *args):
        out_value = 0
        for arg in in_args:
            if re.fullmatch(self.cell_coord_pattern, arg):
                index = self.get_cell_index(arg)
                value = cells[index][0].get()
            else:
                value = arg
            try:
                out_value = out_value + float(value)
            except ValueError:
                return 'ERROR'
        return out_value

    def subtract(self, in_args, *args):
        out_value = 0
        for arg in in_args:
            if re.fullmatch(self.cell_coord_pattern, arg):
                index = self.get_cell_index(arg)
                value = cells[index][0].get()
            else:
                value = arg
            try:
                out_value = out_value - float(value)
            except ValueError:
                return 'ERROR'
        return out_value

    def divide(self, in_args, *args):
        out_value = 0
        for arg in in_args:
            if re.fullmatch(self.cell_coord_pattern, arg):
                index = self.get_cell_index(arg)
                value = cells[index][0].get()
            else:
                value = arg
            try:
                out_value = out_value / float(value)
            except ValueError:
                return 'ERROR'
            except ZeroDivisionError:
                return 'ERROR'

        return out_value

    def multiply(self, in_args, *args):
        out_value = 0
        for arg in in_args:
            if re.fullmatch(self.cell_coord_pattern, arg):
                index = self.get_cell_index(arg)
                value = cells[index][0].get()
            else:
                value = arg
            try:
                out_value = out_value * float(value)
            except ValueError:
                return 'ERROR'
        return out_value

    def average(self, in_args, *args):
        out_value = 0
        for arg in in_args:
            if re.fullmatch(self.cell_coord_pattern, arg):
                index = self.get_cell_index(arg)
                value = cells[index][0].get()
            else:
                value = arg
            try:
                out_value = out_value + int(value)
            except ValueError:
                return 'ERROR'
        return out_value / len(in_args)

    @staticmethod
    def get_time_delta(value):
        matches = ['AM', 'PM', 'am', 'pm', 'Pm', 'Am']
        if any(x in value for x in matches):  # Working with 12 hour format
            value = value.split(" ")
            time = value[0].split(":")
            try:
                hours = int(time[0])
            except ValueError:
                return 'ERROR'
            try:
                minutes = int(time[1])
            except IndexError:
                minutes = 0
            except ValueError:
                return 'ERROR'
            try:
                seconds = int(time[2])
            except IndexError:
                seconds = 0
            except ValueError:
                return 'ERROR'

            if value[1] == 'PM':
                if hours == 12:
                    pass
                else:
                    hours += 12
            elif value[1] == 'AM':
                if hours == 12:
                    hours += 12
        else:  # Working with 24 hour format
            time = value.split(":")
            try:
                hours = int(time[0])
            except ValueError:
                return 'ERROR'
            try:
                minutes = int(time[1])
            except IndexError:
                minutes = 0
            except ValueError:
                return 'ERROR'
            try:
                seconds = int(time[2])
            except IndexError:
                seconds = 0
            except ValueError:
                return 'ERROR'
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def time_diff(self, in_args, *args):
        if re.fullmatch(self.cell_coord_pattern, in_args[0]):
            index = self.get_cell_index(in_args[0])
            value1 = cells[index][0].get()
        else:
            value1 = in_args[0]

        if re.fullmatch(self.cell_coord_pattern, in_args[1]):
            index = self.get_cell_index(in_args[1])
            value2 = cells[index][0].get()
        else:
            value2 = in_args[1]

        if self.get_time_delta(value1) == 'ERROR':
            return 'ERROR'

        if self.get_time_delta(value2) == 'ERROR':
            return 'ERROR'

        return self.get_time_delta(value1) - self.get_time_delta(value2)

    def time_add(self, in_args, *args):
        added_time = timedelta()
        for arg in in_args:
            if re.fullmatch(self.cell_coord_pattern, arg):
                index = self.get_cell_index(arg)
                time_string = cells[index][0].get()
            else:
                time_string = arg
            time_delta = self.get_time_delta(time_string)
            if time_delta == 'ERROR':
                return "ERROR"
            added_time = added_time + time_delta

        return added_time

    def pay_roll(self, in_args):
        if re.fullmatch(self.cell_coord_pattern, in_args[0]):
            index1 = self.get_cell_index(in_args[0])
        else:
            return 'ERROR'
        if re.fullmatch(self.cell_coord_pattern, in_args[1]):
            index2 = self.get_cell_index(in_args[1])
        else:
            return 'ERROR'

        value1 = cells[index1][0].get()
        value2 = cells[index2][0].get()
        if ':' in value1:
            hours_worked = value1
            pay_rate = value2
        elif ':' in value2:
            hours_worked = value2
            pay_rate = value1
        else:
            return 'ERROR'

        if ':' in pay_rate:
            return 'ERROR'

        try:
            pay_rate = float(pay_rate)
        except ValueError:
            return 'ERROR'

        try:
            hours_worked = hours_worked.split(':')
            hours = int(hours_worked[0])
        except ValueError:
            return 'ERROR'

        try:
            minutes = int(hours_worked[1])
        except IndexError:
            minutes = 0
        except ValueError:
            return 'ERROR'
        try:
            seconds = int(hours_worked[2])
        except IndexError:
            seconds = 0
        except ValueError:
            return 'ERROR'

        seconds = seconds / 3600
        minutes = minutes / 60
        total_time = hours + minutes + seconds

        return round((pay_rate * total_time), 2)

    def parse_equation(self, in_equation, *args):
        equations = {
            'ADD': self.add,
            'SUB': self.subtract,
            'MULTI': self.multiply,
            'DIV': self.divide,
            'AVRG': self.average,
            'TIMEDIFF': self.time_diff,
            'TIMEADD': self.time_add,
            'PAYROLL': self.pay_roll
        }

        in_equation = in_equation.split('(')
        operator = in_equation[0]
        args = in_equation[1].strip(')')

        if len(args.split("::")) > 1:
            args = args.split('::')

            start_value = int(args[0][1])  # get row number
            end_value = int(args[1][1])
            column = args[0][0]  # get column letter

            number_of_cells = end_value - start_value

            included_cells = [args[0]]
            for _ in range(number_of_cells):
                start_value += 1
                included_cells.append(f"{column}{start_value}")
            args = included_cells
        else:
            args = args.split(',')

        answer = equations[operator](args)

        return answer

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
            with open('README', 'r', encoding="utf-8") as readme_file:
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

    if not isinstance(entry, Entry):
        return

    if entry == command_line.equation_entry:
        return

    if entry == command_line.cell_entry:
        return

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

    # Reset cells after deselecting
    global root_entry
    x, y = root.winfo_pointerxy()
    root_entry = root.winfo_containing(x, y)
    for cell in entered_cells:
        cell.configure(background='#ffffff')
    for colored_cell in colored_cells:
        colored_cell[0].configure(background=colored_cell[1])
    entered_cells.clear()


def bold_text(*args):
    entry = cell_frame.focus_get()
    if entry == command_line.equation_entry:
        return

    if entry == command_line.cell_entry:
        return

    if 'bold' in entry.cget('font'):
        entry.configure(font=('Helvetica', font_size))
    else:
        entry.configure(font=('Helvetica', font_size, 'bold'))
    return "break"


def italics_text(*args):
    entry = cell_frame.focus_get()
    if entry == command_line.equation_entry:
        return

    if entry == command_line.cell_entry:
        return

    if 'italic' in entry.cget('font'):
        entry.configure(font=('Helvetica', font_size))
    else:
        entry.configure(font=('Helvetica', font_size, 'italic'))
    return "break"


def underline_text(*args):
    entry = cell_frame.focus_get()
    if entry == command_line.equation_entry:
        return

    if entry == command_line.cell_entry:
        return

    if 'underline' in entry.cget('font'):
        entry.configure(font=('Helvetica', font_size))
    else:
        entry.configure(font=('Helvetica', font_size, 'underline'))
    return "break"


def strike_through_text(*args):
    entry = cell_frame.focus_get()
    if entry == command_line.equation_entry:
        return

    if entry == command_line.cell_entry:
        return

    if 'overstrike' in entry.cget('font'):
        entry.configure(font=('Helvetica', font_size))
    else:
        entry.configure(font=('Helvetica', font_size, 'overstrike'))
    return "break"


def change_bg(*args):
    entry = cell_frame.focus_get()
    if entry == command_line.equation_entry:
        return

    if entry == command_line.cell_entry:
        return

    color = colorchooser.askcolor()
    if color[1] == '#ffffff':
        colored_cells.remove([entry, entry.cget('background')])
    else:
        colored_cells.append([entry, color[1]])
    entry.configure(background=color[1])


def change_fg(*args):
    entry = cell_frame.focus_get()
    if entry == command_line.equation_entry:
        return

    if entry == command_line.cell_entry:
        return

    color = colorchooser.askcolor()
    entry.configure(foreground=color[1])
    update_cells()


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


def multi_copy(*args):
    global clipboard
    clipboard.clear()
    for cell in entered_cells:
        cell.configure(background='#ffffff')
        clipboard.append(cell.get())
    for colored_cell in colored_cells:
        colored_cell[0].configure(background=colored_cell[1])
    entered_cells.clear()
    return 'break'


def multi_cut(*args):
    global clipboard
    clipboard.clear()
    for cell in entered_cells:
        cell.configure(background='#ffffff')
        clipboard.append(cell.get())
        cell.delete(0, END)
    for colored_cell in colored_cells:
        colored_cell[0].configure(background=colored_cell[1])
    entered_cells.clear()
    return 'break'


def multi_paste(*args):
    first_entry = root.focus_get()
    index = get_cell_index(first_entry)

    for value in clipboard:
        cells[index][0].delete(0, END)
        cells[index][0].insert(0, value)
        index += 1
    return 'break'


def multi_delete(*args):
    if entered_cells:
        for cell in entered_cells:
            cell.delete(0, END)
        for cell in entered_cells:
            cell.configure(background='#ffffff')
        for colored_cell in colored_cells:
            colored_cell[0].configure(background=colored_cell[1])


def select_cells(*args):
    global root_entry

    x, y = root.winfo_pointerxy()
    entry = root.winfo_containing(x, y)

    if entry == command_line.equation_entry:
        return

    if entry == command_line.cell_entry:
        return

    if not isinstance(entry, Entry):
        return

    if entry == root_entry:  # I.E we haven't left the cell we clicked on, so don't do anything
        return
    else:  # Unless we leave, then highlight it and add it to 'entered_cells' if it is not already
        if root_entry not in entered_cells:
            root_entry.configure(background='#add8e6')
            entered_cells.append(root_entry)

    try:
        if entry not in entered_cells:
            entry.focus_set()
            entry.configure(background='#add8e6')
            entered_cells.append(entry)
    except AttributeError:
        return

    if entry != entered_cells[-1]:  # for deselecting cells when the cursor moves out of an cell
        entry.focus_set()
        entered_cells[-1].configure(background='#ffffff')
        entered_cells.pop()
        for colored_cell in colored_cells:
            colored_cell[0].configure(background=colored_cell[1])


def show_about():
    a = Toplevel()
    a.title("About Discount Microsoft Excel™")
    help_text = "A poor man's Microsoft Excel made with Tkinter and Python. Extremely simple with only\n" \
                "the most basic functions of a spreadsheet.\n" \
                "\n" \
                "What more do you expect from something called \'Discount Microsoft Excel™\'?"
    title_label = Label(a, text="Discount Microsoft Excel™\nWritten by Joshua Kitchen - July 2020\n", font='bold',
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
editMenu.add_command(label="Copy", accelerator="Ctrl+C", command=multi_copy)
editMenu.add_command(label="Cut", accelerator="Ctrl+X", command=multi_cut)
editMenu.add_command(label="Paste", accelerator="Ctrl+V", command=multi_paste)
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
bg_color_button = Button(tool_bar_frame, background='white', command=change_bg,  width=2)
fg_color_button = Button(tool_bar_frame, background='black', command=change_fg, width=2)

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

canvas = Canvas(cell_frame_master, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, highlightthickness=0)
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
root.bind('<B1-Motion>', select_cells)
root.bind('<Control_L>c', multi_copy)
root.bind('<Control_L>x', multi_cut)
root.bind('<Control_L>v', multi_paste)
root.bind('<BackSpace>', multi_delete)


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
