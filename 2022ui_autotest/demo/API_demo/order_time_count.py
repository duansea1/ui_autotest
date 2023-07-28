# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年3月月09日 12:10
# ---
<<<<<<< HEAD
from datetime import datetime, date
import math
from commons.mysql_ops import *
import json, requests

# 数据库-商城
DB = {"host": "zw-db-testing.mysql.polardb.rds.aliyuncs.com", "user": "crm", "password": "JWW4zud0",
      "port": 3306, "data": "zw_shop"}
sql = "select DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') from zw_order where  `tenant_id` = 56 and `shop_id` = 17063  and buyer_uid=77 and order_status = 9 order by created_at ASC limit 3;"


class Ordertime():

    def timestuct(self, *args, times):
        """
        :param args:
        :param times: 字符串的日期数组 ：字符串的日期格式为：'2017-07-17 06:03:00'
        :return: 返回转换为日期格式的日期列表数据
        """
        times_struct = []
        for i in times:
            timei_struct = datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
            print(timei_struct)
            times_struct.append(timei_struct)
        return times_struct

    def seconds_day_hms(self, seconds: int):
        """时间单位：秒"""
        # 分钟，秒
        m, s = divmod(seconds, 60)
        # 时， 分
        h, m = divmod(m, 60)
        # 天， 时
        d, h = divmod(h, 24)
        print(f"下单时间频次：{d}天{h}时{m}分{s}秒")
        return d, h, m, s

    def sum_time(self, datetimes, flag='s'):
        """
        :datetimes:字符串日期
        :flag:h-小时 m--分钟 s--秒
        :return:
        """
        times_c = []
        for n in range(len(datetimes) - 1):  # 循环遍历，求出相邻时间差
            time_c = (datetime.strptime(datetimes[n + 1], "%Y-%m-%d %H:%M:%S")
                      - datetime.strptime(datetimes[n], "%Y-%m-%d %H:%M:%S")).total_seconds()
            times_c.append(time_c)
        print('按时间排序，计算出相邻时间之差列表：', times_c)
        total_seconds = math.fsum(times_c)
        # 计算平均下单的频次总时间-单位秒
        sum_seconds = total_seconds / (len(datetimes) - 1)
        # 将下单的频次时差，换算成天、时、分、秒
        self.seconds_day_hms(seconds=int(sum_seconds))

    def query_order(self, DB: object = DB, SQL: object = sql) -> object:
        """

        :param DB: 数据库信息
        :param SQL: 查询sql
        :return: 返回查到的数据
        """
        result = query_mysql(DB['host'], DB['user'], DB['password'], DB['port'], DB['data'], sql=SQL)
        data = list(result['data'])
        timeList = []
        for i in data:
            timeList.append(i[0])
        print('获取指定信息：', timeList)
        return timeList


if __name__ == "__main__":
    # times = ['2017-07-17 06:03:00', '2017-07-17 06:05:00', '2017-07-18 06:03:00']
    Ordert = Ordertime()
    # 查询符合条件的订单创建时间
    ordertimes = Ordert.query_order()
    Ordert.sum_time(datetimes=ordertimes)
=======
>>>>>>> 5210fa1b7715b51962a03b38b5322cac1dc97b6c
