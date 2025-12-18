"""
@Author    : duansea
@Date      : 2025/6/24 19:19
@Description: [后台mq消息重试工具]
"""
import time

import requests
import json
from Common.CommonLittle.random_string import  generate_random_string
from account_data import DEFAULT_DATA
import urllib3

# 禁用所有不安全的 HTTPS 警告（适用于测试/内部环境）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



# ========== 全局 token 缓存 ==========
_token_cache = {
    "token": None,
    "env": None,
    "last_login_time": None,
    "max_age": 60 * 60  # 假设 token 有效期为 30 分钟
}

def _is_token_expired():
    """判断当前缓存的 token 是否过期"""
    if not _token_cache["token"]:
        return True
    if _token_cache["last_login_time"] is None:
        return True
    return (time.time() - _token_cache["last_login_time"]) > _token_cache["max_age"]

def login(env="uat", login_no="13166210870", password="uKXPzIcL55uI1IUq0yGrMw=="):
    """
    运营后台-登录获取 token，自动缓存
    """
    base_url = {
        "fat": "https://fat-global-ad.baofu.com",
        "uat": "https://uat-global-ad.baofu.com"
    }

    url = f"{base_url.get(env)}/oms-roleApi/login"
    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
    }
    payload = {
        "loginNo": login_no,
        "password": password,
        "picCode": ""
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                # 更新缓存
                _token_cache["token"] = data["token"]
                _token_cache["env"] = env
                _token_cache["last_login_time"] = time.time()
                print(f"[INFO] {env}环境 -登录成功，获取新 token，有效期 {_token_cache['max_age']} 秒")
                return data["token"]
            else:
                print("[ERROR] 登录成功但未返回 token")
                return None
        else:
            print(f"[ERROR] 登录失败，HTTP {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] 请求登录接口异常: {e}")
        return None


def payee_income_mq(env="fat", max_retries=1):
    """
    发送入账 MQ 补偿请求，自动处理 token 认证与 401 重试
    :param env: 环境 fat/uat
    :param max_retries: 最多重试一次（防止死循环）
    :return: requests.Response 对象
    """
    global _token_cache

    # 构建 session
    session = requests.Session()
    session.verify = False  # 忽略 SSL 验证（仅测试环境）

    # 请求 URL
    url = f"https://{env}-global-ad.baofu.com/ams-api/compensationCenter/retry/mqRetryProcess"

    # 构建请求体 —— 完全保留原始字段和注释
    data = {
        "routingKey": "BAOFU_CHANNEL_PAYEE_INCOME_NOTIFY_QUEUE_NAME",
        "routingMsg": {
            "bizType": 2,
            "sendObject": {
                "bankNo": generate_random_string("bankNo"),
                "bankPayeeFeeAmount": 500.00,  # 渠道手续费币种
                "bankPayeeFeeCcy": DEFAULT_DATA["bankPayeeFeeCcy"],  # 渠道手续费金额 ---- 币种
                "channelId": DEFAULT_DATA["channelId"],  # 渠道ID
                "channelIncomeAt": 1750743501001,
                "channelStatus": 1,
                "detailsId": generate_random_string(),
                "payeeAccountName": "WAN ECOMMERCE SOLUTIONS SDN. BHD.",
                "payeeAccountNo": DEFAULT_DATA["payeeAccountNo"],  # 收款方账号
                "payeeAmount": 50000,  # 渠道入账金额 CHANNEL_ENTRY_CCY
                "payeeCcy": DEFAULT_DATA["payeeCcy"],  # 渠道入账币种  HKD,EUR,GBP,SAR,ZAR,HUF,TRY,AED,USD,NOK,RON,KES,CZK,SEK
                "payeeDate": "20250724",
                "payeeIncomeStatus": 2,
                "payeeType": DEFAULT_DATA["payeeType"],  # 账号类型 1-gep电商  3-B2B收款  2-gep汇兑收款   4-服贸交易
                "payerAccountName": "seatongxiang",
                "payerAccountNo": "sea029039090",
                "payerBankName": "bank name",
                "payerCountry": "USA",
                "payerSwiftCode": "SVBKUS6SXXX",
                "reference": "bank seasea111",
                "remarks": DEFAULT_DATA["remarks"],  # fat环境-上海一一网络科技有限公司-自动化--gep-电商收款账户
                "remitAmount": 50500,  # 渠道汇款币种
                "remitCcy": DEFAULT_DATA["remitCcy"],  # 入账币种
                "remitPayerAddress": "29145 CRYSTAL RIDGE CT212amazon WeLLSFAGO ",
                "reserveFieldOne": "UT1868854659089010579",
                "storeNo": DEFAULT_DATA["storeNo"],  # 店铺号  没有则为0
                "userNo": DEFAULT_DATA["userNo"]  # 商户号
            },
            "traceLogId": generate_random_string("traceLogId")
        },
        "retryReason": "入账mqsea"
    }

    # 尝试发送请求（最多重试一次）
    for attempt in range(max_retries + 1):
        # 确保 token 有效
        if _token_cache["env"] != env or _is_token_expired():
            print(f"[INFO] Token 缓存失效或环境变更，重新登录获取 token...")
            token = login(env=env)
            if not token:
                print("[FATAL] 登录失败，无法获取 token，终止请求")
                return None
        else:
            token = _token_cache["token"]
            print(f"[INFO] 使用缓存中的 token 发送请求")

        # 设置 headers
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Cookie": f"agent-control-core-token={token}",
        }

        try:
            print(f"[INFO] 发送请求到 {url} (attempt {attempt + 1})")
            response = session.post(url, headers=headers, json=data,verify=False)

            print("Status Code:", response.status_code)
            try:
                resp_json = response.json()
                print("Response JSON:", resp_json)

                # 成功，直接返回
                if response.status_code != 401:
                    return response

                # 处理 401 错误
                if response.status_code == 401 and attempt < max_retries:
                    print("[WARNING] 401 Unauthorized，尝试重新登录...")
                    _token_cache["token"] = None  # 强制清除 token 缓存
                    continue  # 进入下一轮重试
                else:
                    return response  # 401 且无重试机会了

            except Exception as e:
                print("Error parsing JSON:", e)
                print("Response Text:", response.text)
                return response

        except Exception as e:
            print(f"[ERROR] 请求异常: {e}")
            return None

    return None



if __name__ == '__main__':
    # mq_retry_process(env="fat")
    # mq_retry_process_php(env="fat")

    # mq_retry_process(env="uat")
    # mq_retry_process_php(env="uat")


    # 电商入账和gep收款账户入账
    # gep_shop_mq_retry_process(env="fat")

    # B2B入账
    # b2b_mq_retry_process(env="fat")

    # 通用的入账mq
    payee_income_mq(env="uat")