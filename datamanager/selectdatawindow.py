
from tkinter import *
from tkinter import ttk
import sqlite3
import os

class SelectDataWindow(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.databaseFilePath = ""

        self.stateEntry = ""
        self.tableList = None
        self.strVar = StringVar()
        self.finishedLabel = None

        self.init_window()


    def init_window(self):
        self.master.title("查询数据")
        self.pack(fill=BOTH, expand=1)
        self.update()
        #print("当前窗口的宽度为", self.winfo_width())
        #print("当前窗口的高度为", self.winfo_height())

        columnWidth = int(self.winfo_width() / 5)

        name = Label(self,text="股票状态")
        name.grid(row=0,column=0,sticky=W)
        self.stateEntry = Entry(self,textvariable=self.strVar)
        self.stateEntry.grid(row=0,column=0)

        selectBut = Button(self, text="查询数据", command=self.selectDataSlot)
        selectBut.grid(row=1, column=0, sticky=N+S)
        #self.finishedLabel = Label(self,text="0")
        #self.finishedLabel.grid(row=1, column=0, sticky=W)

        style = ttk.Style(self)
        style.configure('Treeview', rowheight=30)

        self.tableList = ttk.Treeview(self, show="headings",style='Treeview')
        self.tableList.grid(row=2,column=0,sticky=W)
        self.tableList['columns'] = ['name','minprice','maxprice','curprice',"gap"]
        #self.tableList.pack()
        self.tableList.column("#0",width=columnWidth)
        self.tableList.column("name", width=columnWidth)
        self.tableList.column("minprice", width=columnWidth)
        self.tableList.column("maxprice", width=columnWidth)
        self.tableList.column("curprice", width=columnWidth)
        self.tableList.column("gap", width=columnWidth)

        self.tableList.heading('name', text='名字')
        self.tableList.heading('minprice', text='最小')
        self.tableList.heading('maxprice', text='最大')
        self.tableList.heading('curprice', text='当前')
        self.tableList.heading('gap', text='涨跌')

        path = os.getcwd()
        self.databaseFilePath = path + "/databasefile/"


    def selectDataSlot(self):
        selectSql = "select name,minprice,maxprice,curprice,gap from stock where state=?"

        filePath = self.databaseFilePath + "stock.db"
        connectstate = sqlite3.connect(filePath)
        cur = connectstate.cursor()

        try:
            cur.execute(selectSql,(self.stateEntry.get(),))
            resultAll = cur.fetchall()
            self.addData(resultAll)
            #print(resultAll)

        except Exception as e:
            print("查询数据库失败!!!!!!!")
        finally:
            cur.close()
            connectstate.close()


    def addData(self,dataList):
        self.clearItem()

        index = 0
        for data in dataList:
            #print(data[0],data[1],data[2],data[3])
            self.tableList.insert("",index,values=(data[0],data[1],data[2],data[3],data[4]))
            index += 1


    def clearItem(self):
        itemlist = self.tableList.get_children()
        for item in itemlist:
            self.tableList.delete(item)

    def setSystem(self,name):
        self.strVar.set(name)