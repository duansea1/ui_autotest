# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-11-23 16:39
# ---
import json
from icecream import ic
from Kuajing.Common import publicTools
import requests
from commons.RSAUtil import *
from Kuajing.Common import enviromments as enc

def jsonString(data):
    """
    转换 Swift 字典为 JSON 字符串
    data_value = {"email": "121@111.com"}
    """
    # 将字典转换为JSON字符串
    return json.dumps(data, separators=(',', ':'))

def send_request(rsa_utils, url, dataMap):
    """Send request"""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # 发送HTTP POST请求
    response = requests.post(url=url, data=dataMap, headers=headers, verify=False)

    if response.status_code == 200:
        try:
            response_data = response.json()  # 解析JSON响应
            if response_data.get('result'):
                result = response_data.get('result')  # 提取result字段
                print("响应结果：", response_data)
                # print("提取的result字段：", result)
                result = rsa_utils.pub_decrypt(result)  # RSA加密
                ic(result)
                return result
            else:
                ic(response_data)
                return response_data
        except json.JSONDecodeError as e:
            print(f"解析JSON失败：{e}")
            return None
    else:
        print(f"请求失败：{response.text}")
        return None


def rsa_generate(data, env):
    """RAS加密
    @param data: json
    @param env: 环境
    @return rsa_utils: RSA 工具类
    @return dataContent: 加密后的数据
    """
    data_env = enc.get_envs(env)
    rsa_utils = RSAUtil(pfx_path=data_env.get('pfx_path'), pfxpass=data_env.get('pfx_pass'),
                        cer_path=data_env.get('cer_path'))
    dataContent = rsa_utils.pri_encrypt(jsonString(data))  # RSA加密
    return rsa_utils, dataContent

