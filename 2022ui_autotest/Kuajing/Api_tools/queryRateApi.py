# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-11-25 10:30
# ---
from commons.RSAUtil import *
import requests
import json
from Kuajing.Common import publicTools
from Kuajing.Common import enviromments as enc
from icecream import ic
# ic.configureOutput(prefix='DEBUG: ')
ic.configureOutput(includeContext=True)


def query_rate(env):
    """查询汇率-默认查的是biz_type=1的"""
    # 获取秘钥相关信息
    dataenv = enc.get_envs(env)
    pfx_path = dataenv.get('pfx_path')
    pfxpass = dataenv.get('pfx_pass')
    cer_path = dataenv.get('cer_path')
    agentNo = dataenv.get('agentNo')
    base_url = dataenv.get('url')
    certificateId = dataenv.get('certificateId')

    data = {
        "userNo": dataenv.get('userNo'),
        "originalCcy": "CNH",  # 买入
        "targetCcy": "USD",  # 卖出币种
        "closingDate": "2024-12-03"
    }
    ic(data)
    # 开始加密操作
    json_str = publicTools.jsonString(data)  # JSON 格式的字符串
    rsa_util = RSAUtil(pfx_path=pfx_path, pfxpass=pfxpass, cer_path=cer_path)
    dataContent = rsa_util.pri_encrypt(json_str)  # RSA加密

    url = f"{base_url}/api/rate/query-rate"

    # 构建请求数据
    dataMap = {
        "version": "1.0.0",

        "certificateId": certificateId,
        "userNo": dataenv.get('userNo'),
        "dataType": "JSON",
        "dataContent": dataContent,
        # "agentNo": agentNo,
        "apiType": 2       #
        # 1-代理商  2-商户
    }
    ic(dataMap)
    # 定义请求头
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
                result = rsa_util.pub_decrypt(result)  # RSA加密
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


""" GEP汇兑锁定申请"""
def apply_exchange(env):
    """ GEP汇兑锁定申请"""
    # 获取秘钥相关信息
    dataenv = enc.get_envs(env)
    pfx_path = dataenv.get('pfx_path')
    pfxpass = dataenv.get('pfx_pass')
    cer_path = dataenv.get('cer_path')
    agentNo = dataenv.get('agentNo')
    base_url = dataenv.get('url')
    certificateId = dataenv.get('certificateId')

    data = {
        "userNo": dataenv.get('userNo'),
        "userReqNo": "202412040000015",
        "buyCcy": "USD",  # 买入币种
        "buyAmount": 1,  # 买入金额，交易方向为买入时，此字段必须有值并且大于0
        "sellCcy": "CNH",  # 卖出币种
        "sellAmount": 3.11,  # 卖出金额，交易方向为卖出时，此字段必须有值并且大于0
        "closingDate": "2024-12-05",
        "closingType": "TOD",
        "direction": "2",  # 1-买入  2-卖出
        # "deliveryType": "AUTO",  # 交割方式：AUTO-自动交割 MANUAL-手动交割
        # "callbackUrl": ""
    }
    ic(data)
    # 开始加密操作
    json_str = publicTools.jsonString(data)  # JSON 格式的字符串
    rsa_util = RSAUtil(pfx_path=pfx_path, pfxpass=pfxpass, cer_path=cer_path)
    dataContent = rsa_util.pri_encrypt(json_str)  # RSA加密

    url = f"{base_url}/api/exchange/apply-exchange"

    # 构建请求数据
    dataMap = {
        "version": "1.0.0",
        "certificateId": certificateId,
        "userNo": dataenv.get('userNo'),
        "dataType": "JSON",
        "dataContent": dataContent,
        # "agentNo": agentNo,
        "apiType": 2       #
        # 1-代理商  2-商户
    }
    ic(dataMap)
    # 定义请求头
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
                result = rsa_util.pub_decrypt(result)  # RSA加密
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

""" GEP汇兑锁定确认"""
def confirm_exchange(env):
    """ GEP汇兑锁定确认"""
    # 获取秘钥相关信息
    dataenv = enc.get_envs(env)
    pfx_path = dataenv.get('pfx_path')
    pfxpass = dataenv.get('pfx_pass')
    cer_path = dataenv.get('cer_path')
    agentNo = dataenv.get('agentNo')
    base_url = dataenv.get('url')
    certificateId = dataenv.get('certificateId')

    data = {
        "userNo": dataenv.get('userNo'),
        "userReqNo": "202412040000015",
    }
    ic(data)
    # 开始加密操作
    json_str = publicTools.jsonString(data)  # JSON 格式的字符串
    rsa_util = RSAUtil(pfx_path=pfx_path, pfxpass=pfxpass, cer_path=cer_path)
    dataContent = rsa_util.pri_encrypt(json_str)  # RSA加密

    url = f"{base_url}/api/exchange/confirm-exchange"

    # 构建请求数据
    dataMap = {
        "version": "1.0.0",
        "certificateId": certificateId,
        "userNo": dataenv.get('userNo'),
        "dataType": "JSON",
        "dataContent": dataContent,
        # "agentNo": agentNo,
        "apiType": 2       #
        # 1-代理商  2-商户
    }
    ic(dataMap)
    # 定义请求头
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # 发送HTTP POST请求
    response = requests.post(url=url, data=dataMap, headers=headers, verify=False)

    if response.status_code == 200:
        try:
            response_data = response.json()  # 解析JSON响应
            if response_data.get('result'):
                result = response_data.get('result')  # 提取result字段
                print("响应结果：", response_data)
                # print("提取的result字段：", result)
                result = rsa_util.pub_decrypt(result)  # RSA加密
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

""" B2B查询商户计算汇率"""
def query_b2b_cal_rate(env):
    """ B2B查询商户计算汇率"""
    # 获取秘钥相关信息
    dataenv = enc.get_envs(env)
    pfx_path = dataenv.get('pfx_path')
    pfxpass = dataenv.get('pfx_pass')
    cer_path = dataenv.get('cer_path')
    agentNo = dataenv.get('agentNo')
    base_url = dataenv.get('url')
    certificateId = dataenv.get('certificateId')

    data = {
        "userNo": dataenv.get('userNo'),
        "originalCcy": "CNH",   # 买入币种
        "targetCcy": "USD",  # 卖出币种
        "closingDate": "2024-12-05",
    }
    ic(data)
    # 开始加密操作
    json_str = publicTools.jsonString(data)  # JSON 格式的字符串
    rsa_util = RSAUtil(pfx_path=pfx_path, pfxpass=pfxpass, cer_path=cer_path)
    dataContent = rsa_util.pri_encrypt(json_str)  # RSA加密

    url = f"{base_url}/api/rate/query-b2b-cal-rate"

    # 构建请求数据
    dataMap = {
        "version": "1.0.0",
        "certificateId": certificateId,
        "userNo": dataenv.get('userNo'),
        "dataType": "JSON",
        "dataContent": dataContent,
        # "agentNo": agentNo,
        "apiType": 2       #
        # 1-代理商  2-商户
    }
    ic(dataMap)
    # 定义请求头
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # 发送HTTP POST请求
    response = requests.post(url=url, data=dataMap, headers=headers, verify=False)

    if response.status_code == 200:
        try:
            response_data = response.json()  # 解析JSON响应
            if response_data.get('result'):
                result = response_data.get('result')  # 提取result字段
                print("响应结果：", response_data)
                # print("提取的result字段：", result)
                result = rsa_util.pub_decrypt(result)  # RSA加密
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

if __name__ == '__main__':
    # 代理商
    # query_rate(env="fat-sea-agent-hzl")
    # 商户
    # query_rate(env="fat-sea-wu")

    # GEP汇兑锁定申请
    apply_exchange(env="uat-sea-ss")
    # # apply_exchange(env="fat-sea-tx")
    # # GEP汇兑锁定确认
    confirm_exchange(env="uat-sea-ss")

    """ B2B查询商户计算汇率"""
    # query_b2b_cal_rate(env="uat-sea-ss")


