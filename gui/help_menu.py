import os
import tkinter.ttk as ttk
import tkinter as tk

class Features:
    def __init__(self, master):
        self.master = master
        self.master.title("Features")
        self.text = tk.Text(self.master, wrap=tk.WORD)
        self.scrollbar = tk.Scrollbar(self.master)
        self.text.pack(side=tk.LEFT)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.configure(command=self.text.yview)
        try:
            print(os.listdir())
            with open('README', 'r', encoding="utf-8") as readme_file:
                self.readme_text = readme_file.read()
        except FileNotFoundError:
            self.readme_text = "Your readme file was deleted. Guess you'll never know how this program works."
        self.text.insert(1.0, self.readme_text)
        self.text.configure(state='disabled')

class HelpMenu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, tearoff=0)
        self.parent = parent
        self.add_command(label="About", command=self.show_about)
        self.add_command(label="User Guide", command=self.show_features)

    @staticmethod
    def show_about():
        a = tk.Toplevel()
        a.title("About Discount Microsoft Excel™")
        help_text = "A poor man's Microsoft Excel made with Tkinter and Python. Extremely simple with only\n" \
                    "the most basic functions of a spreadsheet.\n" \
                    "\n" \
                    "What more do you expect from something called \'Discount Microsoft Excel™\'?"
        title_label = ttk.Label(a, text="Discount Microsoft Excel™\nWritten by Joshua Kitchen - July 2020\n", font='bold',
                            justify='center')
        about_label = ttk.Label(a, text=help_text)
        title_label.pack()
        about_label.pack()

    @staticmethod
    def show_features():
        b = tk.Toplevel()
        b.minsize(width=50, height=75)
        b.title("Help")
        _ = Features(b)

