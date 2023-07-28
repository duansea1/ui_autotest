# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年3月月08日 19:20
# ---
<<<<<<< HEAD

from datetime import datetime, date

"""给定一组订单，计算下单之间的时间差"""

time1 = '2017-07-17 06:03:00'
time2 = '2020-07-17 06:03:00'

# 把日期字符串 转换为日期格式（把日期格式装换为字符串格式datetime.strftime）
time1_struct = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
print('转换为时间格式：',time1_struct)
time2_struct = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")
# sends = (time2_struct - time1_struct).seconds  # 同一天之内的时间差-秒
sends = (time2_struct - time1_struct).total_seconds()  # 不同天之内的时间差-秒

print("时间间隔-秒/单位", sends)


"""只有时间time,没有日期时，求时间差先加上一个相同的日期，再求时间差"""

t1 = "08:00:00"
t2 = "09:00:00"

t1_struct = datetime.strptime(t1, '%H:%M:%S')
t2_struct = datetime.strptime(t2, '%H:%M:%S')
t_sub = datetime.combine(date.min, t2_struct.time()) -datetime.combine(date.min, t1_struct.time())
print("------------与最小日期组合--------")
print(t_sub.seconds/60)


time_sub = datetime.combine(date.today(), t2_struct.time()) -datetime.combine(date.today(), t1_struct.time())
print("------------与当天日期组合--------")
print(time_sub.seconds/60)
print(time_sub.total_seconds()/60)


=======
>>>>>>> 5210fa1b7715b51962a03b38b5322cac1dc97b6c
