# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-11-23 16:39
# ---
import json

def jsonString(data):
    """
    转换 Swift 字典为 JSON 字符串
    data_value = {"email": "121@111.com"}
    """

    # 将字典转换为JSON字符串
    return json.dumps(data, separators=(',', ':'))
