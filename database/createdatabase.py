
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




    def createDatabase(self):
        #如果数据库不存在就会创建新的数据库

        path = os.getcwd()
        self.databaseFilePath = path + "/databasefile/stock.db"
        
        print("createDatabase=",self.databaseFilePath)
        connectstate = sqlite3.connect(self.databaseFilePath)
        connectstate.close()


