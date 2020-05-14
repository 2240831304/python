
import os
import urllib.request
import sqlite3
from multiprocessing import Process
import multiprocessing
import json


#requesturl = "http://hq.sinajs.cn/list="
requesturl = "http://q.stock.sohu.com/hisHq?code=cn_%s&start=20190501&end=20200514&stat=0&order=D&period=m"


class StockHistoryData:
    def __init__(self):
        self.executeId = 1
        self.curExcuteCodeName = ""
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

            self.curExcuteCodeName = codename
            codename = codename.replace("sh","")
            codename = codename.replace("sz", "")
            url = requesturl % (codename)
            #print(url)

            req = urllib.request.urlopen(url)
            #print(req.headers)
            self.parseData(req.read())

            self.executeId += 1

        self.cur.close()
        self.connect.close()


    def parseData(self,data):
        tempData = data.decode("utf8","ignore")
        tempData = tempData.replace("\n","")
        strToListData = eval(tempData)
        dictData = strToListData[0]
        needData = dictData["hq"]
        # print(needData)

        #['2020-05-14', '16.63', '18.15', '1.42', '8.49%', '16.62', '18.50', '307022', '54609.15', '0.15%']
        weekMin = 0
        weekMax = 0
        weekGap = 0
        yearMinPrice = 0
        yearMaxPrice = 0
        firstListData = needData[0]
        weekGap = firstListData[3]
        weekMin = firstListData[5]
        weekMax = firstListData[6]
        yearMinPrice = firstListData[5]
        yearMaxPrice = firstListData[6]

        for value in needData:
            if yearMinPrice > value[5]:
                yearMinPrice = value[5]

            if yearMaxPrice < value[6]:
                yearMaxPrice = value[6]

        listData = list()
        listData.append(yearMinPrice)
        listData.append(yearMaxPrice)
        listData.append(weekMin)
        listData.append(weekMax)
        listData.append(weekGap)

        self.updateData(listData)


    def updateData(self,dataPt):
        #print(dataPt)
        updatesql = "update stock set minprice=?,maxprice=? where codename=?"
        self.cur.execute(updatesql,(dataPt[0],dataPt[1],self.curExcuteCodeName))
        self.connect.commit()
        self.curExcuteCodeName = ""


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