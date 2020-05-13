
import os
import urllib.request
import sqlite3
from multiprocessing import Process
import multiprocessing


requesturl = "http://hq.sinajs.cn/list=sh"


class ShangHaiStock:

    def __init__(self):
        self.progressObject = None
        self.connect = None
        self.cur = None
        self.databaseFilePath = ""
        self.progressValue = None


    def openDatabase(self):
        path = os.getcwd()
        self.databaseFilePath = path + "/databasefile/stock.db"

        self.connect = sqlite3.connect(self.databaseFilePath)
        self.cur = self.connect.cursor()


    def excute(self):
        self.progressValue = multiprocessing.Value("i", 1)
        self.progressObject = multiprocessing.Process(target=self.requestData,args=(self.progressValue,))
        self.progressObject.start()

    def requestData(self, valuePt):
        self.openDatabase()

        startID = 600000

        while valuePt.value and (startID < 610000) :
            url = requesturl + str(startID)
            #print(url)
            req = urllib.request.urlopen(url)
            self.parseData(req.read())

            startID += 1

        self.cur.close()
        self.connect.close()


    def reuqestData(self,stockId):
        url = requesturl + str(stockId)
        print(url)
        req = urllib.request.urlopen(url)

        if req.read() == "":
            print("request stock is not exist,id=",stockId)
            return
        self.parseData(req.read())


    def parseData(self,data):
        tempData = data.decode("utf8","ignore")
        #print(tempData)

        datalist = tempData.split(",")
        self.insertData(datalist)


    def insertData(self,dataList):
        print(dataList)


    def setExecuteState(self,flag):
        self.progressValue.value = 0
        self.progressObject.join()