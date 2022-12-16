# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年10月月09日 20:39
# ---
import random


class Student():
    class_name = "三年级"

    def __init__(self,name, age):
        self.name = name
        self.age = age

    @classmethod
    def class_name(cls):
        classname = cls.class_name
        print(classname)

    @staticmethod
    def resvert(str):
        return str[::-1]

    def class_num(self):
        return True




st = Student('kobe','43')
Student.class_name()

sts = Student.resvert("nihao")
print(sts)
st.class_num()

st.__setattr__("teacher", 'kevin')
# st.__delattr__("teacher")
print(st.teacher)