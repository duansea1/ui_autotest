import requests
import json

def channel_balance_query(env=None):
    """ 渠道余额查询API调用 """
    
    # 从API文档中提取的信息
    url = "https://fat-global-ad.baofu.com/ams-api/rate-manage/channel-balance-query/balance-query"
    
    # Token信息
    token = "eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3NjY1NTQ1MzR9.u4GH3fx7DYC6TzdWo9hh2PLf7FTdE8XP1WPyEjPRLGAMch9uFNwfOFLgLvbZg6V4tXOoXGT6GbVt3YtSVa6oXg"
    
    # 请求头
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://fat-global-ad.baofu.com',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': f'agent-control-core-token={token}'
    }
    
    # 渠道ID和名称映射关系
    channel_mapping = {
        1200923072: "DBS 货币兑换",
        1000000001:"DBS清结算",
        1200923086: "渣打-【清结算信息】",
        1200923091: "渣打FX-【渣打清结算】",

    }
    
    # 请求体
    payload = {
        "channelIds": [1200923072, 1200923086],
        "accountCcy": "EUR",
        "isRealTime": False
    }
    # 请求体
    payload = {
        "channelIds": [1200923072],
        "accountCcy": "CNH",
        "isRealTime": True
    }
    
    # 发送POST请求
    try:
        print(f"=== 渠道余额查询API调用 ===")
        
        # 发送请求
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            verify=False,
            allow_redirects=False,
            proxies={}  # 禁用代理
        )
        
        # 打印响应状态码
        print(f"\n响应状态码: {response.status_code}")
        print(f"实际请求URL: {response.url}")
        
        # 解析JSON响应
        try:
            response_json = response.json()
            print(f"\nJSON解析结果: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
            
            # 提取响应接口数据
            if response_json.get("message") == "成功" and "result" in response_json:
                print(f"\n=== 渠道余额信息 ===")
                
                for channel_info in response_json.get("result", []):
                    channel_id = channel_info.get("channelId")
                    account_ccy = channel_info.get("accountCcy")
                    available_bal = channel_info.get("availableBal")
                    
                    # 获取渠道名称
                    channel_name = channel_mapping.get(channel_id, f"未知渠道-{channel_id}")
                    
                    # 打印格式1：完整格式
                    print(f"{channel_id}-{channel_name}   卖出{account_ccy}币种，对应的渠道表余额是 {available_bal}")
                    
                    # 打印格式2：简化格式
                    print(f"{channel_id}-{channel_name.split('-')[0]}-卖出{account_ccy}，对应渠道表的余额是{available_bal}")
                    print()
            
            return response_json
        except json.JSONDecodeError:
            print("\n无法解析为JSON")
            print(f"响应内容: {response.text}")
            return response.text
            
    except Exception as e:
        print(f"\n请求出错: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    # 查询渠道余额
    channel_balance_query()
