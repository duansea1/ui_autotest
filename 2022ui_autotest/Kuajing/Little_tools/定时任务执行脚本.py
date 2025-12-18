"""
@Author    : duansea
@Date      : 2025/7/15 14:06
@Description: [定时任务执行脚本，通过token区分环境]
"""
import time

import requests
import json

# 接口地址
run_url = "https://uat-global-ad.baofu.com/ams-api/timedJob/run"
edit_url = "https://uat-global-ad.baofu.com/ams-api/timedJob/edit"

token = ("agent-control-core-token=" +
         "eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDcwMjEzMzcyNDAwNjUiLCJpYXQiOjE3NTI3MTQ1Mzd9.vdDzUrbqJooA7Qg0gyZ-YDqibY44G1c7HZ4fWOAd0ar6CmyOYeV-wMmP1IpJF760at5onaIa-IAUG6tiQFndQA")

headers = {
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    # Cookie 替换为你自己的 token
    "Cookie": token
}

def 小币种损益计算():
    # jobNo 354 为小币种销售损益计算-fat环境的
    # 289 为小币种销售损益计算-uat环境的
    data = {
        "jobNo": 289,
        "operationBy": "段海洋-uat"
    }

    # 发起 POST 请求
    response = requests.post(
        url=run_url,
        headers=headers,
        data=json.dumps(data)
    )

    # 打印响应结果
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

def 小币种损益编辑():
    # 请求体（可变参数）
    data = {
        "jobName": "小币种销售损益计算",
        "jobGroup": "baofu-admin-control-core",
        "jobCronExpress": "0 0 8 * * ?",
        "jobExecCount": "0",
        "jobCronExpressDesc": "每天早上8点直接",
        "jobClass": "springCloudJobWorkImpl",
        "retryTimes": "0",
        "reserve": "/api/v1/calcSmallCcyTask?{\"reCalc\":\"T\",\"beginDate\":\"2025-05-01 10:00:00\",\"endDate\":\"2025-09-15 10:00:00\",\"receiptId\":\"2507171045001637129\",\"runType\":\"APPOINT\"}",
        "jobNo": 289,
        "operationBy": "段海洋-uat"
    }

    # 发起 POST 请求
    response = requests.post(
        url=edit_url,
        headers=headers,
        data=json.dumps(data, ensure_ascii=False).encode('utf-8')  # 确保中文字符正确编码
    )

    # 打印响应结果
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

if __name__ == '__main__':

    小币种损益编辑()
    time.sleep(0.5)  # 等待10秒，等待任务执行完毕
    小币种损益计算()
