
from tkinter import *

from database import createdatabase



class MainWindow(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()


    def init_window(self):
        self.master.title("慧宝宝要学习")
        self.pack(fill=BOTH,expand=1)

        createDataBaseBut = Button(self,text="建数据库",command=self.createDatabaseSLot)
        createDataBaseBut.place(x=10,y=10)


    def createDatabaseSLot(self):
        print("mainwindow createDatabaseSLot start create database!")

        topWindow = Toplevel(self)
        topWindow.geometry("450x300")
        widget = createdatabase.CreateDataBaseWindow(topWindow)
        topWindow.mainloop()
