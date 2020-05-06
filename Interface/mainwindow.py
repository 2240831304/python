
from tkinter import *

from database import createdatabase
from datamanager import insertsharewindow,selectdatawindow
from datamanager import obtaindata
import platform
import os


class MainWindow(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.objectPt = None
        self.obtainDataBut = None
        self.obtainDataState = True

        self.init_window()


    def init_window(self):
        self.master.title("慧宝宝要学习")
        self.pack(fill=BOTH,expand=1)
        self.objectPt = obtaindata.ObtainData()

        createDataBaseBut = Button(self,text="建数据库",command=self.createDatabaseSLot)
        #createDataBaseBut.place(x=10,y=10)
        createDataBaseBut.grid(row=0,column=0)

        insetDataBut = Button(self,text="插入数据",command=self.insetDataSlot)
        insetDataBut.grid(row=1, column=0)

        selectDataBut = Button(self, text="查询数据", command=self.selectDataSlot)
        selectDataBut.grid(row=1, column=1)

        self.obtainDataBut = Button(self, text="获取数据", command=self.obtainDataSlot)
        self.obtainDataBut.grid(row=2, column=0)


    def createDatabaseSLot(self):
        print("mainwindow createDatabaseSLot start create database!")

        topWindow = Toplevel(self)
        screenwidth = topWindow.winfo_screenwidth()
        screenheight = topWindow.winfo_screenheight()
        systemName = platform.system()

        if screenwidth > 1200:
            topWindow.minsize(450, 300)
        else:
            topWindow.minsize(screenwidth - 100, screenheight - 100)
        #topWindow.geometry("450x300")
        widget = createdatabase.CreateDataBaseWindow(topWindow)
        topWindow.mainloop()


    def insetDataSlot(self):
        topWindow = Toplevel(self)
        screenwidth = topWindow.winfo_screenwidth()
        screenheight = topWindow.winfo_screenheight()
        systemName = platform.system()

        if screenwidth > 1200:
            topWindow.minsize(450, 300)
        else:
            topWindow.minsize(screenwidth - 100, screenheight - 100)
        #topWindow.geometry("450x300")
        widget = insertsharewindow.InsertShareWindow(topWindow)
        topWindow.mainloop()


    def selectDataSlot(self):
        topWindow = Toplevel(self)
        screenwidth = topWindow.winfo_screenwidth()
        screenheight = topWindow.winfo_screenheight()
        systemName = platform.system()

        path = os.getcwd()
        filePath = path + "/log/system.txt"
        fileHandle = open(filePath, mode='a+')
        fileHandle.write("system:")
        fileHandle.write(str(systemName))
        fileHandle.write(" ")
        fileHandle.write(str(screenwidth))
        fileHandle.write(" ")
        fileHandle.write(str(screenheight))
        fileHandle.write("\n")
        fileHandle.close()

        if screenwidth > 1200:
            topWindow.minsize(450, 300)
        else:
            topWindow.minsize(screenwidth - 100, screenheight - 100)
        #topWindow.geometry("450x300")
        widget = selectdatawindow.SelectDataWindow(topWindow)
        widget.setSystem(1)
        topWindow.mainloop()


    def obtainDataSlot(self):
        if self.obtainDataState :
            self.obtainDataState = False
            self.obtainDataBut["text"] = "停止请求数据"
            self.objectPt.execute()
        else:
            self.obtainDataState = True
            self.obtainDataBut["text"] = "获取数据"
            self.objectPt.setExecuteState(False)