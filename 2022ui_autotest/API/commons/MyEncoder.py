# -*- coding: utf-8 -*-
# ---
# @Software: 问题是由于json.dumps（）函数引起的。dumps是将dict
# 数据转化为str数据，但是dict数据中包含byte数据所以会报错
# @Author: duansea
# @Time: 2022年9月月04日 14:20
# ---
import json


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encodings="utf-8")
        return json.JSONEncoder.default(self, obj)