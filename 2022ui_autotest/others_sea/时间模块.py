# -*- coding: utf-8 -*-
# ---
<<<<<<< HEAD
<<<<<<< HEAD
# datetime模块
# @Author: duansea
# @Time: 2022年12月月28日 14:25
# ---

import datetime
import time
# from datetime import datetime

print(datetime.date.today())  # 打印当前日期

# time模块
# time.time() 获取当前时间戳
# time.strftime(fmt, t) 用于将时间对象格式化成熟悉的时间格式
# time.strptime(str, fmt) 用于将时间字符串转化成时间对象

print(time.time())
print(time.gmtime())  # 格林时间

print('-'*10 + '分割线localtime' + '-'*10)
print(time.localtime())  #获取当前当地时间
print('-'*10 + '分割线localtime' + '-'*10)

print(dir(time.localtime()))

# 用于将时间对象，格式化为熟悉的格式

print('-'*10 + '分割线' + '-'*10)

print(time.strftime('%Y-%M-%D %H:%M:%S %a %p'), time.localtime())

# mytime = input('请输入时间：')


=======
=======
>>>>>>> 5210fa1b7715b51962a03b38b5322cac1dc97b6c
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年12月月28日 14:25
# ---
<<<<<<< HEAD
>>>>>>> 5210fa1b7715b51962a03b38b5322cac1dc97b6c
=======
>>>>>>> 5210fa1b7715b51962a03b38b5322cac1dc97b6c
