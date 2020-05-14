
from tkinter import *
import sqlite3
import os


class CreateDataBaseWindow(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.databaseFilePath = ""
        self.tableEntry = None
        self.databaseEntry = None

        self.fieldEntry = None

        self.init_window()


    def init_window(self):
        self.master.title("创建数据库")
        self.pack(fill=BOTH, expand=1)


        databaseLabel = Label(self, text="库名")
        databaseLabel.grid(row=0,column=0)

        self.databaseEntry = Entry(self)
        self.databaseEntry.grid(row=0, column=1)

        createDataBaseBut = Button(self,text="建设库",command=self.createDatabase)
        createDataBaseBut.grid(row=1,column=0,sticky=W)

        tableLabel = Label(self, text="表名")
        tableLabel.grid(row=0,column=2)

        self.tableEntry = Entry(self)
        self.tableEntry.grid(row=0,column=3)

        createTableBut = Button(self,text="建设表",command=self.createTable)
        createTableBut.grid(row=1,column=1,sticky=E)

        path = os.getcwd()
        self.databaseFilePath = path + "/databasefile/"


    def createDatabase(self):
        #如果数据库不存在就会创建新的数据库

        if self.databaseEntry.get() == "":
            print("input database name is null!!!!!!!!")
            return

        filePath = self.databaseFilePath  + self.databaseEntry.get() + ".db"

        print("createDatabase=",filePath)
        connectstate = sqlite3.connect(filePath)
        connectstate.close()


    def createTable(self):

        if self.tableEntry.get() == "":
            print("input table name is null!!!!!!!!")
            return

        filePath = self.databaseFilePath  + "stock.db"
        print("database filepath =",filePath)

        sql = "create table " + self.tableEntry.get()
        sql += "(id INTEGER PRIMARY KEY  AUTOINCREMENT ,name varchar(20)," \
              "codename varchar(10),minprice INTEGER,maxprice INTEGER,curprice INTEGER,gap INTEGER,state INTEGER," \
              "weekmin INTEGER,weekmax INTEGER,weekgap INTEGER)"

        connectstate = sqlite3.connect(filePath)
        cur = connectstate.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            print('创建表失败')
        finally:
            pass

        # 关闭游标
        cur.close()
        # 关闭连接
        connectstate.close()