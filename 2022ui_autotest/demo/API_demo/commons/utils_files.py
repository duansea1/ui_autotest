# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-04-22 10:35
# ---
import os
import json

from icecream import ic

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def read_json(file_name, subdir=""):
    """读取josn文件"""
    if subdir:
        fpath=os.sep.join([BASE_DIR,"file",subdir,file_name]) + ".json"
    else:
        fpath=os.sep.join([BASE_DIR,"file",file_name]) + ".json"
    listCookies={}
    with open(fpath, "r", encoding="utf-8") as f:
        listCookies = json.loads(f.read())
    return listCookies

ic(BASE_DIR)