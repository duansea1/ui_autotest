# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月09日 9:50
# ---

import requests

def print_url(r, *args, **kwargs):
    print("rul:"+r.url)

# 钩子函数2
def change_url(r, *args, **kwargs):
    r.url = 'http://change.url'
    print("changed_url: " + r.url)
    return r

# tips: http://httpbin.org能够用于测试http请求和响应
url = 'http://httpbin.org/cookies'
response = requests.get(url, hooks=dict(response=[print_url, change_url]))
print("result_url: "+response.url)

dics = dict(we=[123, 234])
print(dics)





