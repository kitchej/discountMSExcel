import sys
import os
from gui.gui_main import MainWindow

def main():
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]) and not os.path.isdir(sys.argv[1]):
            main_win = MainWindow(sys.argv[1])
            main_win.mainloop()
        else:
            print(f"Cannot open {sys.argv[1]}")
    else:
        main_win = MainWindow()
        main_win.mainloop()

if __name__ == '__main__':
    main()