# -*- coding: utf-8 -*-
#开发人员:   
#开发日期:   
#文件项目:   
#文件名称:
#import mysql.connector
import pymysql
import random
class TMS_mysql():
    def sql_excute(sql,parameter):
        mydb = pymysql.connect(
                host="10.6.84.20",
                user="tms",
                passwd="d41d8cd98f00b204",
                database="tms",
        )
        mycursor = mydb.cursor()
        #sql="SELECT GROUP_CONCAT(code)list from tms_carrier where `name`=%s;"
        mycursor.execute(sql,(parameter,))
        print('sql执行成功')
        #mycursor.execute(sql)
        mydb.commit()
        print('执行结果已提交')
        # myresult = mycursor.fetchall()
        # print(myresult,type(myresult))
        # b=myresult[0]
        # a = ','.join(b)
        # print(a,type(a))


