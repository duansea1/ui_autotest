"""
@Author    : duansea
@Date      : 2025/6/24 19:19
@Description: [后台mq消息重试工具]
"""

import requests
import json
from Common.CommonLittle.random_string import  generate_random_string

token = ("agent-control-core-token="+
         "eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3NTA4MzAwMzV9.lk3dJSpWokX8BoAlQ0TND8bGKQLj7qCjdH23yj0rzfnpRntMZOXVZGyTLwqlh8gTVTE-WBsy2QHKLcijArzPug")
def mq_retry_process():
    """B2B入账-Payso-电商收款-API"""
    url = "https://fat-global-ad.baofu.com/ams-api/compensationCenter/retry/mqRetryProcess"

    headers = {
        "Accept": "application/json",
        "Connection": "keep-alive",
        "Content-Type": "application/json; charset=utf-8",
        "Cookie": token,
    }
    # 货币对一致，无汇兑的场景
    data1 = {
        "routingKey": "BAOFU_CHANNEL_PAYEE_INCOME_NOTIFY_QUEUE_NAME",
        "routingMsg": {
            "bizType": 2,
            "sendObject": {
                "bankNo": "HK5IT250624000DH-6",
                "bankPayeeFeeAmount": 50.00,  # 渠道入账币种
                "bankPayeeFeeCcy": "PHP",  # 渠道入账金额
                "channelId": 1200923077,
                "channelIncomeAt": 1750743501000,
                "channelStatus": 1,
                "detailsId": 250624133867226016,
                "payeeAccountName": "WAN ECOMMERCE SOLUTIONS SDN. BHD.",
                "payeeAccountNo": "P900100108612",
                "payeeAmount": 100.000,  #商户入账金额
                "payeeCcy": "PHP",    #商户入账币种
                "payeeDate": "20250624",
                "payeeIncomeStatus": 2,
                "payeeType": 3,
                "payerAccountName": "usdtest",
                "payerAccountNo": "029039090",
                "payerBankName": "bank name",
                "payerCountry": "USA",
                "payerSwiftCode": "SVBKUS6SXXX",
                "reference": "bank seasea",
                "remarks": "bank-sea2",
                "remitAmount": 10.00,   #渠道汇款币种
                "remitCcy": "USD",     #渠道汇款币种
                "remitPayerAddress": "29145 CRYSTAL RIDGE CT212amazon WeLLSFAGO ",
                "reserveFieldOne": "UT1868854659089010579",
                "storeNo": 0,
                "userNo": 5181240628000024148
            },
            "traceLogId": "ca22ffa577bc411bb46f0f9d891e4f06"
        },
        "retryReason": "我的桐乡-fat"
    }
    # 货币对不一致，汇兑的场景
    data = {
        "routingKey": "BAOFU_CHANNEL_PAYEE_INCOME_NOTIFY_QUEUE_NAME",
        "routingMsg": {
            "bizType": 2,
            "sendObject": {
                "bankNo": generate_random_string("bankNo"),
                "bankPayeeFeeAmount": 500.00,  # 渠道手续费币种
                "bankPayeeFeeCcy": "VND",  # 渠道手续费金额 ---
                "channelId": 1200923050,   #---------------------------银行渠道
                "channelIncomeAt": 1750743501001,
                "channelStatus": 1,
                "detailsId": generate_random_string(),
                "payeeAccountName": "WAN ECOMMERCE SOLUTIONS SDN. BHD.",
                "payeeAccountNo": "GB85TCCL12345669644978",   # --------------------------收款方账号
                "payeeAmount": 89000,  #渠道入账金额 CHANNEL_ENTRY_CCY
                "payeeCcy": "VND",    #渠道入账币种
                "payeeDate": "20250624",
                "payeeIncomeStatus": 2,
                "payeeType": 3,
                "payerAccountName": "seatongxiang",
                "payerAccountNo": "sea029039090",
                "payerBankName": "bank name",
                "payerCountry": "USA",
                "payerSwiftCode": "SVBKUS6SXXX",
                "reference": "bank seasea",
                "remarks": "bank-sea2",
                "remitAmount": 989000,   #渠道汇款币种
                "remitCcy": "VND",     #渠道汇款币种   对应 CHANNEL_REMITTANCE_CCY
                "remitPayerAddress": "29145 CRYSTAL RIDGE CT212amazon WeLLSFAGO ",
                "reserveFieldOne": "UT1868854659089010579",
                "storeNo": 0,
                "userNo": 5181240628000024148
            },
            "traceLogId": generate_random_string("traceLogId")
        },
        "retryReason": "我的桐乡-fat"
    }

    # 发起请求
    session = requests.Session()
    response = session.post(url, headers=headers, json=data)

    # 打印响应内容
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception as e:
        print("Response Text:", response.text)
        print("Error parsing JSON:", e)

    return response


if __name__ == '__main__':
    mq_retry_process()