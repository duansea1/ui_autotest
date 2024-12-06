# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-11-23 16:30
# ---
from commons.RSAUtil import *
from icecream import ic
import requests
import base64
import json
from Kuajing.Common import publicTools
from Kuajing.Common import enviromments as enc
from icecream import ic


def create_user(env):
    """新增代理商用户"""

    data = {
        "email": "121@111.com"
    }

    # 获取秘钥相关信息
    dataenv = enc.get_envs(env)
    pfx_path = dataenv.get('pfx_path')
    pfxpass = dataenv.get('pfx_pass')
    cer_path = dataenv.get('cer_path')
    agentNo = dataenv.get('agentNo')
    base_url = dataenv.get('url')
    certificateId = dataenv.get('certificateId')

    # 开始加密操作
    json_str = publicTools.jsonString(data)  # JSON 格式的字符串
    rsa_util = RSAUtil(pfx_path=pfx_path, pfxpass=pfxpass, cer_path=cer_path)
    dataContent = rsa_util.pri_encrypt(json_str)  # RSA加密

    url = f"{base_url}/api/agent/user/createUser"

    # 构建请求数据
    dataMap = {
        "agentNo": agentNo,
        "certificateId": certificateId,
        "dataContent": dataContent,
        "dataType": "JSON",
        "version": "1.0.0"
    }

    # 定义请求头
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # 发送HTTP POST请求
    response = requests.post(url=url, data=dataMap, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:

        print("响应结果：", response.text)
        return response.text
    else:
        print(f"请求失败：{response.tex}")
        return response.text


if __name__ == '__main__':
    # 海之蓝代理商用户新增
    res = create_user(env='fat-sea-agent-hzl')
    # print(res)
