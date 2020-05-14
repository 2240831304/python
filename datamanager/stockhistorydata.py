
import os
import urllib.request
import sqlite3
from multiprocessing import Process
import multiprocessing


requesturl = "http://hq.sinajs.cn/list="


class StockHistoryData:
    def __init__(self):
        self.executeId = 1
        self.state = True

        self.connect = None
        self.cur = None
        self.databaseFilePath = ""
        self.progressObject = None
        self.progressValue = None
        self.maxID = 0


    def openDatabase(self):
        path = os.getcwd()
        self.databaseFilePath = path + "/databasefile/stock.db"

        self.connect = sqlite3.connect(self.databaseFilePath)
        self.cur = self.connect.cursor()


    def excute(self):
        self.progressValue = multiprocessing.Value("i",1)
        self.progressObject = multiprocessing.Process(target=self.requestData,args=(self.progressValue,))
        self.progressObject.start()


    def requestData(self,valuePt):
        self.openDatabase()
        self.maxID = int(self.getMaxID())
        print(self.maxID)
        #print(valuePt.value)

        while valuePt.value :
            if self.executeId > self.maxID :
                self.executeId = 1
                print("stockhistorydata.py requestData  is finished!!!!!!!!")
                break

            codename = self.getStockNum(self.executeId)

            if codename == "" :
                self.executeId += 1
                continue
            url = requesturl + str(codename)
            #print(url)
            req = urllib.request.urlopen(url)

            self.parseData(req.read())
            self.executeId += 1

        self.cur.close()
        self.connect.close()


    def parseData(self,data):

        tempData = data.decode("utf8","ignore")
        #print(tempData)

        datalist = tempData.split(",")
        #print(datalist[3])
        self.insertData(datalist[3],datalist[2])


    def insertData(self,price,yesterdayprice):
        gapnum = float(price) - float(yesterdayprice)
        gapnum = '%.2f' % gapnum
        sql = "update stock set curprice=?,gap=?,state=? where id=?"
        self.cur.execute(sql, (price,gapnum,1, self.executeId))
        self.connect.commit()


    def getStockNum(self,codeId):
        sql = "select codename from stock where id=?"
        self.cur.execute(sql, (codeId,))
        resultAll = self.cur.fetchone()
        #print(resultAll[0])
        if resultAll:
            return resultAll[0]
        else:
            return ""

    def setExecuteState(self,flag):
        self.state = flag
        self.progressValue.value = 0
        self.progressObject.join()


    def getMaxID(self):
        sql = "select max(id) from stock"
        self.cur.execute(sql)
        result = self.cur.fetchone()

        return result[0]