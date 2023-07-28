# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年3月月13日 20:02
# ---

from datetime import datetime
now_time = datetime.now()
print(now_time)

# 时间对象。strptime(fmt) 将时间返回为字符串格式的日期
print(now_time.strftime('%Y:%m:%d %H:%M:%S'))

str_time = '2023:03:14 12:24:23'

# 将时间字符串转为时间字符串
timeT = datetime.strptime(str_time, '%Y:%m:%d %H:%M:%S')
print(timeT)
print(timeT.year)
print(type(timeT.month))

