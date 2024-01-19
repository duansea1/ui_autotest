# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-12 12:16
# ---

class Cat(object):
    def say(self):
        print("maio-----")

class Dog(object):
    def say(self):
        print("wangwang----")

def f(obj):
    """obj 只要是用say的方法的对象就行"""
    obj.say()

if __name__ == '__main__':
    f(Cat())
    f(Dog())

"""
应用场景：发送消息
其实是包装每个类里面的相同方法(封装一个function，传入这些不同的类，调用相同的方法的设计称之为鸭子类型)
封装一个方法，接收不同的function，前提是接收的这些方法里都有这个方法指定的动作。
def send_msg(obj):
    obj.send()
"""