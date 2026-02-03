import requests
import json
import time
from datetime import datetime

url = "http://172.23.6.41:10015/metric-center/run"
# data = {
#     "groupCodes": ["BXY_TEST"],  # 指标分组code
#     # "metricCodes": ["string"],  # 指标code
#     # "modularCodes": ["string"], #模块code
#     "paramsMap": {
#         "USER_NO": 5181230111000551688,
#         "externalOrderId": 2410151706001070808,
#         "externalItemId": 612505
#     },
#     "requestBy": "测试sea",
#     "requestId": "sea00000001",
#     "requestReason": "测试sea Python调用"
# }
""" 
QA_GROUP---质量部可见
44444--潜在客户可见
参数：
USER_NO：5181230111000551688、5181240628000024148-桐乡
externalOrderId：2601191010412064676 -桐乡
externalItemId：9918209-桐乡



"""
data = {
    "groupCodes": ["ARIATEST"],  # 指标分组code
    # "metricCodes": ["string"],  # 指标code
    # "modularCodes": ["string"], #模块code
    "paramsMap": {
        # "USER_NO": "5181240628000024141",
        "USER_NO": "5181240628000024148",
        "externalOrderId": 2601291121414967928,
        "externalItemId": 9919549,
        "ORIGINAL_CCY":"EUR"
    },
    "requestBy": "测试sea-系统",
    "requestId": "sea00001-"+datetime.now().strftime("%Y%m%d%H%M"),
    "requestReason": "测试sea Python调用" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# 发送请求
r = requests.post(url, json=data, headers={"Content-Type": "application/json", "accept": "*/*"})

# 打印原始响应
print("=== 原始响应 ===")
print(f"状态码: {r.status_code}")
print(f"原始响应内容: {r.text}")

# 解析并格式化完整的JSON响应
print("\n=== 优化后响应 ===")
if r.status_code == 200:
    try:
        # 解析完整的JSON响应
        full_response = r.json()
        
        # 解析result字段（如果存在的话）
        if 'result' in full_response and full_response['result']:
            try:
                # 格式化result字段内的JSON字符串
                full_response['result'] = json.loads(full_response['result'])
            except json.JSONDecodeError:
                # 如果result不是有效的JSON字符串，保持原样
                pass
        
        # 打印格式化后的完整响应
        print(json.dumps(full_response, indent=2, ensure_ascii=False))
        
        # 校验是否缺少指定字段
        print("\n=== 字段校验结果 ===")
        # 定义需要校验的字段字典，包含字段名称和描述
        required_fields = {
            "ABS_ORDERAMT_SUM_QTY_PRICR": "商品数量*商品单价 的绝对值（订单金额原始合计）-1",
            "CHANNEL_RATE": "汇率-2",
            "FX_BD_QTY": "商品数量-3",
            "FX_BD_TRANAMT": "交易金额（原始币种）-4",
            "FX_BD_PRICE": "商品单价（原始币种）-5",
            "CLIENT_90D_1000USD_ORDER_QTY": "商户近90天内商品单价 >1000 USD的订单数量-6",
            "CLIENT_90D_5000USD_ORDER_QTYAMT": "商户近90天内交易金额 >5000 USD 的订单数量-7",
            "FX_BD_ITEMNAME": "商品名称-8",
            "CLIENT_LABEL": "商户标签-9"
        }
        
        # 检查字段是否存在
        missing_fields = []
        existing_fields = []
        
        # 检查result字段是否存在且是字典
        if 'result' in full_response and isinstance(full_response['result'], dict):
            result_data = full_response['result']
            # 检查每个必填字段
            for field, description in required_fields.items():
                if field not in result_data:
                    missing_fields.append((field, description))
                else:
                    existing_fields.append((field, description, result_data[field]))
        else:
            print("错误：响应中没有有效的result字段或result不是字典格式")
        
        # 输出校验结果
        if missing_fields:
            print("🚀🚀🚀缺少以下字段🚀🚀🚀：")
            for field, description in missing_fields:
                print(f"- {field} ({description})")
        else:
            print("🚀🚀所有指定字段都存在")
        
        # 输出存在字段的值
        if existing_fields:
            print("\n=== 存在字段详情 ===")
            for field, description, value in existing_fields:
                print(f"{field}: {value} ({description})")
            
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
else:
    print(f"请求失败，状态码: {r.status_code}")
