

from tkinter import *
from Interface import mainwindow


if __name__ == "__main__":
    root = Tk()
    root.geometry("450x300")
    app = mainwindow.MainWindow(root)
    root.mainloop()

