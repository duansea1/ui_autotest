# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-12 11:11
# ---
"""
with：上下文管理协议 对象一定包含 __enter__ 和__exit__
被with包裹的代码块在被执行前先执行__enter__ 代码执行结束后，再执行__exit__
"""
class Myclass():
    def __enter__(self):
        print("enter---")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit-----")



#  open 返回一个对应-文件对象，文件对象支持上下文管理协议
f = open()
