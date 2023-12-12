# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月19日 19:17
# ---

class B:
    age = 10

    def __init__(self, name):
        self.name = name

    def sleep(self):    #打印
        print('sleep的结果',self)

    @classmethod
    def eat(cls):  # 被修饰的函数
        print('eat的返回结果：',cls)  #看看传递的是类还是值
        print(cls.age)  #访问类的属性
        print(self.name)	#访问实例对象的属性


b = B("龙叔")
b.sleep()
b.eat()
