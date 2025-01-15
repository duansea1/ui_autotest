# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-11-25 10:30
# ---
from Common import publicTools as p
from Common import enviromments as enc
from icecream import ic


# ic.configureOutput(prefix='DEBUG: ')
ic.configureOutput(includeContext=True)


def query_rate(env):
    """查询汇率-默认查的是biz_type=1的"""
    # 获取秘钥相关信息

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/rate/query-rate"

    data = {
        "userNo": data_env.get('userNo'),
        "originalCcy": "CNH",  # 买入
        "targetCcy": "USD",  # 卖出币种
        "closingDate": p.generate_dates()
    }
    ic(data)
    p.rsa_and_send_request(data, env, url, apiType=3)

""" GEP汇兑锁定申请"""
def apply_exchange(env, userReqNo):
    """ GEP汇兑锁定申请"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/exchange/apply-exchange"

    data = {
        "userNo": data_env.get('userNo'),
        "userReqNo": userReqNo,
        "buyCcy": "CNH",  # 买入币种
        "buyAmount": 1,  # 买入金额，交易方向为买入时，此字段必须有值并且大于0
        "sellCcy": "USD",  # 卖出币种
        "sellAmount": 1,  # 卖出金额，交易方向为卖出时，此字段必须有值并且大于0
        "closingDate": p.generate_dates(day_offset=0),
        "closingType": "TOD",
        "direction": "2",  # 1-买入  2-卖出
        "tradeModel": 1,   # 1-实时  2-预约
        "deliveryType": "MANUAL",  # 交割方式：AUTO-自动交割 MANUAL-手动交割
        # "callbackUrl": ""
    }
    ic(data)
    # 开始加密操作
    rsa_utils, dataContent = p.rsa_generate(data, env)

    # 构建请求数据 apiType=1 代理商 2-商户本身
    dataMap = p.data_Map(data_env, dataContent, apiType=3)
    dataMap = {
        "version": "1.0.0",
        "certificateId": data_env.get('certificateId'),
        "dataType": "JSON",
        "dataContent": dataContent,
        "userNo": data_env.get('userNo'),
        "agentNo": "eee",
        "apiType": "2"  # 1-代理商  2-商户

    }
    ic(dataMap)

    # 发送请求
    p.send_request(rsa_utils, url, dataMap)

def apply_exchange_agent(env, userReqNo, closingType="TOD", closingDate="2024-12-12", deliveryType="MANUAL"):
    """ GEP汇兑锁定申请"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/exchange/apply-exchange"

    data = {
        "userNo": data_env.get('userNo'),
        "userReqNo": userReqNo,
        "buyCcy": "CNH",  # 买入币种
        "buyAmount": 1,  # 买入金额，交易方向为买入时，此字段必须有值并且大于0
        "sellCcy": "USD",  # 卖出币种
        "sellAmount": 0.99,  # 卖出金额，交易方向为卖出时，此字段必须有值并且大于0
        "closingDate": closingDate,
        "closingType": closingType,
        "direction": "2",  # 1-买入  2-卖出
        "tradeModel": 2,   # 1-实时  2-预约
        "deliveryType": deliveryType,  # 交割方式：AUTO-自动交割 MANUAL-手动交割
        # "callbackUrl": ""
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
    ic(dataMap)

    # 发送请求
    p.send_request(rsa_utils, url, dataMap)

""" GEP汇兑锁定确认"""
def confirm_exchange(env, userReqNo):
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
    dataMap = p.data_Map(data_env, dataContent, apiType=3)
    ic(dataMap)

    # 发送请求
    p.send_request(rsa_utils, url, dataMap)


def confirm_exchange_agent(env, userReqNo):
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
    dataMap = p.data_Map(data_env, dataContent, apiType=1)
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

def exchange_delivery(env, userReqNo):
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
    dataMap = p.data_Map(data_env, dataContent, apiType=3)
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

    # 构建请求数据
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
    uat_env = "uat-sea-agent-hzl"
    # prod_env = "prod-sea-agent-dhf"
    # 代理商
    # query_rate(env=fat_env)
    # 商户
    query_rate(env="fat-sea-wu")

    """GEP汇兑锁定申请-done"""
    # apply_exchange(env="uat-sea-ss")
    userReqNo = "20250115000001"

    apply_exchange(env="uat-sea-ss", userReqNo=userReqNo)

    # apply_exchange(env="fat-sea-tx", userReqNo=userReqNo)
    # MANUAL-手动交割 prod-sea-agent-dhf   --prod
    # apply_exchange_agent(env=uat_env, userReqNo=userReqNo, closingType="TOD",
    #                      closingDate="2025-01-02", deliveryType="AUTO")  # TODO-1
    # time.sleep(3)
    """GEP汇兑锁定确认 -done"""
    # confirm_exchange(env="fat-sea-tx", userReqNo=userReqNo)
    # confirm_exchange_agent(env=uat_env, userReqNo=userReqNo)  # TODO-2 汇兑单确认
    # confirm_exchange(env=uat_env, userReqNo=userReqNo)

    """ B2B查询商户计算汇率-done"""
    # query_b2b_cal_rate(env="uat-sea-ss")

    # 修改交割方式-done
    # exchange_modify_delivery_agent(env=fat_env, userReqNo=userReqNo, deliveryType="AUTO")

    # 2.3.49 GEP汇兑交割申请 -done
    # exchange_delivery(env="uat-sea-agent-hzl", userReqNo=userReqNo)

    # 2.3.9 GEP汇兑订单查询-done
    # query_exchange_order(env="prod-sea-agent-dhf", userReqNo=userReqNo)  # TODO-3


