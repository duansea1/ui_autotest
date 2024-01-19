# -*- coding: utf-8 -*-
"""
# 什么是单例模式
# 什么是装饰器，带参数的装饰器的调用顺序
# __new__ 和__init__的区别
# supershi shenm
# 实现一个类，前5次创建对象，以后创建返回5个中的一个
"""

import random

class MyClass(object):
    objs = []

    def __new__(cls, *args, **kwargs):
        if len(cls.objs) < 5:
            obj = super().__new__(cls)  # 创建实例
            cls.objs.append(obj)
        else:
            obj = random.choice(cls.objs)  # 随机选择一个
        return obj

class Person(object):
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def fullname(self):
        print(f"{self.firstname} {self.lastname}")

class Student(Person):

    def __init__(self, firstname, lastname, grade):
        self.grade = grade
        # # 初始化父类
        # Person.__init__(self, firstname, lastname)  # 方法1：将父类初始化
        super().__init__(firstname, lastname)   # 方法2： 与上边是一样的效果(在子类中调用父类的初始化方法)
        # super().__init__(firstname, lastname)  # 方法3，调用继承的父类

    # def __str__(self):
    def show_student(self):
        Person.fullname(self)    # 此处的self就是student
        print("grade：", self.grade)


class A(object):
    def __init__(self,):
        # self.a = a
        super().__init__()
        print("A---")

    def dayin(self):
        s = 'A'
        return s

class B(object):
    def __init__(self):
        super().__init__()
        print("B---")

    def dayin(self):
        s = 'B'
        return s

class C(A, B):
    """
    类继承，优先从左到右继承
    """
    def __init__(self):
        super(B, self).__init__()
        print("C---")
        # B.__init__(self)

if __name__ == "__main__":
    stu = Student('tom', '-o', '第7期')
    stu.show_student()

    c = C()
    # print(c.dayin())


