import logging

from Api_tools.FxRateApi import *
import concurrent.futures
import random
import string

def generate_random_string(length):
    """生成由字母和数字组成的随机字符串"""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choices(letters_and_digits, k=length))



"""
    fat:代理商 fat-sea-agent-hzl
    uat:代理商 uat-sea-agent-hzl
    prod: 代理商 prod-sea-agent-dhf

    """
fat_env = "fat-sea-agent-hzl"
uat_env = "uat-sea-agent-hzl"
# prod_env = "prod-sea-agent-dhf"
# 代理商
# query_rate(env=fat_env)
# 商户
# query_rate(env="fat-sea-wu")

"""GEP汇兑锁定申请-done"""
# apply_exchange(env="uat-sea-ss")






# 生成一个10个字符长的随机字符串
# random_string = generate_random_string(20)

N = 1

env=fat_env
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     futures = []
#     for _ in range(N):
#         userReqNo = generate_random_string(20)
#         futures.append(executor.submit(apply_exchange_agent, env, userReqNo=userReqNo, closingType="TOD",
#                                        closingDate="2025-03-12", deliveryType="MANUAL",tradeModel=1))
#         futures.append(executor.submit(confirm_exchange_agent, env, userReqNo=userReqNo))
#     for future in concurrent.futures.as_completed(futures):
#         future.result()
#     N += 1

while N <= 1:
    userReqNo = generate_random_string(20)
    # 定义汇兑申请参数
    exchange_params = {
        'closingType': "TOD",  # TOD:立即交割 TOM:T+1日交割 SPOT:T+2日交割
        'closingDate': "2025-03-28",  # 交割日期
        'deliveryType': "MANUAL",  # AUTO:自动交割 MANUAL:手动交割
        'tradeModel': 2,  # 1:实时 2:预约
        "direction": 1,  # 1-买入  2-卖出
        # "buyCcy": "CNH",  # 买入币种
        # "buyAmount": 1,  # 买入金额，交易方向为买入时，此字段必须有值并且大于0
        # "sellCcy": "USD",  # 卖出币种
        # "sellAmount": 1,  # 卖出金额，交易方向为卖出时，此字段必须有值并且大于0
    }
    apply_exchange_agent(env, userReqNo=userReqNo, **exchange_params)
    
    logging.info(f".................等待中..........")
    # time.sleep(84)
    # userReqNo = "6f9b8acc-bee4-4ffd-a514-6ddfded3cc7c"
    confirm_exchange_agent(env, userReqNo)    # 确认汇兑申请
    # cancel_exchange(env, userReqNo, apiType=1)  # 取消汇兑申请
    N += 1