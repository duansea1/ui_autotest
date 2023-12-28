# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-05 12:20
# ---
# 函数里面套函数
"""
回调函数（callback function）是一个在特定事件发生时被调用的函数。在Python中，回调函数可以用于各种场景，如事件处理、异步编程、函数式编程等
"""
def callback_fuc(arg1, arg2):
    return f"callback func:{arg1}、{arg2}"

def main_func(callback):
    print('main function running')
    callback('kaevin', 'sea')

if __name__ == '__main__':
    main_func(callback_fuc)
