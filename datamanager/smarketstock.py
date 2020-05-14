
import os
import urllib.request
import sqlite3
from multiprocessing import Process
import multiprocessing
import requests

#requesturl = "http://hq.sinajs.cn/list=s_sz"
requesturl = "http://qt.gtimg.cn/q=s_sz"


class SmarketStock:

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

        startID = 300000

        while valuePt.value and (startID < 301000) :
            url = requesturl + str(startID)
            #print(url)
            req = requests.get(url=url)
            #print(req.content)
            self.parseData(req.content, startID)

            #req = urllib.request.urlopen(url)
            #self.parseData(req.read(),startID)

            startID += 1

        print("request all smarket stock is finished!!!!!!!!!")
        self.cur.close()
        self.connect.close()


    def parseData(self,data,stockId):
        #print(data)
        tempData = data.decode("GBK")
        #print(tempData)

        datalist = tempData.split("~")
        self.insertData(datalist,stockId)


    def insertData(self,dataList,stockId):
        #print(dataList)
        if len(dataList) < 3:
            return
        grice = float(dataList[3])
        if grice < 6:
            return

        strTemp = "sz" + str(stockId)
        state = self.getStocExist(strTemp)
        if state:
            updateSql = "update smarket set name=?,curprice=?,gap=? where codename=?"
            self.cur.execute(updateSql,(dataList[1],dataList[3],dataList[4],strTemp))
            self.connect.commit()
        else:
            insertSql = "insert into smarket(name,codename,curprice,gap) values(?,?,?,?)"
            self.cur.execute(insertSql,(dataList[1],strTemp,dataList[3],dataList[4]))
            self.connect.commit()



    def getStocExist(self,codeId):
        sql = "select name from smarket where codename=?"
        self.cur.execute(sql, (codeId,))
        resultAll = self.cur.fetchone()
        #print(resultAll[0])
        if resultAll:
            print("select smarket name is exist,codename=",codeId)
            return True
        else:
            return False


    def setExecuteState(self,flag):
        self.progressValue.value = 0
        self.progressObject.join()