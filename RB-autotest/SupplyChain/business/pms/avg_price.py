"""
Created on 2019/3/13
@author: liya
"""
import pymysql
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from business.BasePage import Base


class Pms_Avg_Price(Base):

    def avg_price(self):

        conn = pymysql.connect(host = 'mysql.test.yiyaowang.com',  # 远程主机的ip地址，
                                            user = 'yao',   # MySQL用户名
                                            db = 'yao',   # database名
                                            passwd = 'd41d8cd98f00b204',   # 数据库密码
                                            port = 3306,  #数据库监听端口，默认3306
                                            charset = "utf8")  #指定utf8编码的连接
        print('PMS数据库:连接成功')
        cursor = conn.cursor()  # 创建一个光标，然后通过光标执行sql语句

        sql = """
        SELECT
        	warehouse_id,
        	changed_qty,
        	current_in_price,
        	current_qty,
    	current_avg_price,
        after_avg_price,
        doc_detail_id,
        reason_note,
        create_time
        FROM
            item_avg_price_log
        WHERE
            product_id = '54367962'
        ORDER BY
            id desc;
        """
        cursor.execute(sql)
        data = cursor.fetchall()  # 取出cursor得到的数据
        print('最新平均价日志：\n' + str(data[0]))
        print('当前商品仓库：%d' % (data[0][0]))
        print('变更库存数量：%d' % (data[0][1]))
        print('进来平均价：%f' % (data[0][2]))
        print('当前库存：%d'  % (data[0][3]))
        print('当前平均价：%f' % (data[0][4]))
        changed_avg_price = float((data[0][1]*data[0][2]+data[0][3]*data[0][4])/(data[0][1]+data[0][3]))
        print('计算后的平均价：%f' % (changed_avg_price))
        print('变更后的平均价：%f' % (data[0][5]))  # 此值，用来对比计算的平均价是否准确

        print('将查询的数据保存到pms_avg_price.txt文件中')
        doc = open('pms_avg_price.txt', 'w')
        print('%f' % (changed_avg_price), file=doc)
        # print('计算后的平均价：%f' % (changed_avg_price))
        doc.close()
        doc = open('pms_avg_price.txt', 'a')
        print(data[0][5], file=doc)
        doc.close()
        # assert float(changed_avg_price) == float(values[0][5])
        cursor.close()
        conn.close()  #最后记得关闭光标和连接，防止数据泄露


    def assert_avg_price(self):
        """校验计算平均价与数据库中算的是否一致"""
        f = open('pms_avg_price.txt', 'r')
        str1 = f.readline()
        print("读取整行内容：", str1)
        str3 = f.readline()
        print("读取剩下内容：", str3)
        if (str1[0]) > (str3[0]):
            assert print('计算平均价 > 数据库中平均价')
        elif (str1[0]) < (str3[0]):
            assert print('计算平均价 < 数据库中平均价')
        else:
            print('计算平均价 = 数据库中平均价')
        f.close()

    def clear_file(self,file):
        print('清空文件内容')
        doc = open(file, 'w')  #file--'pms_avg_price.txt'
        doc.truncate()