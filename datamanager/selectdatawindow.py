
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

        self.init_window()


    def init_window(self):
        self.master.title("查询数据")
        self.pack(fill=BOTH, expand=1)

        name = Label(self,text="股票状态")
        name.grid(row=0,column=0)
        self.stateEntry = Entry(self)
        self.stateEntry.grid(row=0,column=1)

        selectBut = Button(self, text="查询数据", command=self.selectDataSlot)
        selectBut.grid(row=1, column=0, sticky=E)

        self.tableList = ttk.Treeview(self)
        self.tableList.grid(row=2)
        self.tableList['columns'] = ['name','minprice','maxprice','curprice']
        #self.tableList.pack()
        self.tableList.column("name", width=50)
        self.tableList.column("minprice", width=50)
        self.tableList.column("maxprice", width=50)
        self.tableList.column("curprice", width=50)

        self.tableList.heading('name', text='股票名字')
        self.tableList.heading('minprice', text='最小价格')
        self.tableList.heading('maxprice', text='最大价格')
        self.tableList.heading('curprice', text='当前价格')

        path = os.getcwd()
        self.databaseFilePath = path + "/databasefile/"


    def selectDataSlot(self):
        selectSql = "select name,minprice,maxprice,curprice from stock where state=?"

        filePath = self.databaseFilePath + "stock.db"
        connectstate = sqlite3.connect(filePath)
        cur = connectstate.cursor()

        try:
            cur.execute(selectSql,(self.stateEntry.get(),))
            resultAll = cur.fetchall()

        except Exception as e:
            print("查询数据库失败!!!!!!!")
        finally:
            cur.close()
            connectstate.close()