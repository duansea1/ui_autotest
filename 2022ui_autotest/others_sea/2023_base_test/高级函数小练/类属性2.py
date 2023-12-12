# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年10月月10日 19:04
# ---
import os

current_file = os.getcwd()


class File():

    files = current_file+'\other.text'
    def __init__(self,file):
        self.file = file

    def readfile(self, file):
        with open(file, 'r+', encoding='gbk') as f:
            for i in f.readlines():
                # content = f.read()
                print(i, end="")
        return self.file

    @classmethod
    def readfiles(cls, file):
        with open(file, 'r+', encoding='gbk') as f:
            for i in f.readlines():
                # content = f.read()
                print(i, end="")
        return cls.files

    @staticmethod
    def readffileline(file):
        with open(file, 'r+', encoding='gbk') as f:
            for i in f.readlines():
                # content = f.read()
                print(i, end="")
        return True


f = File(file=None)
f.readfile(current_file+'\other.text')
print("=======", end=' \n ')
File.readffileline(current_file+'\other.text')