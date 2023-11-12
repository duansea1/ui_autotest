# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-09 12:06
# ---
import time
# 计算函数的执行时间
def calc_time(func):  # 如果装饰器带参数，则需要多一层方法嵌套
    # @wraps(func)
    def wrapper(*args, **kwargs):
        now = time.time()
        time_array = time.localtime(now)
        start_styleTime = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        print(func.__name__ + '==========开始执行时间：' + str(start_styleTime) + '==============')
        func(*args, **kwargs)  # 执行的函数
        end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print(func.__name__ + '==========执行完成时间：' + str(end) + '==============')
    return wrapper

@calc_time
def sum(num):
    s = 0
    for i in range(num):
        s = i +s
    print(s)
    return s

if __name__ == "__main__":
    print(sum(1000))