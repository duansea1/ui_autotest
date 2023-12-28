# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-10-31 11:52
# ---
"""
递归：函数里调用本身函数
遍历目录：输出某文件夹下的所有文件

"""
import os

def print_all_files(file_path):
    for root, dirs, files in os.walk(file_path):
        # print(root)
        for file in files:
            print(os.path.join(root, file))  # 使用os函数拼接路径

def print_all_file2(file_path):
    """
    思路：获得file_path下所有文件及文件夹:os.scandir(file_path);;;os.listdir(file_path)
    如果是文件直接输出；
    如果是文件夹，递归调用
    :param file_path:
    :return:
    """
    for item in os.scandir(file_path):
        if item.is_file():
            print(item.path)
        elif item.is_dir():
            print_all_file2(item.path)

def recoder(n: int):  # n必须大于0
    # 过深的递归会导致栈溢出
    if n == 1:
        return True
    else:
        n -= 1  # 每递归一次，层数减1
        print(n)
        recoder(n)
def recoder2():
    recoder2()


if __name__ == "__main__":
    p = ("C:/Users/段海洋/myfiles/auto_files/ui_autotest/2022ui_autotest"
         "/2023sea_project/python_davance_programs/day3")
    # print_all_file2(p)
    # 注意，os.walk('.') 会遍历当前目录及其所有子目录
    print_all_files('.')
    recoder(995)
