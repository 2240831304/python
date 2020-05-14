
from tkinter import *

from database import createdatabase
from datamanager import insertsharewindow,selectdatawindow
from datamanager import obtaindata,shanghaistock,smarketobtaindata
from datamanager import smarketstock,smallstock
from datamanager import stockhistorydata
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

        self.smarketHistoryBut = None
        self.smarketHistoryState = True
        self.smarketHistoryObject = None

        self.stockHistoryBut = None
        self.stockHistoryState = True
        self.stockHistoryObject = None

        self.init_window()


    def init_window(self):
        self.master.title("慧宝宝要学习")
        self.pack(fill=BOTH,expand=1)
        self.objectPt = obtaindata.ObtainData()
        self.smarketDataGetObject = smarketobtaindata.SmarketObtainData()

        self.shanghaiObject = shanghaistock.ShangHaiStock()
        self.smarketObject = smarketstock.SmarketStock()
        self.smallObject = smallstock.SmallStock()

        self.stockHistoryObject = stockhistorydata.StockHistoryData()


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

        self.stockHistoryBut = Button(self, text="获取A股历史价格", command=self.stockHistorySlot)
        self.stockHistoryBut.grid(row=3, column=0)

        self.smarketHistoryBut = Button(self, text="获取创业板历史价格", command=self.smarketHistorySlot)
        self.smarketHistoryBut.grid(row=3, column=1)

        self.obtainDataBut = Button(self, text="获取A股实时数据", command=self.obtainDataSlot)
        self.obtainDataBut.grid(row=4, column=0)

        self.smarketDataGetBut = Button(self, text="获取创业板实时数据", command=self.smarketDataGetSlot)
        self.smarketDataGetBut.grid(row=4, column=1)


    def stockHistorySlot(self):
        if self.stockHistoryState:
            self.stockHistoryState = False
            self.stockHistoryBut["text"] = "停止请求数据"
            self.stockHistoryObject.excute()
        else:
            self.stockHistoryState = True
            self.stockHistoryBut["text"] = "获取A股历史价格"
            self.stockHistoryObject.setExecuteState(False)

    def smarketHistorySlot(self):
        pass



    def smarketSlot(self):
        if self.smarketState:
            self.smarketState = False
            self.smarketBut["text"] = "停止请求数据"
            self.smarketObject.excute()
        else:
            self.smarketState = True
            self.smarketBut["text"] = "获取创业板股票"
            self.smarketObject.setExecuteState(False)

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
        if self.smallState:
            self.smallState = False
            self.smallBut["text"] = "停止请求数据"
            self.smallObject.excute()
        else:
            self.smallState = True
            self.smallBut["text"] = "获取中小板股票"
            self.smallObject.setExecuteState(False)


    def smarketDataGetSlot(self):
        if self.smarketDataGetState:
            self.smarketDataGetState = False
            self.smarketDataGetBut["text"] = "停止请求数据"
            self.smarketDataGetObject.execute()
        else:
            self.smarketDataGetState =  True
            self.smarketDataGetBut["text"] = "获取创业板实时数据"
            self.smarketDataGetObject.setExecuteState(False)


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
            self.obtainDataBut["text"] = "获取A股实时数据"
            self.objectPt.setExecuteState(False)