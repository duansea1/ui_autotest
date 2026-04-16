"""FORWARD_RATE-汇率计算逻辑.py: 计算给定交割日的汇率"""

from datetime import date
import requests


def calculate_standard_forward(spot_bid, spot_ask, swap_bid, swap_ask):
    """
    计算标准期限的远期汇率
    公式：forward bid=spot bid + swap bid/10000; forward ask = spot ask + swap ask/10000
    
    参数:
    - spot_bid: 即期买入价 (float)
    - spot_ask: 即期卖出价 (float)
    - swap_bid: 掉期买入点 (float)
    - swap_ask: 掉期卖出点 (float)
    
    返回:
    - (forward_bid, forward_ask): 远期买入价和卖出价 (tuple)
    """
    forward_bid = spot_bid + swap_bid / 100
    forward_ask = spot_ask + swap_ask / 100
    return forward_bid, forward_ask


def calculate_non_standard_forward(forward1, forward2, settlement_date1, settlement_date2, target_settlement_date):
    """
    计算不标准期限的远期汇率（插值法）
    公式：(forward2 - forward1) / (settlement_date2 - settlement_date1) * (target_settlement_date - settlement_date1) + forward1
    
    参数:
    - forward1: 第一个标准期远期汇率 (float)
    - forward2: 第二个标准期远期汇率 (float)
    - settlement_date1: 第一个标准期交割日期 (datetime.date)
    - settlement_date2: 第二个标准期交割日期 (datetime.date)
    - target_settlement_date: 目标交割日期 (datetime.date)
    
    返回:
    - 目标交割日的远期汇率 (float)
    """
    # 计算两个标准期交割日之间的天数差异
    days_diff = (settlement_date2 - settlement_date1).days
    
    # 计算目标交割日与第一个标准期交割日之间的天数差异
    target_days_diff = (target_settlement_date - settlement_date1).days
    
    # 根据插值公式计算汇率
    forward_rate = ((forward2 - forward1) / days_diff) * target_days_diff + forward1
    
    return forward_rate


def calculate_forward_rate_with_missing_data(spot_bid, spot_ask, one_d_swap_bid, one_d_swap_ask, two_w_swap_bid, two_w_swap_ask, one_d_settlement_date, two_w_settlement_date, target_settlement_date):
    """
    当中间掉期点缺失时（如缺少1W），计算远期汇率
    公式：(2w forward-1D forward) / (2w交割日期-1D交割日期) * (交割日-1D交割日) +1D forward
    
    参数:
    - spot_bid: 即期买入价 (float)
    - spot_ask: 即期卖出价 (float)
    - one_d_swap_bid: 1天掉期买入点 (float)
    - one_d_swap_ask: 1天掉期卖出点 (float)
    - two_w_swap_bid: 2周掉期买入点 (float)
    - two_w_swap_ask: 2周掉期卖出点 (float)
    - one_d_settlement_date: 1天交割日期 (datetime.date)
    - two_w_settlement_date: 2周交割日期 (datetime.date)
    - target_settlement_date: 目标交割日期 (datetime.date)
    
    返回:
    - (forward_bid, forward_ask): 目标交割日的远期买入价和卖出价 (tuple)
    """
    # 先计算1D远期汇率
    one_d_forward_bid = spot_bid + one_d_swap_bid / 100
    one_d_forward_ask = spot_ask + one_d_swap_ask / 100
    
    # 再计算2W远期汇率
    two_w_forward_bid = spot_bid + two_w_swap_bid / 100
    two_w_forward_ask = spot_ask + two_w_swap_ask / 100
    
    # 计算1D和2W交割日之间的天数差异
    days_diff = (two_w_settlement_date - one_d_settlement_date).days
    
    # 计算目标交割日与1D交割日之间的天数差异
    target_days_diff = (target_settlement_date - one_d_settlement_date).days
    
    # 根据公式计算买入价和卖出价
    forward_bid = ((two_w_forward_bid - one_d_forward_bid) / days_diff) * target_days_diff + one_d_forward_bid
    forward_ask = ((two_w_forward_ask - one_d_forward_ask) / days_diff) * target_days_diff + one_d_forward_ask
    
    return forward_bid, forward_ask


def get_forward_rates(one_d_date, one_w_date, currency_pair="USD/CNH"):
    """
    通过API动态获取指定日期的远期汇率
    
    参数:
    - one_d_date: 第一个交割日期 (datetime.date)
    - one_w_date: 第二个交割日期 (datetime.date)
    - currency_pair: 货币对 (str), 默认"USD/CNH"
    
    返回:
    - (one_d_forward_bid, one_d_forward_ask, one_w_forward_bid, one_w_forward_ask): 两个日期的远期买入价和卖出价 (tuple)
    """
    url = "https://fat-global-ad.baofu.com/ams-api/rateManage/queryRateSwap"
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Cookie': 'Hm_lvt_97352b16ed2df8c3860cf5a1a65fb4dd=1772431870,1773824606; agent-control-core-token=eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3NzU2MjY0NjV9.VUcbIu3o8b8JYs3FZVcwuskWJEm7qz2TMa8a89h7TSwystkz4VbaguzxEeOCJEtWYUaFFtJf_GlGDNeFYhGRng'
    }
    
    data = {
        "termCode": "",
        "currencyPair": currency_pair,
        "currentPage": 1,
        "pageSize": 10
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('code') == '0':
            # 转换日期为字符串格式，匹配API返回的closingDate格式
            one_d_date_str = one_d_date.strftime('%Y-%m-%d')
            one_w_date_str = one_w_date.strftime('%Y-%m-%d')
            
            # 初始化变量
            one_d_forward_bid = 0
            one_d_forward_ask = 0
            one_w_forward_bid = 0
            one_w_forward_ask = 0
            
            # 查找两个日期的数据
            for item in result.get('result', {}).get('list', []):
                if item.get('closingDate') == one_d_date_str:
                    one_d_forward_bid = item.get('bidChannelRate')
                    one_d_forward_ask = item.get('askChannelRate')
                elif item.get('closingDate') == one_w_date_str:
                    one_w_forward_bid = item.get('bidChannelRate')
                    one_w_forward_ask = item.get('askChannelRate')
            
            # 检查是否找到数据
            if one_d_forward_bid == 0 or one_d_forward_ask == 0:
                raise ValueError(f"未找到日期为{one_d_date_str}的汇率数据")
            if one_w_forward_bid == 0 or one_w_forward_ask == 0:
                raise ValueError(f"未找到日期为{one_w_date_str}的汇率数据")
            
            return one_d_forward_bid, one_d_forward_ask, one_w_forward_bid, one_w_forward_ask
        else:
            raise ValueError(f"API调用失败: {result.get('message', '未知错误')}")
            
    except Exception as e:
        print(f"获取汇率数据失败: {str(e)}")
        # 返回默认值，避免程序崩溃
        return 0, 0, 0, 0


# 示例使用
if __name__ == '__main__':
    # ===== 汇率计算示例 =====
    print("汇率计算示例")
    print("=" * 50)
    
    # 参数配置（请根据实际情况修改）
    # 1. 标准期限汇率计算参数
    spot_bid = 482.7  # 即期买入价SPOT
    spot_ask = 482.73  # 即期卖出价SPOT
    
    # 2. 掉期点参数
    # 1D掉期点   使用这一个就行
    one_d_swap_bid = -13.8028  # 1D掉期买入点
    one_d_swap_ask = -11.9813  # 1D掉期卖出点
    
    # 4. 交割日期参数
    one_d_date = date(2026, 4, 24)  # 1D交割日期
    one_w_date = date(2026, 5, 1)  # 1W交割日期
    target_date = date(2026, 4, 26)  # 目标交割日期（1D-1W之间）
    
    # 3. 计算标准期限远期汇率
    # 通过API动态获取两个日期的远期汇率
    print("\n正在从API获取远期汇率数据...")
    currency_pair = "USD/CNH"
    one_d_forward_bid, one_d_forward_ask, one_w_forward_bid, one_w_forward_ask = get_forward_rates(one_d_date, one_w_date, currency_pair)
    
    # 打印获取到的汇率
    print(f"获取到的远期汇率:")
    print(f"  {one_d_date}远期: 买入价={one_d_forward_bid}, 卖出价={one_d_forward_ask}")
    print(f"  {one_w_date}远期: 买入价={one_w_forward_bid}, 卖出价={one_w_forward_ask}")
    
    # 检查API返回值是否有效
    if one_d_forward_bid == 0 or one_d_forward_ask == 0 or one_w_forward_bid == 0 or one_w_forward_ask == 0:
        print("警告: API获取失败，使用默认值")
        # 使用默认值
        one_d_forward_bid = 481.4544
        one_d_forward_ask = 481.5998
        one_w_forward_bid = 480.7752
        one_w_forward_ask = 480.925
    
    # 计算并输出结果
    print("\n计算结果:")
    
    # 1. 标准期限汇率计算
    print("1. 标准期限远期汇率:")
    print(f"   1D远期: 买入价={one_d_forward_bid}, 卖出价={one_d_forward_ask}")
    print(f"   1W远期: 买入价={one_w_forward_bid}, 卖出价={one_w_forward_ask}")
    
    # 2. 不标准期限汇率计算（1D-1W之间）
    print("\n2. 不标准期限汇率计算:")
    # 买入价计算
    non_std_bid = calculate_non_standard_forward(one_d_forward_bid, one_w_forward_bid, one_d_date, one_w_date, target_date)
    # 卖出价计算
    non_std_ask = calculate_non_standard_forward(one_d_forward_ask, one_w_forward_ask, one_d_date, one_w_date, target_date)
    print(f"   目标日期({target_date})在{one_d_date}和{one_w_date}之间的汇率: 买入价={non_std_bid}, 卖出价={non_std_ask}")
