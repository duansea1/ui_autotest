# mq_retry.py

import time
import requests
import json
from icecream import ic
import os

from Common.CommonLittle.random_string import generate_random_string
from account_data import get_test_data  
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



# 获取当前时间的毫秒级时间戳（13位整数），作为 channelIncomeAt
current_timestamp_ms = int(time.time() * 1000)
# ========== 全局 token 缓存 ==========
_token_cache = {
    "token": None,
    "env": None,
    "last_login_time": None,
    "max_age": 60 * 60
}

# 缓存文件路径
CACHE_FILE = os.path.join(os.path.dirname(__file__), '.token_cache.json')

def _load_token_cache():
    """从文件加载缓存的token"""
    global _token_cache
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                cached_data = json.load(f)
                # 验证缓存数据的有效性
                if all(key in cached_data for key in ["token", "env", "last_login_time", "max_age"]):
                    _token_cache = cached_data
                    print(f"[INFO] 从文件加载缓存的token，环境: {_token_cache['env']}")
    except Exception as e:
        print(f"[ERROR] 加载token缓存失败: {e}")

def _save_token_cache():
    """将token缓存保存到文件"""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(_token_cache, f)
        print(f"[INFO] Token缓存已保存到文件: {CACHE_FILE}")
    except Exception as e:
        print(f"[ERROR] 保存token缓存失败: {e}")

# 在模块加载时加载缓存
_load_token_cache()

def _is_token_expired():
    if not _token_cache["token"]:
        return True
    if _token_cache["last_login_time"] is None:
        return True
    return (time.time() - _token_cache["last_login_time"]) > _token_cache["max_age"]

def login(env="uat", login_no="13166210870", password="uKXPzIcL55uI1IUq0yGrMw=="):
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
                _token_cache["token"] = data["token"]
                _token_cache["env"] = env
                _token_cache["last_login_time"] = time.time()
                # 保存到文件
                _save_token_cache()
                print(f"[INFO] {env}环境 - 登录成功，获取新 token")
                return data["token"]
            else:
                print("[ERROR] 登录成功但未返回 token")
                return None
        else:
            print(f"[ERROR] 登录失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] 请求登录接口异常: {e}")
        return None


# ========== payee_income_mq 函数优化版 ==========

def payee_income_mq(account_key=None, env="uat", userNo=None, max_retries=1):
    """
    发送入账 MQ 补偿请求
    :param account_key: 账户标识，如 "yiyi_shop", "bank_pln" 等
    :param env: 环境，如 "fat", "uat"
    :param userNo: 用户编号（int 或 str），如 5181240702000026848
    :param max_retries: 最大重试次数（不含首次）
    :return: Response or None
    """
    global _token_cache

    # ✅ 使用新结构获取数据
    test_data = get_test_data(env=env, userNo=userNo, account_key=account_key)
    if not test_data:
        print(f"[FATAL] 无法获取测试数据: env={env}, userNo={userNo}, account_key={account_key}")
        return None

    session = requests.Session()
    session.verify = False

    url = f"https://{env}-global-ad.baofu.com/ams-api/compensationCenter/retry/mqRetryProcess"

    data = {
        "routingKey": "BAOFU_CHANNEL_PAYEE_INCOME_NOTIFY_QUEUE_NAME",
        "routingMsg": {
            "bizType": 2,
            "sendObject": {
                "bankNo": generate_random_string("bankNo"),
                "bankPayeeFeeAmount": 50.00,  # 渠道手续费金额
                "bankPayeeFeeCcy": test_data["bankPayeeFeeCcy"],  # 渠道手续费金额 ---- 币种
                "channelId": test_data["channelId"],  # 渠道ID
                "channelIncomeAt": current_timestamp_ms,  # 渠道入账时间戳
                "channelStatus": 1,    # 渠道入账状态 1-成功
                "detailsId": generate_random_string(),
                "payeeAccountName": "WAN ECOMMERCE SOLUTIONS SDN. BHD.",
                "payeeAccountNo": test_data["payeeAccountNo"],  # 收款方账号
                "payeeAmount": 50,  # 渠道入账金额 CHANNEL_ENTRY_CCY
                "payeeCcy": test_data["payeeCcy"],  # 渠道入账币种  HKD,EUR,GBP,SAR,ZAR,HUF,TRY,AED,USD,NOK,RON,KES,CZK,SEK
                "payeeDate": "20250724",
                "payeeIncomeStatus": 2,
                "payeeType": test_data["payeeType"],  # 账号类型 1-gep电商  3-B2B收款  2-gep汇兑收款   4-服贸交易
                "payerAccountName": "seatongxiang",
                "payerAccountNo": "sea029039090",
                "payerBankName": "bank name",
                "payerCountry": "USA",
                "payerSwiftCode": "SVBKUS6SXXX",
                "reference": "bank seasea111",
                "remarks": test_data["remarks"],  # fat环境-上海一一网络科技有限公司-自动化--gep-电商收款账户
                "remitAmount": 50,  # 渠道汇款金额
                "remitCcy": test_data["remitCcy"],  # 渠道汇款币种
                "remitPayerAddress": "29145 CRYSTAL RIDGE CT212amazon WeLLSFAGO ",
                "reserveFieldOne": "UT1868854659089010579",
                "storeNo": test_data["storeNo"],  # 店铺号  没有则为0
                "userNo": userNo  # 商户号
            },
            "traceLogId": generate_random_string("traceLogId")
        },
        "retryReason": "入账mqsea"
    }
    ic(data)
    for attempt in range(max_retries + 1):
        if _token_cache["env"] != env or _is_token_expired():
            print(f"[INFO] Token 缓存失效，重新登录...")
            token = login(env=env)
            if not token:
                print("[FATAL] 登录失败，终止请求")
                return None
        else:
            token = _token_cache["token"]
            print(f"[INFO] 使用缓存中的 token")

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Cookie": f"agent-control-core-token={token}",
        }

        try:
            print(f"[INFO] 发送请求到 {url} (attempt {attempt + 1})")
            response = session.post(url, headers=headers, json=data)

            print("Status Code:", response.status_code)
            try:
                resp_json = response.json()
                print("Response JSON:", resp_json)

                if response.status_code != 401:
                    return response

                if response.status_code == 401 and attempt < max_retries:
                    print("[WARNING] 401 Unauthorized，尝试重新登录...")
                    _token_cache["token"] = None
                    continue
                else:
                    return response
            except Exception as e:
                print("Error parsing JSON:", e)
                print("Response Text:", response.text)
                return response

        except Exception as e:
            print(f"[ERROR] 请求异常: {e}")
            return None

    return None


if __name__ == '__main__':
    # ✅ 示例1：fat-董春旭-gep-电商收款账户-入账mq测试
    # payee_income_mq(account_key="shop_wb_cnh", env="fat", userNo=5181240731000102528)

    # # ✅ 示例2：使用默认值（env="uat", userNo=默认, account_key=默认）
    # payee_income_mq()  # 使用 DEFAULT_ENV, DEFAULT_USERNO, DEFAULT_ACCOUNT_KEY
    #
    # # ✅ 示例3：仅指定 account_key，其余用默认
    # payee_income_mq(account_key="tx_shop")
    #
    # ✅ 示例4：香港五五测试
    # payee_income_mq(account_key="shop_alone_hkd", env="fat", userNo=5181240821000008798)
    # # ✅ 示例5：香港五五-b2b入账
    # payee_income_mq(account_key="b2b_eur", env="fat", userNo=5181240821000008798)


    # local_eur_gbp
    # ✅ 示例4：桐乡
    # payee_income_mq(account_key="local_eur_gbp", env="fat", userNo=5181240628000024148)
    # ✅ 示例4：qiya
    payee_income_mq(account_key="qiya_shop", env="fat", userNo=5181241126000123328)