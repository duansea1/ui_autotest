# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-11-25 10:30
# ---
from Common import publicTools as p
from Common import enviromments as enc
from icecream import ic
import time


# ic.configureOutput(prefix='DEBUG: ')
ic.configureOutput(includeContext=True)


def query_rate(env):
    """查询汇率-默认查的是biz_type=1的"""
    # 获取秘钥相关信息

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/rate/query-rate"

    # 卖出方向
    data1 = {
        "userNo": data_env.get('userNo'),
        "originalCcy": "CNH",  # 买入
        "targetCcy": "USD",  # 卖出币种
        "closingDate": p.generate_dates()
    }
    # 买入方向
    data = {
        "userNo": data_env.get('userNo'),
        "originalCcy": "USD",  # 买入
        "targetCcy": "CNH",  # 卖出币种
        "closingDate": p.generate_dates()
    }
    ic(data)
    p.rsa_and_send_request(data, env, url, apiType=2)



def b2b_query_rate(env):
    """此汇率查询接口是按照固定币种对方向返回汇率，币种对方向一致时返回卖出价，币种对方向相反则返回买入价。
            业务类型暂支持取值：
        6：B2B结汇付款汇率，
        7：B2B国际分发汇率
        8：B2B兑换汇率
        示例：如币种对 USD/CNH

        卖出USD->买入CNH，则返回7.231900,表示：卖出1 USD可以换7.231900 CNH
        卖出CNH->买入USD，则返回7.260700,表示：买入1 USD需要7.260700 CNH"""
    # 获取秘钥相关信息

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/rate/query-rate"

    data = {
          "bizType":"8",
          "closingType":"SPOT",
          "originalCcy":"CNH",
          "targetCcy":"USD"
    }
    ic(data)
    p.rsa_and_send_request(data, env, url, apiType=3)

def b2b_cal_query_rate(env):
    """B2B商户计算汇率查询
        此汇率查询接口按照实际卖出币种换算。
        示例：

        卖出USD->买入CNH，则返回7.2,表示：1 USD=7.2 CNH
        卖出CNH->买入USD，则返回0.13,表示：1 CNH = 0.13 USD"""
    # 获取秘钥相关信息

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/rate/query-b2b-cal-rate"

    data = {
        "userNo": data_env.get('userNo'),
        "closingDate": "2025-04-08",
        "originalCcy": "CNH",
        "targetCcy": "USD"
    }
    ic(data)
    p.rsa_and_send_request(data, env, url, apiType=3)

""" GEP汇兑锁定申请 """
def apply_exchange(env, userReqNo, closingType="TOD", closingDate="2024-12-12", deliveryType="MANUAL", tradeModel=2):
    """ GEP汇兑锁定申请"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/exchange/apply-exchange"

    data = {
        "userNo": data_env.get('userNo'),
        "userReqNo": userReqNo,
        "buyCcy": "EUR",  # 买入币种
        "buyAmount": 10,  # 买入金额，交易方向为买入时，此字段必须有值并且大于0
        "sellCcy": "CNH",  # 卖出币种
        "sellAmount": 1,  # 卖出金额，交易方向为卖出时，此字段必须有值并且大于0
        "closingDate": closingDate, # 交割日期，格式为 YYYY-MM-DD
        "closingType": closingType,  # TOD:立即交割，账户余额一定要有资金才行 TOM:T+1日交割 SPOT:T+2日交割
        "direction": "1",  # 1-买入  2-卖出
        "tradeModel": tradeModel,   # 1-实时  2-预约
        "deliveryType": deliveryType,  # 交割方式：AUTO-自动交割 MANUAL-手动交割
        "callbackUrl": "http://www.baidu.com/seasea"
    }
    ic(data)
    # 开始加密操作
    rsa_utils, dataContent = p.rsa_generate(data, env)

    # 构建请求数据 apiType=1 代理商 2-商户本身
    dataMap = p.data_Map(data_env, dataContent, apiType=2)
    # dataMap = {
    #     "version": "1.0.0",
    #     "certificateId": data_env.get('certificateId'),
    #     "dataType": "JSON",
    #     "dataContent": dataContent,
    #     "userNo": data_env.get('userNo'),
    #     "agentNo": "eee",
    #     "apiType": "2"  # 1-代理商  2-商户
    #
    # }
    ic(dataMap)

    # 发送请求
    p.send_request(rsa_utils, url, dataMap)

def apply_exchange_agent(env, userReqNo, closingType = "TOD", closingDate="2024-12-12", deliveryType="MANUAL", tradeModel=2, direction=1):
    """ B2B汇兑锁定申请-B2b汇兑"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/exchange/apply-exchange"

    data = {
        "userNo": data_env.get('userNo'),
        "userReqNo": userReqNo,
        "buyCcy": "USD",  # 买入币种
        "buyAmount": 1,  # 买入金额，交易方向为买入时，此字段必须有值并且大于0
        "sellCcy": "CNH",  # 卖出币种
        "sellAmount": 1,  # 卖出金额，交易方向为卖出时，此字段必须有值并且大于0
        "closingDate": closingDate,   # 交割日期，格式为 YYYY-MM-DD
        "closingType": closingType,  # TOD:立即交割，账户余额一定要有资金才行 TOM:T+1日交割 SPOT:T+2日交割
        "direction": direction,  # 1-买入  2-卖出
        "tradeModel": tradeModel,   # 1-实时  2-预约
        "deliveryType": deliveryType,  # 交割方式：AUTO-自动交割 MANUAL-手动交割
        "callbackUrl": "http://www.baidu.com/seasea"
    }
    ic(data)
    # 开始加密操作
    rsa_utils, dataContent = p.rsa_generate(data, env)

    # 生成
    dataMap = p.data_Map(data_env, dataContent, apiType=1)
    # dataMap = {
    #     "version": "1.0.0",
    #     "certificateId": data_env.get('certificateId'),
    #     "dataType": "JSON",
    #     "dataContent": dataContent,
    #     "userNo": data_env.get('userNo'),
    #     "agentNo": "11111",
    #
    #
    # }
    # ic(dataMap)

    # 发送请求
    p.send_request(rsa_utils, url, dataMap)

""" GEP汇兑锁定确认"""
def confirm_exchange(env, userReqNo, apiType):
    """ GEP汇兑锁定确认"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/exchange/confirm-exchange"

    data = {
        "userNo": data_env.get('userNo'),
        "userReqNo": userReqNo,
    }
    ic(data)
    # 开始加密操作
    rsa_utils, dataContent = p.rsa_generate(data, env)

    # 构建请求数据
    dataMap = p.data_Map(data_env, dataContent, apiType)
    ic(dataMap)

    # 发送请求
    p.send_request(rsa_utils, url, dataMap)


def confirm_exchange_agent(env, userReqNo, apiType=1):
    """ GEP汇兑锁定确认"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/exchange/confirm-exchange"

    data = {
        "userNo": data_env.get('userNo'),
        "userReqNo": userReqNo,
    }
    ic(data)

    # 开始加密操作
    rsa_utils, dataContent = p.rsa_generate(data, env)

    # 构建请求数据
    dataMap = p.data_Map(data_env, dataContent, apiType)
    ic(dataMap)

    # 发送请求
    p.send_request(rsa_utils, url, dataMap)


def cancel_exchange(env, userReqNo, apiType):
    """
    汇兑锁定取消
    """
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/exchange/cancel-exchange"

    data = {
        "userNo": data_env.get('userNo'),
        "userReqNo": userReqNo,
    }
    ic(data)
    # 开始加密操作
    rsa_utils, dataContent = p.rsa_generate(data, env)

    # 构建请求数据
    dataMap = p.data_Map(data_env, dataContent, apiType)
    ic(dataMap)

    # 发送请求
    p.send_request(rsa_utils, url, dataMap)

""" B2B查询商户计算汇率"""
def query_b2b_cal_rate(env):
    """ B2B查询商户计算汇率"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/rate/query-b2b-cal-rate"

    data = {
        "userNo": data_env.get('userNo'),
        "originalCcy": "CNH",   # 买入币种
        "targetCcy": "USD",  # 卖出币种
        "closingDate": "2024-12-05",
    }
    ic(data)
    # 开始加密操作
    rsa_utils, data_content = p.rsa_generate(data, env)

    # 构建请求数据
    datamap = p.data_Map(data_env, data_content, apiType=2)
    ic(datamap)

    # 发送请求
    p.send_request(rsa_utils, url, datamap)

def exchange_delivery(env, userReqNo, apiType=1):
    """
    2.3.53 交割申请接口
    注意：依赖 -汇率申请接口 apply_exchange()---汇兑确认接口confirm_exchange()
    """
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/exchange/exchange-delivery"
    data = {
            "userNo": data_env.get('userNo'),
            "userReqNo": userReqNo,
            }

    ic(data)
    # 开始加密操作
    rsa_utils, dataContent = p.rsa_generate(data, env)

    # 构建请求数据
    dataMap = p.data_Map(data_env, dataContent, apiType)
    ic(dataMap)

    # 发送请求
    p.send_request(rsa_utils, url, dataMap)

def exchange_modify_delivery_agent(env, userReqNo, deliveryType="AUTO"):
    """ 2.3.52 汇兑修改交割方式"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/exchange/exchange-modify-delivery"

    data = {
        "userNo": data_env.get('userNo'),
        "userReqNo": userReqNo,
        "deliveryType": deliveryType  # 交割方式AUTO自动交割 MANUAL手动交割
    }
    ic(data)
    # 开始加密操作
    rsa_utils, dataContent = p.rsa_generate(data, env)

    # 构建请求数据
    dataMap = p.data_Map(data_env, dataContent, apiType=1)
    ic(dataMap)
    # 发送请求
    p.send_request(rsa_utils, url, dataMap)

def query_exchange_order(env, userReqNo):
    """ 2.3.9 GEP汇兑订单查询"""

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/exchange/query-exchange-order"

    data = {
        "userNo": data_env.get('userNo'),
        "userReqNo": userReqNo,  # 商户订单号，在汇兑锁定申请中请求的单号
    }
    ic(data)
    # 开始加密操作
    rsa_utils, dataContent = p.rsa_generate(data, env)

    # 构建请求数据 2-商户 3-代理商和商户
    dataMap = p.data_Map(data_env, dataContent, apiType=2)
    ic(dataMap)
    # 发送请求
    p.send_request(rsa_utils, url, dataMap)


def query_agent_exchange_order(env, userReqNo):
    """ B2B汇兑订单查询"""

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/exchange/query-exchange-order"

    data = {
        "userNo": data_env.get('userNo'),
        "userReqNo": userReqNo,  # 商户订单号，在汇兑锁定申请中请求的单号
    }
    ic(data)
    # 开始加密操作
    rsa_utils, dataContent = p.rsa_generate(data, env)

    # 构建请求数据 2-商户 3-代理商和商户
    dataMap = p.data_Map(data_env, dataContent, apiType=3)
    ic(dataMap)
    # 发送请求
    p.send_request(rsa_utils, url, dataMap)

if __name__ == '__main__':
    """
    fat:代理商 fat-sea-agent-hzl
    uat:代理商 uat-sea-agent-hzl
    prod: 代理商 prod-sea-agent-dhf
    
    """
    fat_env = "fat-sea-agent-hzl"
    # fat_env = "uat-sea-agent-hzl"
    # fat_env = "fat-sea-wu"
    fat_env = "uat-sea-ss"  # uat环境 其他企业丝丝
    # fat_env = ""fat-sea-tx""
    fat11_env = "prod-sea-agent-dhf"  # 生产环境TODO
    # prod_env = "prod-sea-agent-dhf"
    # 代理商
    query_rate(env=fat_env)
    # b2b_query_rate(env=fat_env)
    # b2b_cal_query_rate(env=fat_env)
    # 商户
    # query_rate(env="fat-sea-wu")

    """GEP汇兑锁定申请-done"""
    # apply_exchange(env="uat-sea-ss")
    userReqNo = int(time.time())
    # userReqNo = "a20296fb-2f3d-4cba-8470-3de555fdc843"

    """GEP汇兑锁定申请-done"""
    # apply_exchange(env=fat_env, userReqNo=userReqNo, closingType="TOM",
    #                      closingDate=p.generate_dates(day_offset=1), deliveryType="AUTO", tradeModel=2)  # TODO 汇兑申请

    # apply_exchange(env=fat_env, userReqNo=userReqNo, closingType="TOM", closingDate="", deliveryType="MANUAL", tradeModel=2)
    # MANUAL-手动交割 prod-sea-agent-dhf   --prod  MANUAL-手动交割
    """B2B汇兑申请-done"""
    # apply_exchange_agent(env=fat_env, userReqNo=userReqNo, closingType="TOD",closingDate="", deliveryType="MANUAL")  # TODO-跨境b2b 汇兑申请
    # query_exchange_order(env="uat-sea-tx", userReqNo=userReqNo)  # TODO-# 2.3.9 GEP汇兑订单查询-done 汇兑订单查询
    # time.sleep(1)
    """GEP汇兑锁定确认 -done"""
    # confirm_exchange(env="uat-sea-tx", userReqNo=userReqNo, apiType=2)
    # confirm_exchange(env=fat_env, userReqNo=userReqNo, apiType=2)    # TODO-2 GEP汇兑锁定确认-商户
    # confirm_exchange_agent(env=fat_env, userReqNo=userReqNo)  # TODO-跨境b2b 汇兑单确认--代理商
    # confirm_exchange(env=uat_env, userReqNo=userReqNo)

    """GEP汇兑申请取消  -done"""
    # cancel_exchange(env="fat-sea-agent-hzl", userReqNo=userReqNo, apiType=3)  # TODO-4 汇兑申请取消
    # cancel_exchange(env="uat-sea-tx", userReqNo=userReqNo, apiType=2)  # TODO-4 汇兑申请取消-商户

    """ B2B查询商户计算汇率-done"""
    # query_b2b_cal_rate(env="uat-sea-ss")

    """修改交割方式-done"""
    # exchange_modify_delivery_agent(env=fat_env, userReqNo=userReqNo, deliveryType="AUTO")
    #
    # """2.3.49 GEP汇兑交割申请 -done"""
    # exchange_delivery(env="uat-sea-tx", userReqNo=userReqNo,apiType=2)

    """2.3.9 GEP汇兑订单查询-done"""
    # query_exchange_order(env="uat-sea-tx", userReqNo=userReqNo)  # TODO-# 2.3.9 GEP汇兑订单查询-done 汇兑订单查询
    # query_agent_exchange_order(env="uat-sea-agent-hzl", userReqNo=userReqNo)  # TODO-# b2b汇兑订单查询-done 汇兑订单查询


