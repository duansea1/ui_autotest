# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-05 12:35
# ---
"""
闭包：函数里嵌套其他函数输出

"""
import logging


def logger(func):
    def log_func(*args):
        logging.basicConfig(filename='day4.log', level=logging.INFO)
        logging.info(f"{func.__name__} is running,argument is {args}")
    return log_func  # 把log_func函数的引用 传给logger的调用者

def f1(a, b):
    return a + b

def f2(x, y):
    return


def out_func(n):
    num = n

    def inner_func():
        # nonlocal--通常用在嵌套函数中
        nonlocal num
        num -= 1
        print('done done!')
    # 返回的不需要加（）。直接返回函数名称
    return inner_func


f1_logger = logger(f1)  # 返回该嵌套的函数func-->f1
print(f1_logger)
# f2_logger = logger(f2)
f1_logger(1, 222)  # 执行f1(1,222)函数
# f2_logger(2, 3)

# o_f = out_func(30)
# o_f()
def zip_test():
    a = ['a', 'b']
    b = [1,2]
    print(zip(a, b))
    for item in zip(a, b):  # 遍历zip
        print(item)


# zip_test()


