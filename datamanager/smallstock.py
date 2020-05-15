
import os
import urllib.request
import sqlite3
from multiprocessing import Process
import multiprocessing
import requests

#requesturl = "http://hq.sinajs.cn/list=s_sh"
requesturl = "http://qt.gtimg.cn/q=s_sz00"
import os
import configparser


class SmallStock:

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

    def getNumStr(self,number):
        strTp = ""
        if number < 10:
            strTp = "000" + str(number)
        elif (number >= 10) and (number < 100):
            strTp = "00" + str(number)
        elif (number >= 100) and (number < 1000):
            strTp = "0" + str(number)
        else:
            strTp = str(number)

        return strTp



    def excute(self):
        self.progressValue = multiprocessing.Value("i", 1)
        self.progressObject = multiprocessing.Process(target=self.requestData,args=(self.progressValue,))
        self.progressObject.start()

    def requestData(self, valuePt):
        self.openDatabase()

        cur_path = os.path.dirname(os.path.realpath(__file__))
        config_path = cur_path + "/config/stock.ini"
        conf = configparser.ConfigParser()
        conf.read(config_path)
        startID = conf.getint("stockid","small")

        if startID >= 10000 :
            print("obtain small stock restart new query")
            startID = 0

        print("obtain small stock start codename=",startID)


        while valuePt.value and (startID < 10000) :
            url = requesturl + self.getNumStr(startID)
            #print(url)
            req = requests.get(url=url)
            #print(req.content)
            self.parseData(req.content, startID)

            #req = urllib.request.urlopen(url)
            #self.parseData(req.read(),startID)

            startID += 1

        conf.set("stockid","small",str(startID))
        with open(config_path, 'w') as fw:
            conf.write(fw)

        print("request all small stock is finished!!!!!!!!!")
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

        strTemp = "sz00" + self.getNumStr(stockId)
        state = self.getStocExist(strTemp)
        if state:
            updateSql = "update stock set name=?,curprice=?,gap=? where codename=?"
            self.cur.execute(updateSql,(dataList[1],dataList[3],dataList[4],strTemp))
            self.connect.commit()
        else:
            insertSql = "insert into stock(name,codename,curprice,gap) values(?,?,?,?)"
            self.cur.execute(insertSql,(dataList[1],strTemp,dataList[3],dataList[4]))
            self.connect.commit()



    def getStocExist(self,codeId):
        sql = "select name from stock where codename=?"
        self.cur.execute(sql, (codeId,))
        resultAll = self.cur.fetchone()
        #print(resultAll[0])
        if resultAll:
            print("select stock name is exist,codename=",codeId)
            return True
        else:
            return False


    def setExecuteState(self,flag):
        self.progressValue.value = 0
        self.progressObject.join()