import pandas as pd
from flask import Flask, render_template
import pandas
import pymysql
import MyEnDecryption

class DB:
    def __init__(self):
        account = MyEnDecryption.decrypt_account('mysqlUser','userAcount')
        self.db_con = pymysql.connect(
                user=account[0],
                passwd=account[1],
                host='localhost',
                db='flask_db',
                charset='utf8'
                    )
        self.cursor = self.db_con.cursor(pymysql.cursors.DictCursor)
        #self.insert_df = None
        self.select_df = "SELECT * FROM dailycount "
        self.select_df_userInfo = "SELECT * FROM usertable "
        #self.commit_result = None

    def insertSiteCount(self,page,cnt):
        sql = "UPDATE dailycount SET day='"+page+"',count='"+cnt+"' where day='"+page+"'"
        self.cursor.execute(sql)
        self.db_con.commit()

    def getData(self,page):
        sql = self.select_df
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        countDF = pd.DataFrame(result)
        main = countDF[countDF['day'] == page]
        countR=int(main['count'])
        return countR
    def mainLogin(self):
        sql = self.select_df
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        countDF = pd.DataFrame(result)
        countList = {"MAIN": 0, "cht": 0, "idx2": 0, "dff": 0, "mysql": 0}
        for index, row in countDF.iterrows():
            temp = countDF[countDF['day'] == countDF['day'][index]]
            r = int(temp['count'].iloc[0])
            countList[countDF['day'][index]] = r
        return countList

    def getSample(self,day):
        ret = []

        sql = self.select_df

        if day !='':
            sql += f" where day ='{day}'"
        self.cursor.execute(sql)

        rows = self.cursor.fetchall()
        for e in rows:
            temp = {'day': e['day'], 'count': e['count']}
            ret.append(temp)

        return ret

    def insertSite(self,day : str,cnt : int):
        sql = '''insert into dailycount (day, count) values(%s,%s)'''
        affected_rows = self.cursor.execute(sql,(day, cnt))
        self.db_con.commit()
        return affected_rows

    def deleteType(self, day: str):
        sql = "delete from dailycount where day = %s"
        affected_rows = self.cursor.execute(sql,day)
        self.db_con.commit()
        return affected_rows

    def getSampleUserInfo(self,name):
        ret = []

        sql = self.select_df_userInfo

        if name !='':
            sql += f" where name ='{name}'"
        self.cursor.execute(sql)

        rows = self.cursor.fetchall()
        for e in rows:
            temp = {'name': e['name'], 'location': e['location'], 'badge': e['badge']}
            ret.append(temp)
        if len(ret)==0 :
            temp = {'name': 'None', 'location': 'NonData' }
            ret.append(temp)
        return ret

    def __del__(self):
        self.db_con.close()
        self.cursor.close()
