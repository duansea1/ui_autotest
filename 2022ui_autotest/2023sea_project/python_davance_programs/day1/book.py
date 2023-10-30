# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月22日 10:47
# ---
import os.path
import pickle      # 序列化和反系列化-


class Book(object):
    def __init__(self, num, name, positon):
        self.num = num
        self.name = name
        self.positon = positon

    def __str__(self):  # 属性方法
        """自定义 print对象时显示的格式"""
        return f"{self.num}\t{self.name}\t{self.positon}"


class BookMange(object):
    book_list = []

    def __init__(self):
        """加载文件到内存"""
        # __init__对象被初始化的时候执行
        print("__init__ is running.......")

        # 加载文件到内存
        if not os.path.isfile("book.data"):  # 判断文件是否存在
            pickle.dump(self.book_list, open("book.data", "wb"))  # 把对象保存到文件
        # 确保每次运行前，把book.data中的内容load到book_list中
        self.book_list = pickle.load(open("book.data", "rb"))  # 把文件中的内容加载到内存
        # 避免异常的方法：1、加判断、2、异常处理

    def show_book(self):
        """显示所有图书"""
        for book in self.book_list:
            print('book:', book)

    def add_book(self, book: Book):
        """添加书"""
        self.book_list.append(book)

    def del_book_by_name(self, name:str):
        """根据书名删除图书"""
        for i, book in enumerate(self.book_list):
            if book.name == name:
                del self.book_list[i]
                # self.book_list.remove(book)
                break

    @property  # 装饰器、调用时不需要加（）
    def last_book_id(self):
        """如果book_list是空，返回0，否则，返回最后一本书的值"""
        if self.book_list:
            last_book = self.book_list[-1]  # 获得最后数的属性
            return self.book_list[-1].num   # 取list表里的最后一个中的num
        return 0

    def __del__(self):
        """把内存中的数据保存到文件中"""
        # 析构方法
        # 在对象被销毁的时候自动执行
        print("__del__ is running.......")
        # 确保退出时，把self.book_list的内容序列化到book.data中
        pickle.dump(self.book_list, open("book.data", "wb"))  # 把对象保存到文件，若没有文件则创建
        print("执行完成")

    def save(self):
        pickle.dump(self.book_list, open("book.data", "wb"))

    def clean(self):
        """ 清空book_list"""
        self.book_list = []


if __name__ == "__main__":
    book = Book(1, '编程书', '1楼')
    print(book)
    # print(f"{book.num}\n{book.name}\t{book.positon}")
    bookmange = BookMange()
