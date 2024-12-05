# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-11-21 19:25
# ---
import json
import csv
import os

from icecream import ic

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print("files_opr - BASE_DIR :", BASE_DIR)
# C:\Users\段海洋\myfiles\auto_files\ui_autotest\2022ui_autotest\Kuajing

def get_files(subdir, filename):
    """
    @subdir:文件目录
    @filename:文件名称
    return: 文件地址
    """
    fpath = os.sep.join([BASE_DIR, "Files", subdir, filename])
    return fpath


if __name__ == '__main__':
    path = get_files("FatAgentFiles", "key_5182240909000002158@@2409101910000000504.cer")
    ic(path)
