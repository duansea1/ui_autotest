# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年3月月09日 12:10
# ---

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
    list = ('3531619', '3531624', '3531638', '3531642', '3531653', '3531658', '3531662', '3531669', '3527113', '3532804', '3534701', '3534721', '3534724', '3534725', '3534739', '3534754', '3534761', '3535906', '3535883', '3535887', '3540168', '3538608', '3540180', '3540137', '3540203', '3540921', '3541563', '3537864', '3542053', '3543998', '3545825', '3545841', '3094944', '3554116', '3564491', '3572183', '3572204', '3577004', '3590480', '3597761', '2577122', '3604260', '3606087', '3606300', '3606321', '3606325', '3606332', '3606341', '3606344', '3606346', '3606354', '3606379', '3606381', '3606385', '3606420', '3606432', '3606436', '3606444', '3606450', '3606459', '3606478', '3606479', '3606485', '3606494', '3606505', '3606517', '3606524', '3606529', '3606534', '3606539', '3606546', '3606587', '3606589', '3606595', '3606607', '3606632', '3606638', '3606642', '3606648', '3606668', '3606671', '3606673', '3606681', '3606683', '3606728', '3606741', '3606744', '3606748', '3608186', '3610883', '3610904', '3615702', '2573192', '3619019', '3619020', '3619030', '3619116', '3619148', '3619151', '3619159', '3619189', '3619251', '3619273', '3619357', '3619360', '3619390', '3619401', '3619461', '3619475', '3619477', '3619494', '3619510', '3619511', '3619526', '3619545', '3619626', '3619629', '3619630', '3619632', '3619634', '3619639', '3619640', '3619641', '3619642', '3619643', '3619644', '3619649', '3619652', '3619654', '3619655', '3619656', '3619661', '3619662', '3619664', '3619665', '3619666', '3619669', '3619674', '3619675', '3619681', '3619682', '3619683', '3619686', '3619691', '3619692', '3619693', '3619694', '3619697', '3619698', '3619699', '3619701', '3619702', '3619704', '3619705', '3619707', '3619708', '3619710', '3619712', '3619713', '3619714', '3619715', '3619716', '3619718', '3619719', '3619720', '3619725', '3619727', '3619728', '3619729', '3619730', '3619731', '3619734', '3619736', '3619737', '3619738', '3619740', '3619741', '3619742', '3619744', '3619746', '3619748', '3619750', '3619751', '3619755', '3619758', '3619760', '3619761', '3619764', '3619770', '3619771', '3619772', '3619777', '3619779', '3619782', '3619785', '3619787', '3619788', '3619789', '3619792', '3619793')
    print(len(list))

