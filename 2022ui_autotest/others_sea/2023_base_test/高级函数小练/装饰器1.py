# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年12月月25日 16:40
# ---
import time





def decorator(func):
    # 计算函数的执行时间
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print('执行时间：', end_time-start_time)
    return inner

@decorator
def my_test():
    for i in range(100000000):
        pass


my_test()
