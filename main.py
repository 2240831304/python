

from tkinter import *
from Interface import mainwindow

import platform


if __name__ == "__main__":
    root = Tk()
    #print(platform.system())
    #print(root.winfo_screenwidth(),root.winfo_screenheight())
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    systemName = platform.system()

    if screenwidth > 1200:
        root.minsize(450,300)
    else:
        root.minsize(screenwidth-100,screenheight-100)
    app = mainwindow.MainWindow(root)
    root.mainloop()

