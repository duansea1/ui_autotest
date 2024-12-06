# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-08-22 10:22
# ---

from commons.RSAUtil import *
# 假设这是你的datacontent 明文信息：{email=121@111.com}
from icecream import ic
import requests
import base64
import json

# 加密内容传参
pfx_path = 'C:\\Users\段海洋\\myfiles\\auto_files\\ui_autotest\\2022ui_autotest\\demo\\API_demo\KuaJing\\tools\\key_5182240620000018698@@2406261353000001391.pfx'
pfxpass = '5182240620000018698_435548'
cer_path = 'C:\\Users\段海洋\\myfiles\\auto_files\\ui_autotest\\2022ui_autotest\\demo\\API_demo\\KuaJing\\tools\\key_5182240620000018698@@2406261353000001391.cer'


data_encode = ("c7806c6822b21884788f1b4561b8fefe13c6ffde50936f307964686bac07d2b0247162563484b3"
               "0975ba9e61e6bd3fec7ef26ced8d706d453b8fd503cf8e071b12de694ec921dee06f0a831bca35c97d9bf7a4e3"
               "1a94fca9d44cfc098fc409fb276fb6ba494f583343235922a5dae1c4ffdc7143c068546a9329ddef1fe13e34")

encryted_str = "6717921993c3e4e449de0e331c7122761991359050b5b3735032cf60edd5b64d51cb19b83e595e9b802bf147d2ecc76eaf3207bae6365fa52935afd383ec476562b4901657727507d991409f5225df8ecd1d71fc471d4beaa26db2518c2b79295e5b19ed4e0179690fef3b2421c4226e1e4f72569c009c558a77ab8fe3e27d62"
# 字典
data_content_map = {"email": "121@111.com"}

# 将字典转换为JSON字符串
json_str = json.dumps(data_content_map, separators=(',', ':'))

# # 对JSON字符串进行UTF-8编码后使用Base64编码
# encoded_data = base64.b64encode(json_str.encode('utf-8'))
#
# # 去除尾部的换行符
# encoded_data = encoded_data.strip()
#
# # 打印原始字典（即“明文信息”）
# print("明文信息：", data_content_map)
#
# # 打印Base64编码后的结果
# print("Base64编码后的信息：", encoded_data.decode('utf-8'))
# data = encoded_data.decode('utf-8')



# ic(encoded_data)
# data = 'eyJlbWFpbCI6IjEyMUAxMTEuY29tIn0='
rsa_util = RSAUtil(pfx_path, pfxpass, cer_path)

pri_en = rsa_util.pri_encrypt(json_str)
print("私钥加密内容：{}".format(pri_en))
print("公钥解密内容：{}".format(rsa_util.pub_decrypt(pri_en)))

pub_en = rsa_util.pub_encrypt(json_str)
print("公钥加密内容：{}".format(pub_en))
print("私钥解密内容：{}".format(rsa_util.pri_decrypt(pub_en)))


# 定义请求URL-fat环境
url = "http://10.254.95.181:8061/api/agent/user/createUser"

# 构建请求数据
dataMap = {
    "agentNo": "5182240620000018698",
    "certificateId": "2406261353000001391",
    "dataContent": pri_en,
    "dataType": "JSON",
    "version": "1.0.0"
}

# 定义请求头
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# 发送HTTP POST请求
response = requests.post(url, data=dataMap, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    # 打印响应结果
    print("响应结果：", response.text)
else:
    print(f"请求失败，状态码：{response.status_code}")
