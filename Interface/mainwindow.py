
from tkinter import *

from database import createdatabase
from datamanager import insertsharewindow,selectdatawindow



class MainWindow(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()


    def init_window(self):
        self.master.title("慧宝宝要学习")
        self.pack(fill=BOTH,expand=1)

        createDataBaseBut = Button(self,text="建数据库",command=self.createDatabaseSLot)
        #createDataBaseBut.place(x=10,y=10)
        createDataBaseBut.grid(row=0,column=0)

        insetDataBut = Button(self,text="插入数据",command=self.insetDataSlot)
        insetDataBut.grid(row=1, column=0)

        selectDataBut = Button(self, text="查询数据", command=self.selectDataSlot)
        selectDataBut.grid(row=1, column=1)

        obtainDataBut = Button(self, text="获取数据", command=self.obtainDataSlot)
        obtainDataBut.grid(row=2, column=0)


    def createDatabaseSLot(self):
        print("mainwindow createDatabaseSLot start create database!")

        topWindow = Toplevel(self)
        topWindow.geometry("450x300")
        widget = createdatabase.CreateDataBaseWindow(topWindow)
        topWindow.mainloop()


    def insetDataSlot(self):
        topWindow = Toplevel(self)
        topWindow.geometry("450x300")
        widget = insertsharewindow.InsertShareWindow(topWindow)
        topWindow.mainloop()


    def selectDataSlot(self):
        topWindow = Toplevel(self)
        topWindow.geometry("450x300")
        widget = selectdatawindow.SelectDataWindow(topWindow)
        topWindow.mainloop()


    def obtainDataSlot(self):
        pass