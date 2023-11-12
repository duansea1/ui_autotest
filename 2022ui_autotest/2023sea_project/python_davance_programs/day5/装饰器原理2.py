# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-08 18:25
# ---
# 需求：为字符串添加修饰 hello==》<i>hello<i>  hello =><b>hello<b>
"""若装饰器传参，需要3层嵌套"""
from types import FunctionType

def add_itali(func):
    def new_func():
        return "<b>" + func() + "<b>"
    return new_func

def add_bold(func):
    print('func:',func)
    def new_func():
        return "<a>" + func() + "<a>"
    return new_func

@add_bold
@add_itali   # 语法糖（装饰器）
def text():
    return "hello"

if __name__ == "__main__":
    print(add_itali("ssss"))
    print(type(add_itali))
    print(text())