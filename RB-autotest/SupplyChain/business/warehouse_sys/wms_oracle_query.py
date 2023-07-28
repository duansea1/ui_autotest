"""
Created on 2019/3/9
@author: liya
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from business.BasePage import Base
from business.warehouse_sys import outbound_resource as R
import cx_Oracle

class  Wms_Oracle(Base):

    def wms_oracle_query(self):
        db = cx_Oracle.connect('WMS_SH_YW', 'WMS_SH_YW', '10.6.84.20:1521/WMSOracle')
          # # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
        print('WMS-Oracle数据库:连接成功')

        cursor = db.cursor()
        sql = """
        SELECT 	b.DO_NO,	b.PLAN_SHIP_TIME,	b.CARRIER_ID,	A .TRACKING_NO 
        FROM	doc_do_wave_ex A INNER JOIN DOC_DO_HEADER b ON A .DO_H_ID = b. ID 
        WHERE	b.do_no = 'CSXGCYSWD'
        """
        # oracle数据库查询sql语句，最后不带分号

        cursor.execute(sql)
        data = cursor.fetchone()
        print('DO单：' + data[0])
        print('预计出库时间：' + str(data[1]))
        print('承运商ID：' + str(data[2]))
        print('运单号：' + str(data[3]))

        print('将查询的数据保存到wms_do_carrier.txt文件中')
        doc = open('wms_do_carrier.txt', 'a')
        print(data[1], file=doc)
        print(data[2], file=doc)
        print(data[3], file=doc)
        doc.close()
        cursor.close()

    def assert_do_carrier(self):
        """校验do单中的承运商信息是否变更"""
        f = open('wms_do_carrier.txt', 'r')
        str1  = f.readline()
        print("读取第一行内容：", str1 )
        str2 = f.readline()
        print("读取第二行剩下内容：", str2)
        str3 = f.readline()
        print("读取第三行剩下内容：", str3)
        str4 = f.readline()
        print("读取第四行剩下内容：", str4)
        str5 = f.readline()
        print("读取第五行剩下内容：", str5)
        str6 = f.readline()
        print("读取第六行剩下内容：", str6)

        assert str1 != str4 and str1 != 'null' and str4 != 'null'
        print('预计出库时间变更-成功')
        assert str2 != str5
        print('承运商ID变更-成功')

        for i in str3:
            print(i)
        for j in str6:
            print(j)
        print(str3,str6,type(str6),type(str3),len(str3),len(str6))
        assert str3 != str6  or len(str3)==len(str6)==5  #测试环境运单号可能获取不到为 None

        print('运单号变更-成功')
        f.close()

    def clear_file(self,file):
        print('清空文件内容')
        doc = open(file, 'w')  #file--'wms_do_carrier.txt'
        doc.truncate()
        doc.close()

