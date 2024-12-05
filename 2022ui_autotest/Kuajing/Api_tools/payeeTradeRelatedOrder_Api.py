# -*- coding: utf-8 -*-
# ---
# 入账交易关联申报订单
# @Time: 2024-11-25 10:30
# ---
from commons.RSAUtil import *
import requests
import json
from Kuajing.Common import publicTools
from Kuajing.Common import enviromments as enc
from icecream import ic
# ic.configureOutput(prefix='DEBUG: ')
ic.configureOutput(includeContext=True)


def payeeTradeRelatedOrder(env):
    """查询汇率"""
    # 获取秘钥相关信息
    dataenv = enc.get_envs(env)
    pfxpath = dataenv.get('pfxpath')
    pfxpass = dataenv.get('pfx_pass')
    cerpath = dataenv.get('cerpath')
    agentNo = dataenv.get('agentNo')
    base_url = dataenv.get('url')
    certificateId = dataenv.get('certificateId')

    data = {
        "userNo": dataenv.get('userNo'),
        "detailId": "2411281625288629191",  # 入账交易的交易单号
        "relationSettleOrderDetailList": [{
            "orderId": "2411281414288619187",  # 结汇订单明细接口返回的orderId
            "relationOrderAmt": 17
        }],
        "supplementMaterialList": [{
            "materialId": "13459292",
            "materialName": "企业^_^火狐.png"}
        ],   # 新增的两个参数
        "userRemarks": "api新增的备注"

    }
    ic(data)
    # 开始加密操作
    json_str = publicTools.jsonString(data)  # JSON 格式的字符串
    rsa_util = RSAUtil(pfx_path=pfxpath, pfxpass=pfxpass, cer_path=cerpath)
    dataContent = rsa_util.pri_encrypt(json_str)  # RSA加密

    # 入账交易关联申报订单接口
    url = f"{base_url}/api/agent/declarationOrder/payeeTradeRelatedOrder"

    # 构建请求数据
    dataMap = {
        "certificateId": certificateId,
        "dataContent": dataContent,
        "dataType": "JSON",
        "version": "1.0.0",
        "agentNo": agentNo,
    }
    ic(dataMap)
    # 定义请求头
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # 发送HTTP POST请求
    response = requests.post(url=url, data=dataMap, headers=headers,verify=False)

    if response.status_code == 200:
        try:
            response_data = response.json()  # 解析JSON响应
            if response_data.get('result'):
                result = response_data.get('result')  # 提取result字段
                print("响应结果：", response_data)
                # print("提取的result字段：", result)
                result = rsa_util.pub_decrypt(result)  # RSA解密
                ic("=====================打印解密结果：===================")
                ic(result)
                return result
            else:
                ic(response_data)
                return response_data
        except json.JSONDecodeError as e:
            print(f"解析JSON失败：{e}")
            return None
    else:
        print(f"请求失败：{response.text}")
        return None


if __name__ == '__main__':
    # 代理商
    payeeTradeRelatedOrder(env="fat-sea-agent-hzl")


