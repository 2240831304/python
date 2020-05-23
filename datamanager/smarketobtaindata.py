
import os
import urllib.request
import sqlite3
from multiprocessing import Process
import multiprocessing


requesturl = "http://hq.sinajs.cn/list="


class SmarketObtainData:
    def __init__(self):
        self.executeId = 1
        self.state = True

        self.connect = None
        self.cur = None
        self.databaseFilePath = ""
        self.progressObject = None
        self.progressValue = None
        self.maxID = 0

        self.curminPrice = 0
        self.curMaxPrice = 0
        self.curState = 0

    def openDatabase(self):
        path = os.getcwd()
        self.databaseFilePath = path + "/databasefile/stock.db"

        self.connect = sqlite3.connect(self.databaseFilePath)
        self.cur = self.connect.cursor()


    def execute(self):
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
                print("smarketobtaindata.py  requestData finished!!!!!!!!")
                continue

            codename = self.getStockNum(self.executeId)

            if codename == "" :
                self.executeId += 1
                continue

            print("smarketobtaindata.py requestData current executeId==", self.executeId)
            url = requesturl + str(codename)
            #print(url)
            req = urllib.request.urlopen(url)

            self.parseData(req.read())
            self.executeId += 1

        print("obatin smarket stock query price is finished!!!!")
        self.cur.close()
        self.connect.close()


    def parseData(self,data):

        tempData = data.decode("utf8","ignore")
        #print(tempData)

        try:
            datalist = tempData.split(",")
            #print(datalist[3])
            self.insertData(datalist[3],datalist[2])
        except:
            print("smarket stock get often data is encounter error,id=", self.executeId)


    def getStockNum(self,codeId):
        sql = "select codename,minprice,maxprice,state from smarket where id=?"
        self.cur.execute(sql, (codeId,))
        resultAll = self.cur.fetchone()
        try:
            self.curminPrice = float(resultAll[1])
            self.curMaxPrice = float(resultAll[2])
            self.curState = int(resultAll[3])
        except:
            self.curminPrice = 0
            self.curMaxPrice = 0
            self.curState = 1
        # print(resultAll)

        if resultAll:
            return resultAll[0]
        else:
            return ""


    def insertData(self,price,yesterdayprice):
        gapnum = float(price) - float(yesterdayprice)
        gapnum = '%.2f' % gapnum

        curPriceTemp = float(price)
        if self.curState >= 7:
            self.curState = self.curState
        else:
            onePrice = (self.curMaxPrice - self.curminPrice) / 4
            onefourth = self.curminPrice + onePrice
            twofourth = self.curminPrice + onePrice * 2
            threefourth = self.curminPrice + onePrice * 3
            if curPriceTemp <= onefourth:
                self.curState = 1
            elif (curPriceTemp > onefourth) and (curPriceTemp <= twofourth):
                self.curState = 2
            elif (curPriceTemp > twofourth) and (curPriceTemp <= threefourth):
                self.curState = 3
            else:
                self.curState = 4

        sql = "update smarket set curprice=?,gap=?,state=? where id=?"
        self.cur.execute(sql, (price,gapnum,self.curState, self.executeId))
        self.connect.commit()


    def setExecuteState(self,flag):
        self.state = flag
        self.progressValue.value = 0
        self.progressObject.join()


    def getMaxID(self):
        sql = "select max(id) from smarket"
        self.cur.execute(sql)
        result = self.cur.fetchone()

        return result[0]