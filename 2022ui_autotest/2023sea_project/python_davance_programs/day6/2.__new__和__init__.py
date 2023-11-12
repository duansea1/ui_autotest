# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-09 20:02
# ---
class Person(object):
    def __init__(self, name):
        self.name = name
        print("初始化对象的值")

    def __new__(cls, *args, **kwargs):
        print("开始创建对象并分配内存")
        self = super().__new__(cls)
        return self

class Student(Person):
    def __init__(self, name, stu):
        super(Student, self).__init__(name)

    def study(self):
        pass

class Teacher(Person):
    pass

if __name__ == "__main__":
    xiaoming = Person("xiaoming")