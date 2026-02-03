import logging
import requests
import json

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def query_trader_profit(ccy_group_list, closing_begin_date, closing_end_date, token, env='FAT'):
    """
    查询交易员收益信息
    
    参数:
    ccy_group_list: list, 货币对列表，如 ["USD/CNH"]
    closing_begin_date: str, 交割开始日期，格式：YYYY-MM-DD
    closing_end_date: str, 交割结束日期，格式：YYYY-MM-DD
    token: str, 认证token
    env: str, 环境，默认FAT
    
    返回:
    list: 包含交易员收益信息的列表，每个元素包含trader_profit_loss, trade_amount, profit_loss_currency
    """
    # 环境配置
    env_config = {
        'FAT': {
            'base_url': 'https://fat-global-ad.baofu.com',
            'api_path': '/ams-api/rate-manage/receipt-positions/queryPage'
        }
    }
    
    # 获取环境对应的配置
    config = env_config.get(env, env_config['FAT'])
    url = f"{config['base_url']}{config['api_path']}"
    
    # 打印入参日志
    logging.info(f"查询交易员收益入参：ccyGroupList={ccy_group_list}, closingBeginDate={closing_begin_date}, closingEndDate={closing_end_date}")
    
    # 请求头
    headers = {
        'Host': 'fat-global-ad.baofu.com',
        'sec-ch-ua-platform': '"Windows"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'Content-Type': 'application/json',
        'request-system-name': 'baofu-admin-control-client-vue',
        'sec-ch-ua-mobile': '?0',
        'Accept': '*/*',
        'Origin': 'https://fat-global-ad.baofu.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://fat-global-ad.baofu.com/new/account/ams/main/global-rate-manege/rate-risk-manage/rate-position-management',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': f'agent-control-core-token={token}'
    }
    
    # 请求体
    payload = {
        "ccyGroupList": ccy_group_list,
        "currentPage": 1,
        "pageSize": 10,
        "closingBeginDate": closing_begin_date,
        "closingEndDate": closing_end_date
    }
    
    try:
        # 发送请求
        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        logging.info(f"API响应：{json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get('code') == '0':
            # 提取结果
            data_list = []
            for item in result['result']['list']:
                profit_ccy = item['profitCcy']
                sale_ccy = item['saleCcy']
                buy_ccy = item['buyCcy']
                
                # 计算trade_amount：根据profitCcy决定取buyAmount还是saleAmount
                if profit_ccy == sale_ccy:
                    trade_amount = item['saleAmount']
                else:
                    trade_amount = item['buyAmount']
                
                # 提取所需字段
                trader_profit_loss = item['traderProfit']
                profit_loss_currency = profit_ccy
                
                # 添加到结果列表
                data_list.append({
                    'trader_profit_loss': trader_profit_loss,
                    'trade_amount': trade_amount,
                    'profit_loss_currency': profit_loss_currency,
                    'ccy_group': item['ccyGroup'],
                    'closing_begin_date': item['closingBeginDate'],
                    'closing_end_date': item['closingEndDate']
                })
            
            return data_list
        else:
            logging.error(f"API调用失败：{result.get('message')}")
            return []
            
    except Exception as e:
        logging.error(f"查询交易员收益失败：{str(e)}")
        return []

# 示例使用
if __name__ == "__main__":
    # 示例token，实际使用时需要替换为有效的token
    token = "eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3NjcwNzMxMDF9.xKTS1vOFK8Wwncf5gw6iLILtTsrePQxIVdnsjNqeDz3JKVh4Kkwur-cMwjiZKJrUjTAymidH031W91nH_EOaMw"
    
    # 示例参数
    ccy_group_list = ["USD/CNH"]
    closing_begin_date = "2025-12-31"
    closing_end_date = "2025-12-31"
    
    # 调用方法
    result = query_trader_profit(ccy_group_list, closing_begin_date, closing_end_date, token)
    
    # 打印结果
    print("\n查询结果：")
    for item in result:
        print(f"货币对：{item['ccy_group']}")
        print(f"交割日期：{item['closing_begin_date']} 至 {item['closing_end_date']}")
        print(f"交易员收益：{item['trader_profit_loss']} {item['profit_loss_currency']}")
        print(f"交易金额：{item['trade_amount']} {item['profit_loss_currency']}")
        print("-" * 50)
