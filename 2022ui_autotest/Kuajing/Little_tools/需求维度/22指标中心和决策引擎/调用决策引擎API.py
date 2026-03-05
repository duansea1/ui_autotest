import requests
import json
import time
from datetime import datetime

# API端点URL
rul_core = "172.23.133.120:10014"  # 修正变量名 rul_core -> url_core
# user_flow = "172.23.6.58:1113"     # 修正非法IP 582->58，变量名改为合法的 user_flow
# admin_core = "172.23.6.9:21802"

url = "http://10.254.224.216:10014/v1/decision/flow/query/api/execute"    #rul_core


print("最终API地址：", url)

# 请求数据
"""
接口文档：7.1.4 决策流执行
URL : POST /front/decision/flow/api/execute       /front/decision/flow/node/api/execute
功能 : 决策流执行
必填参数：
- decisionFlowCode: 决策流 ID
- bizData: 业务数据
- initiatingParty: 调用方(哪个系统发起的调用)
- requestSerialId: 请求流水号(如果是异步请保证该参数唯一性)
- executeType: 执行方式（SYNC，ASYNC）
- operator: 操作人
可选参数：
- callbackType: 回调类型，HTTP（POST）、MQ
- callbackUrl: 异步回调地址（MQ队列、URL），执行方式为异步时必填
- extensionData: 扩展域
"""

""""
 "PAYEE_NAME": "李琳",
    "TRADE_MONTH": "2025-12",
    "TRADE_AMOUNT_1": 0,
    "TRAD_INFO": 2
"""
# FLOW_000048决策流 SEA000001
data = {
    "decisionFlowCode": "SEA007",  # 决策流 CODE   SEA007   SEA000001  SEA0004
    "executeType": "SYNC",  # 执行方式（SYNC，ASYNC）
    "requestSerialId": "uuid-" + datetime.now().strftime("%Y%m%d%H%M%S"),  # 请求流水号
    "initiatingParty": "Python-sea129-SEA000001",  # 调用方
    "operator": "测试sea129-SEA000001",  # 操作人
    "bizData": {
        "PAYEE_NAME": "李琳",
        "USD_AMT_C": 4,
        "TRADE_AMOUNT_1":555,
        "P_IN":41,
        "RATEID_SEA": "7.88",
        "CLIENT_90D_5000USD_ORDER_QTYAMT":11,
        # "ORDER_71":60,
        "externalItemId": 9918209,
        "ABS_ORDERAMT_SUM_QTY_PRICR": 2,  #R01  大于6 flase
        "CLIENT_90D_1000USD_ORDER_QTYAMT": 0,
        "externalOrderId": 2601191010412064676,
        "TAG_ID": "2509021003000524137",
        "FX_BD_TRANAMT": 9999.9,      # 控制R10 、R02 
        "CLIENT_90D_1000USD_ORDER_QTY": "20%",  # R5 >11--TRUE 
        "FX_BD_ITEMNAME": "delllatitude牌",
        "FX_BD_PRICE": "1100.09",   #R6 >1200 --TRUE
        "CLIENT_90D_ORDERAMT": 0,
        "CHANNEL_RATE": 1.209292,
        "CLIENT_LABEL": "东方红,流失客户,潜在流失客户,电商",
        "CLIENT_90D_5000USD_ORDER_QTY": "12%",
        "CLIENT_90D_5000USD_ORDER_QTYAMT": "0",      #R08
        "FX_BD_QTY": 31   #R02       (FX_BD_QTY=31  FX_BD_TRANAMT=4000）-flase   (FX_BD_QTY=20  FX_BD_TRANAMT=4000）-flase
    },  #指标中心传入的参数值(指标code)
    "extensionData": {}
}
# 发送请求
# r = requests.post(url, json=data, headers={"Content-Type": "application/json", "accept": "*/*"})
# 电商结汇需要的参数值 NEW_FX_BD_DIANSHANG
biz_data = {
    "externalItemId": 9918209,
    "ABS_ORDERAMT_SUM_QTY_PRICR": 6,  #R01  大于6 flase
    "CLIENT_90D_1000USD_ORDER_QTYAMT": 0,
    "externalOrderId": 2601191010412064676,
    "TAG_ID": "2509021003000524137",
    "FX_BD_TRANAMT": 5799.9,      # 控制R10 、R02 
    "CLIENT_90D_1000USD_ORDER_QTY": "12",  # R5 >11--TRUE 
    "FX_BD_ITEMNAME": "delllatitude牌包",
    "FX_BD_PRICE": "1100.09",   #R6 >1200 --TRUE
    "CLIENT_90D_ORDERAMT": 0,
    "CHANNEL_RATE": 1.209292,
    "CLIENT_LABEL": "东方红,流失客户,潜在流失客户,电商",
    "CLIENT_90D_5000USD_ORDER_QTY": "12%",
    "CLIENT_90D_5000USD_ORDER_QTYAMT": "0",      #R08
    "FX_BD_QTY": 31   #R02       (FX_BD_QTY=31  FX_BD_TRANAMT=4000）-flase   (FX_BD_QTY=20  FX_BD_TRANAMT=4000）-flase
}

# 决策需要的参数数据
data = {
    "decisionFlowCode": "NEW_FX_BD_DIANSHANG",  # 决策流 CODE
    "executeType": "SYNC",  # 执行方式（SYNC，ASYNC）
    "requestSerialId": "uuid-" + datetime.now().strftime("%Y%m%d%H%M%S"),  # 请求流水号
    "initiatingParty": "Python-sea129电商结汇",  # 调用方
    "operator": "测试sea-电商结汇",  # 操作人
    "bizData": biz_data,  #指标中心传入的参数值(指标code)
    "extensionData": {}
}


# 发送请求
r = requests.post(url, json=data, headers={"Content-Type": "application/json", "accept": "*/*"})

# 打印原始响应
excue_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f'------开始执行时间：{excue_time}----开始执行打印返回结果')
print("=== 原始响应 ===")
print(f"状态码: {r.status_code}")
print(f"原始响应内容: {r.text}")

# 解析并格式化完整的JSON响应
print("\n=== 优化后响应 ===")
if r.status_code == 200:
    try:
        # 解析完整的JSON响应
        full_response = r.json()
        
        # 打印格式化后的完整响应
        print(json.dumps(full_response, indent=2, ensure_ascii=False))
        
        # 打印决策结果
        print("\n=== 决策结果 ===")
        if "result" in full_response:
            result_data = full_response["result"]
            if "decisionEndDto" in result_data:
                decision = result_data["decisionEndDto"]
                print(f"🎉决策: {decision.get('decision', '未知')}")
                print(f"决策原因: {decision.get('decisionReason', '未知')}")
        
        # 打印规则执行结果
        print("\n=== 规则执行结果 ===")
        if "result" in full_response:
            result_data = full_response["result"]
            if "steps" in result_data:
                for step in result_data["steps"]:
                    print(f"结果: {step.get('isSuccess', '未知')}--{step.get('ruleId', '未知')}--步骤 {step.get('step', '未知')}: {step.get('ruleName', '未知')}")
                    # print(f"  结果: {step.get('result', '未知')}")
                    # print(f"  是否通过: {step.get('isSuccess', '未知')}")
                    # print(f"  规则ID: {step.get('ruleId', '未知')}")
                    print("  --------------------")
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
else:
    print(f"请求失败，状态码: {r.status_code}")

print(f'------开始执行时间-目前已执行结束：{excue_time}------------------------')
