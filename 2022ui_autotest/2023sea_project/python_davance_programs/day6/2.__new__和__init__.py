# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-09 20:02
# ---
"""
在Student类的__init__方法中，super(Student, self).__init__(name)这行代码的作用是调用Person类的__init__方法。让我们逐步解析这行代码：

super(Student, self)：这部分代码返回一个临时对象，该对象绑定到Student类的父类（即Person类），并且传递了当前实例（即self）。这样，我们就可以通过这个临时对象来调用父类的方法。
.__init__(name)：在返回的临时对象上调用__init__方法，并将name参数传递给它。这样，父类Person的__init__方法将被执行，以初始化name属性并打印消息。
通过使用super()函数，我们可以在子类中重用父类的方法，而无需显式地指定父类的名称。这提供了一种更灵活和可维护的方式来处理继承关系，特别是在多重继承的情况下。

总结起来，super()函数允许你在子类中调用父类的方法，以便重用和扩展父类的功能。在你的代码中，它用于调用Person类的初始化方法，以确保在创建Student对象时正确初始化属性。

"""

class Person(object):
    def __init__(self, name):
        self.name = name
        print("初始化对象的值", self.name)

    def __new__(cls, *args, **kwargs):
        print("开始创建对象并分配内存")
        self = super().__new__(cls)
        return self

    def sum(self, name):
        print ('输出--' +str(name))
        return '输出--' +str(name)

class Student(Person):  # 继承person
    def __init__(self, name, stu):
        super(Student, self).__init__(stu)  #
        self.stu = stu

    def study(self):
        print('-----srudy------')
        pass

    def sum(self, name):
        print('重写--' + str(name))
        # self.sum('kevin')

        return '重写--' + str(name)

class Teacher(Person):
    pass

if __name__ == "__main__":
    # xiaoming = Person("xiaoming")
    # Student('sea','no')
    Student('sea', 'no').sum('1')
