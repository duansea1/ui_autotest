"""
@Author    : duansea
@Date      : 2025/7/25 15:59
@Description: 模拟不同IP请求接口，并支持动态传参控制请求频率，打印详细日志，包括响应内容和状态码
"""
import json

import random

import requests
import time
from threading import Thread
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 请求配置
# URL = "https://uat-member.gepholding.com/api/user/pwd/isExistPwd/2"
URL= "https://uat-global-ad.baofu.com/ams-api/ipListLimit/page"
HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'Hm_lvt_4481d82590bdc2a34bde3cde07f3ef59=1751533112; agent-control-core-token=eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDcwMjEzMzcyNDAwNjUiLCJpYXQiOjE3NTM3NjgxODF9._aczEBu0n1TrAHHFXSnISRwOwWFexq0r8O7vbSYSU2rFtnIKAHl43SkbOheDfSUmPIbJhZTkGyFhqdg5gNvUeg'
}
data = {"currentPage":1,"pageSize":10}

# 模拟IP池
IP_POOL = [f"192.168.1.{i}" for i in range(1, 2)]  # 示例两个IP

def make_request(ip, req_num):
    headers = HEADERS.copy()
    headers["X-Forwarded-For"] = ip

    print(f"⏩[{datetime.now()}] 第 {req_num} 次请求开始，IP: {ip}")

    try:
        response = requests.post(URL, headers=headers,data=json.dumps(data), timeout=10, verify=False)
        # response = requests.get(URL, headers=headers, timeout=10, verify=False)

        # 打印状态码
        print(f"🚀[{datetime.now()}] 第 {req_num} 次请求完成，IP: {ip}")
        print(f"🚀响应状态码: {response.status_code}")

        # 打印响应内容（区分JSON和文本）
        if response.headers.get("Content-Type", "").lower().startswith("application/json"):
            try:
                print("响应内容（JSON）:")
                print(response.json())
            except requests.exceptions.JSONDecodeError:
                print("响应内容（原始文本，JSON解析失败）:")
                print(response.text[:1000])  # 打印前1000字符
        else:
            print("响应内容（文本）:")
            print(response.text[:1000])  # 打印前1000字符，防止日志过长

        if response.status_code >= 400:
            print(f"[ERROR] 请求失败，状态码: {response.status_code}, IP: {ip}")

    except Exception as e:
        print(f"[{datetime.now()}] 第 {req_num} 次请求异常: {e}, IP: {ip}")

def send_requests_in_period(ip, time_seconds, number):
    print(f"[{datetime.now()}] 开始请求任务，IP: {ip}，{time_seconds}s 内发送 {number} 次请求")

    interval = time_seconds / number  # 计算每次请求的间隔

    for i in range(1, number + 1):
        Thread(target=make_request, args=(ip, i)).start()
        time.sleep(interval)

    print(f"[{datetime.now()}] 请求任务结束，IP: {ip}，共发送 {number} 次请求")

def main():
    # ✅ 可配置参数
    time_seconds = 10    # 单位：秒
    number = 100          # 在 time_seconds 秒内发送 number 次请求
    ip = random.choice(IP_POOL)  # 随机选择一个IP

    send_requests_in_period(ip, time_seconds, number)

if __name__ == "__main__":
    main()