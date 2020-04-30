
from tkinter import *
import sqlite3
import os


class CreateDataBaseWindow(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.databaseFilePath = ""

        self.init_window()


    def init_window(self):
        self.master.title("创建数据库")
        self.pack(fill=BOTH, expand=1)


        databaseLabel = Label(self, text="库名")
        databaseLabel.grid(row=0,column=0)

        databaseEntry = Entry(self)
        databaseEntry.grid(row=0, column=1)

        createDataBaseBut = Button(self,text="建设库",command=self.createDatabase)
        createDataBaseBut.grid(row=1,column=0,sticky=W)

        tableLabel = Label(self, text="表名")
        tableLabel.grid(row=0,column=2)

        tableEntry = Entry(self)
        tableEntry.grid(row=0,column=3)


        createTableBut = Button(self,text="建设表",command=self.createTable)
        createTableBut.grid(row=1,column=1,sticky=E)




    def createDatabase(self):
        #如果数据库不存在就会创建新的数据库

        path = os.getcwd()
        self.databaseFilePath = path + "/databasefile/stock.db"

        print("createDatabase=",self.databaseFilePath)
        connectstate = sqlite3.connect(self.databaseFilePath)
        connectstate.close()


    def createTable(self):
        print("fffffffffffffffffff")