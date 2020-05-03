
from tkinter import *
import sqlite3
import os


class InsertShareWindow(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.databaseFilePath = ""

        self.nameEntry = ""
        self.codenameEntry = ""
        self.minpriceEntry = 0
        self.maxpriceEntry = 0

        self.init_window()


    def init_window(self):
        self.master.title("创建数据库")
        self.pack(fill=BOTH, expand=1)

        name = Label(self,text="股票名字")
        name.grid(row=0,column=0)
        self.nameEntry = Entry(self)
        self.nameEntry.grid(row=0,column=1)

        codename = Label(self,text="股票代码")
        codename.grid(row=1,column=0)
        self.codenameEntry = Entry(self)
        self.codenameEntry.grid(row=1,column=1)

        minprice = Label(self,text="最小价格")
        minprice.grid(row=2,column=0)
        self.minpriceEntry = Entry(self)
        self.minpriceEntry.grid(row=2,column=1)

        maxprice = Label(self,text="最小价格")
        maxprice.grid(row=3,column=0)
        self.maxpriceEntry = Entry(self)
        self.maxpriceEntry.grid(row=3,column=1)

        insertDataBut = Button(self,text="添加数据",command=self.insertDataSlot)
        insertDataBut.grid(row=4,column=0,sticky=E)

        path = os.getcwd()
        self.databaseFilePath = path + "/databasefile/"


    def insertDataSlot(self):

        insertSql = "insert into stock(name,codename,minprice,maxprice) values(?,?,?,?)"
        selectSql = "select * from stock where codename=?"

        filePath = self.databaseFilePath + "stock.db"
        connectstate = sqlite3.connect(filePath)
        cur = connectstate.cursor()

        IsNeedInsertData = True

        try:
            cur.execute(selectSql,(self.codenameEntry.get(),))
            resultAll = cur.fetchall()
            if resultAll :
                IsNeedInsertData = False
                print("insert share stock data ,data is exist=true!!")

        except Exception as e:
            print(e)
            print('查询数据库失败')
        finally:
            pass

        if IsNeedInsertData :
            cur.execute(insertSql,(self.nameEntry.get(),self.codenameEntry.get(),
                                   self.minpriceEntry.get(),self.maxpriceEntry.get()))
            connectstate.commit()

        # 关闭游标
        cur.close()
        # 关闭连接
        connectstate.close()
