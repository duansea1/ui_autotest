# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-09 19:39
# ---
"""
用来记录日志的装饰器
def1（参数）
使用参数
def2（func）
def3 wrapper（*arg, **kwarg）
return wrapper
return def2

"""

def log(filename: str):
    print('打印', filename)

    def inner(func):
        print(f"方法名：{func.__name__}()")

        def wrapper(*args, **kwargs):
            print('开始执行函数func')
            re = func(*args, **kwargs)
            print(f'{re}')
        return wrapper

    return inner

@log(filename="XXX.log")
def add(a, b):
    return a + b


if __name__ == '__main__':
    add(1,2)