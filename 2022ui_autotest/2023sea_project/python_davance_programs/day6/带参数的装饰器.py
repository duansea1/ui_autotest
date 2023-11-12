# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-09 19:39
# ---
"""
用来记录日志的装饰器

"""

def log(filename: str):
    print(filename)

    def inner(func):
        print(f"{func.__name__}")

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper

    return inner

@log(filename="XXX.log")
def add(a, b):
    return a + b
