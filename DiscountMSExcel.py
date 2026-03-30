import sys
from gui.gui_main import MainWindow

def main():
    if len(sys.argv) > 1:
        main_win = MainWindow(sys.argv[1])
    else:
        main_win = MainWindow()
    main_win.mainloop()

if __name__ == '__main__':
    main()