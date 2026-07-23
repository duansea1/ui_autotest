import requests
import json
import time
from datetime import datetime

# API端点URL
url = "http://10.254.224.216:10014/v1/decision/flow/query/api/execute"

print("最终API地址：", url)

# 请求数据
"""
接口文档：7.1.4 决策流执行
URL : POST /front/decision/flow/api/execute
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

# 电商结汇需要的参数值 NEW_FX_BD_DIANSHANG
biz_data = {
   "externalItemId": "9985367",
  "ABS_ORDERAMT_SUM_QTY_PRICR": "1.99",
  "CLIENT_90D_1000USD_ORDER_QTYAMT": "0",
  "externalOrderId": "2602091005419414106",
  "TAG_ID": "2509021003000524137",
  "FX_BD_TRANAMT": "19998.01",
  "CLIENT_90D_1000USD_ORDER_QTY": "0",
  "FX_BD_ITEMNAME": "雪花秀商品",
  "FX_BD_PRICE": "500",
  "CLIENT_90D_ORDERAMT": "0",
  "CHANNEL_RATE": "0.278841947",
  "CLIENT_LABEL": "东方红",
  "CLIENT_90D_5000USD_ORDER_QTY": "0",
  "CLIENT_90D_5000USD_ORDER_QTYAMT": "0",
  "FX_BD_QTY": "10"
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
                print(f"决策: {decision.get('decision', '未知')}")
                print(f"决策原因: {decision.get('decisionReason', '未知')}")

        # 打印规则执行结果
        print("\n=== 规则执行结果 ===")
        if "result" in full_response:
            result_data = full_response["result"]
            if "steps" in result_data:
                rule_index = 0  # 规则编号计数器
                for step in result_data["steps"]:
                    # 获取各个字段，当ruleName或ruleId为未知时使用nodeName
                    rule_id = step.get('ruleId', '未知')
                    rule_name = step.get('ruleName', '未知')
                    node_name = step.get('nodeName', '未知')

                    # 如果ruleId或ruleName是未知，使用nodeName
                    display_rule_id = rule_id if rule_id != '未知' else node_name
                    display_rule_name = rule_name if rule_name != '未知' else node_name

                    # 如果是结束节点，不加编号
                    if "结束节点" in node_name:
                        print(f"结果: {step.get('isSuccess', '未知')}--{display_rule_id}--步骤 {step.get('step', '未知')}: {display_rule_name}")
                    else:
                        rule_index += 1
                        print(f"{rule_index}、结果: {step.get('isSuccess', '未知')}--{display_rule_id}--步骤 {step.get('step', '未知')}: {display_rule_name}")
                    print("  --------------------")
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
else:
    print(f"请求失败，状态码: {r.status_code}")

print(f'------开始执行时间-目前已执行结束：{excue_time}------------------------')
