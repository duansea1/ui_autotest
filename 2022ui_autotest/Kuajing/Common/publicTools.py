# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-11-23 16:39
# ---

from commons.RSAUtil import *
from Kuajing.Common import enviromments as enc
from icecream import ic
from Kuajing.Common import publicTools
import json
import requests

def jsonString(data):
    """
    转换 Swift 字典为 JSON 字符串
    data_value = {"email": "121@111.com"}
    """
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
                print(f"{url}未解密前的响应结果：", response_data)
                result = rsa_utils.pub_decrypt(result)  # RSA加密
                with open('跨境接口调用成功返回记录表.txt', "a") as f:
                    f.write(f"\n {url}调用成功返回结果：\n {result}")
                print(f"{url}解密结果：{result}")
                return result
            else:
                print(f"{url}解密result失败结果：{response_data}")
                return response_data
        except json.JSONDecodeError as e:
            print(f"{url}解析JSON失败：{e}")
            return None
    else:
        print(f"{url}请求失败：{response.text}")
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
    dataContent = rsa_utils.pri_encrypt(json.dumps(data))  # RSA加密
    return rsa_utils, dataContent


def data_Map(data_env, dataContent, apiType=None):
    """
    构建数据Map
    @param data_env: 环境变量
    @param dataContent: 加密后的数据
    @param apiType: 1-代理商  2-商户  3-代理商和商户
    @return dataMap: 构建的数据Map
    """
    dataMap = {
        "version": "1.0.0",
        "certificateId": data_env.get('certificateId'),
        "dataType": "JSON",
        "dataContent": dataContent,
        # "userNo": data_env.get('userNo'),
        # "agentNo": data_env.get('agentNo'),
        # "apiType": 1  # 1-代理商  2-商户

    }
    if apiType:
        if apiType == 1:
            # 传代理商参数
            dataMap['apiType'] = apiType
            dataMap['agentNo'] = data_env.get('agentNo')
            return dataMap
        elif apiType == 2:
            # 传代理商参数
            dataMap['apiType'] = apiType
            dataMap['userNo'] = data_env.get('userNo')
            return dataMap
        elif apiType == 3:
            # 传代理商参数和商户参数
            dataMap['apiType'] = 1
            dataMap['userNo'] = data_env.get('userNo')
            dataMap['agentNo'] = data_env.get('agentNo')
            return dataMap
    else:
        # 无代理商和商户参数
        return dataMap




