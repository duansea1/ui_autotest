# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-16 11:29
# ---

import jsonpath

data = {
    "store": {
        "book": [
            {"category": "reference",
             "author": "Nigel Rees",
             "title": "Sayings of the Century",
             "price": 8.95
             },
            {"category": "fiction",
             "author": "Evelyn Waugh",
             "title": "Sword of Honour",
             "price": 12.99
             }
        ],
        "bicycle": {
            "color": "red",
            "price": 19.95
        }
    }
}

ret = jsonpath.jsonpath(data, "$.store.book[*].author")  # *代表匹配多个子集中的字段
print(ret)
ret2 = jsonpath.jsonpath(data, "$..author")  # 查找二级下的author
print(ret2)
ret3 = jsonpath.jsonpath(data, "$.store..price")   # 按节点查询
print(ret3)

ret4 = jsonpath.jsonpath(data, "$..book[0].title")
print(type(ret4))

ret5 = jsonpath.jsonpath(data, "$..book[?(@.price>10)].price")   # ?(@.price>0) --这个是判断条件，获取符合条件的子集
print(ret5)