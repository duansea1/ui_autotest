# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-08 18:25
# ---
# 需求：为字符串添加修饰 hello====》<i>hello<i>  hello ----> <b>hello<b>
from types import FunctionType

def add_itali(s):
    return "<i>" + s + "<i>"
# @add_itali
def add_bold(s):
    return "<b>" + s + "<b>"

if __name__ == "__main__":
    print(add_itali("ssss"))
    print(type(add_itali))

    print(add_itali('abc'))