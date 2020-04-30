
from tkinter import *


class MainWindow(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master

        self.init_window()


    def init_window(self):
        self.master.title("慧宝宝要学习")
        self.pack(fill=BOTH,expand=1)

        createDataBaseBut = Button(self,text="创建数据库",command=self.createDatabaseSLot)
        createDataBaseBut.place(x=10,y=10)


    def createDatabaseSLot(self):
        print("mainwindow createDatabaseSLot start create database!")