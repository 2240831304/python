
from tkinter import *

from database import createdatabase
from datamanager import insertsharewindow,selectdatawindow
from datamanager import obtaindata,shanghaistock
import platform
import os


class MainWindow(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.objectPt = None
        self.obtainDataBut = None
        self.obtainDataState = True

        self.smarketDataGetBut = None
        self.smarketDataGetState = True
        self.smarketDataGetObject = None

        self.shanghaiBut = None
        self.shanghaiState = True
        self.shanghaiObject = None

        self.smallBut = None
        self.smallState = True
        self.smallObject = None

        self.smarketBut = None
        self.smarketState = True
        self.smarketObject = None

        self.init_window()


    def init_window(self):
        self.master.title("慧宝宝要学习")
        self.pack(fill=BOTH,expand=1)
        self.objectPt = obtaindata.ObtainData()
        self.shanghaiObject = shanghaistock.ShangHaiStock()

        createDataBaseBut = Button(self,text="建数据库",command=self.createDatabaseSLot)
        #createDataBaseBut.place(x=10,y=10)
        createDataBaseBut.grid(row=0,column=0)

        insetDataBut = Button(self,text="插入数据",command=self.insetDataSlot)
        insetDataBut.grid(row=1, column=0)

        selectDataBut = Button(self, text="查询数据", command=self.selectDataSlot)
        selectDataBut.grid(row=1, column=1)

        self.smarketBut = Button(self, text="获取创业板股票", command=self.smarketSlot)
        self.smarketBut.grid(row=2, column=0)
        self.shanghaiBut = Button(self, text="获取上证股票", command=self.shanghaiSlot)
        self.shanghaiBut.grid(row=2, column=1)
        self.smallBut = Button(self, text="获取中小板股票", command=self.smallSlot)
        self.smallBut.grid(row=2, column=2)

        self.obtainDataBut = Button(self, text="获取A股数据", command=self.obtainDataSlot)
        self.obtainDataBut.grid(row=3, column=0)

        self.smarketDataGetBut = Button(self, text="获取创业板股票数据", command=self.smarketDataGetSlot)
        self.smarketDataGetBut.grid(row=3, column=1)


    def smarketSlot(self):
        pass

    def shanghaiSlot(self):
        if self.shanghaiState:
            self.shanghaiState = False
            self.shanghaiBut["text"] = "停止请求数据"
            self.shanghaiObject.excute()
        else:
            self.shanghaiState = True
            self.shanghaiBut["text"] = "获取上证股票"
            self.shanghaiObject.setExecuteState(False)


    def smallSlot(self):
        pass

    def smarketDataGetSlot(self):
        pass

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
            self.obtainDataBut["text"] = "获取A股数据"
            self.objectPt.setExecuteState(False)