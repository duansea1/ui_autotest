# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月09日 9:35
# ---

import requests

# r2 = requests.get("https://httpbin.org/get", verify=False)
# print(f"status doce: {r2.status_code}")


def status_code(response, *args, **kwargs):
    print(f"hook status code:{response.status_code}")

""" 
把打印状态码封装到一个status_code() 函数中，在requests.get() 方法中通过hooks 参数接收钩子函数status_code()。
status_code() 作为一个函数，可以做的事情很多，比如，进一步判断状态码，打印响应的数据，甚至对相应的数据做加解密等处理。
"""

# r = requests.get("https://httpbin.org/get", hooks={"response": status_code}, verify=False)
# r = requests.get("https://httpbin.org/get", hooks=dict(response=[status_code]), verify=False)




