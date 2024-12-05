# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-11-09 13:26
# ---
import requests
import json
import urllib
import urllib3
# 忽略 SSL 警告
from icecream import ic

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def encrypt_source(source_str, user_no=5182240620000018698, certificate_id=2406261353000001391):
    # fat 环境
    base_url = "https://fat-member.gepholding.com/api/security/encrypt"
    params = {
        "sourceStr": source_str,
        "userNo": user_no,
        "certificateId": certificate_id
    }
    datas = {"email": "121@111.com"}
    # 对查询参数进行 URL 编码
    query_string = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_string}"

    # 设置请求头
    headers = {}

    # 发送 GET 请求
    response = requests.get(url, headers=headers, verify=False)
    res = json.loads(response.text)
    ic(res)
    if res['code'] == '0':
        # ic(res['result'])
        return res['result']
    else:
        return None


def create_user_api():
    url = "http://10.254.95.181:8061/api/agent/user/createUser"

    dataclasses = {"email": "121@111.com"}

    data_encode = encrypt_source(source_str=dataclasses)

    if data_encode:
        dataContent = data_encode
    else:
        raise "加密失败"
    # 构建请求数据
    dataMap = {
        "agentNo": "5182240620000018698",
        "certificateId": "2406261353000001391",
        "dataContent": dataContent,
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

if __name__ == '__main__':
    create_user_api()