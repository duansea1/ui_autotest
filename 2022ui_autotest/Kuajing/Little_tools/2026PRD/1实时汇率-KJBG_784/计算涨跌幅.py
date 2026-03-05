"""
@Author    : duansea
@Date      : 2026/2/10 15:42
@Description: [汇率涨跌幅计算工具]
"""
import sys
import os
from datetime import datetime

# 添加项目路径以便导入kjMysql模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from Kuajing.Common.kjMysql import execute_db

def get_latest_rate(currency_pair: str, closing_type: str, start_time: str, end_time: str, channel_id: str = '1200923069', unit: int = 0, env: str = 'FAT_DATA') -> dict:
    """
    获取指定货币对、当天最新的买入、卖出方向汇率
    Args:
        currency_pair: 货币对，如 'USD/HKD'
        closing_type: 交割类型，如 'TOD'
        start_time: 开始时间，格式 '2026-02-10 00:00:00'
        end_time: 结束时间，格式 '2026-02-10 23:59:59'
        channel_id: 渠道ID，默认 '1200923069'
        unit: 汇率单位，0表示原值，1表示除以100
        env: 数据库环境，默认 'FAT_DATA'
    Returns:
        包含最新汇率信息的字典
    """
    sql = """
    SELECT 
        t.create_time AS createAt, 
        t.sourceCcy AS sourceCcy, 
        t.destCcy AS destCcy, 
        t.channelId AS channelId, 
        t.closingType AS closingType, 
        MAX(CASE WHEN t.tradeDirection = 1 THEN t.discountRate END) AS sellRate, 
        MAX(CASE WHEN t.tradeDirection = 2 THEN t.discountRate END) AS buyRate 
    FROM T_TOPIC_BAOFU_CGW_CHANNEL_RATE t 
    WHERE 
        t.tradeRate > 0 
        AND t.discountRate > 0 
        AND t.closingType = %s 
        AND t.create_time > %s 
        AND t.create_time < %s 
        AND t.channelId = %s 
        AND CONCAT(t.sourceCcy, '/', t.destCcy) IN (%s) 
        AND t.create_time = ( 
            SELECT MAX(t2.create_time) 
            FROM T_TOPIC_BAOFU_CGW_CHANNEL_RATE t2 
            WHERE 
                t2.tradeRate > 0 
                AND t2.discountRate > 0 
                AND t2.closingType = %s 
                AND t2.create_time > %s 
                AND t2.create_time < %s 
                AND t2.channelId = t.channelId 
                AND t2.sourceCcy = t.sourceCcy 
                AND t2.destCcy = t.destCcy 
        ) 
    GROUP BY 
        t.channelId, 
        t.create_time, 
        t.sourceCcy, 
        t.destCcy, 
        t.closingType 
    ORDER BY t.create_time DESC;
    """
    params = (closing_type, start_time, end_time, channel_id, currency_pair, closing_type, start_time, end_time)
    result = execute_db(env, sql, params=params)
    
    # 处理汇率单位
    if result:
        rate_info = result[0]
        if unit == 1:
            if 'buyRate' in rate_info and rate_info['buyRate']:
                rate_info['buyRate'] = rate_info['buyRate'] / 100
            if 'sellRate' in rate_info and rate_info['sellRate']:
                rate_info['sellRate'] = rate_info['sellRate'] / 100
        return rate_info
    return None

def get_oldest_rate(currency_pair: str, closing_type: str, start_time: str, end_time: str, channel_id: str = '1200923069', unit: int = 0, env: str = 'FAT_DATA') -> dict:
    """
    获取指定货币对、当天最旧的买入、卖出方向汇率
    Args:
        currency_pair: 货币对，如 'USD/HKD'
        closing_type: 交割类型，如 'TOD'
        start_time: 开始时间，格式 '2026-02-10 00:00:00'
        end_time: 结束时间，格式 '2026-02-10 23:59:59'
        channel_id: 渠道ID，默认 '1200923069'
        unit: 汇率单位，0表示原值，1表示除以100
        env: 数据库环境，默认 'FAT_DATA'
    Returns:
        包含最旧汇率信息的字典
    """
    sql = """
    SELECT 
        t.create_time AS createAt, 
        t.sourceCcy AS sourceCcy, 
        t.destCcy AS destCcy, 
        t.channelId AS channelId, 
        t.closingType AS closingType, 
        MAX(CASE WHEN t.tradeDirection = 1 THEN t.discountRate END) AS sellRate, 
        MAX(CASE WHEN t.tradeDirection = 2 THEN t.discountRate END) AS buyRate 
    FROM T_TOPIC_BAOFU_CGW_CHANNEL_RATE t 
    WHERE 
        t.tradeRate > 0 
        AND t.discountRate > 0 
        AND t.closingType = %s 
        AND t.create_time > %s 
        AND t.create_time < %s 
        AND t.channelId = %s 
        AND CONCAT(t.sourceCcy, '/', t.destCcy) IN (%s) 
        AND t.create_time = ( 
            SELECT MIN(t2.create_time) 
            FROM T_TOPIC_BAOFU_CGW_CHANNEL_RATE t2 
            WHERE 
                t2.tradeRate > 0 
                AND t2.discountRate > 0 
                AND t2.closingType = %s 
                AND t2.create_time > %s 
                AND t2.create_time < %s 
                AND t2.channelId = t.channelId 
                AND t2.sourceCcy = t.sourceCcy 
                AND t2.destCcy = t.destCcy 
        ) 
    GROUP BY 
        t.channelId, 
        t.create_time, 
        t.sourceCcy, 
        t.destCcy, 
        t.closingType 
    ORDER BY t.create_time DESC;
    """
    params = (closing_type, start_time, end_time, channel_id, currency_pair, closing_type, start_time, end_time)
    result = execute_db(env, sql, params=params)
    
    # 处理汇率单位
    if result:
        rate_info = result[0]
        if unit == 1:
            if 'buyRate' in rate_info and rate_info['buyRate']:
                rate_info['buyRate'] = rate_info['buyRate'] / 100
            if 'sellRate' in rate_info and rate_info['sellRate']:
                rate_info['sellRate'] = rate_info['sellRate'] / 100
        return rate_info
    return None

def get_mid_price_range(currency_pair: str, closing_type: str, start_time: str, end_time: str, channel_id: str = '1200923069', unit: int = 0, env: str = 'FAT_DATA') -> dict:
    """
    获取指定货币对、当天最高、最低的中间价
    Args:
        currency_pair: 货币对，如 'USD/HKD'
        closing_type: 交割类型，如 'TOD'
        start_time: 开始时间，格式 '2026-02-10 00:00:00'
        end_time: 结束时间，格式 '2026-02-10 23:59:59'
        channel_id: 渠道ID，默认 '1200923069'
        unit: 汇率单位，0表示原值，1表示除以100
        env: 数据库环境，默认 'FAT_DATA'
    Returns:
        包含最高、最低中间价的字典
    """
    sql = """
    SELECT 
        s.sourceCcy AS sourceCcy, 
        s.destCcy AS destCcy, 
        MAX((s.buyR + s.sellR) / 2) AS maxMidPrice, 
        MIN((s.buyR + s.sellR) / 2) AS minMidPrice 
    FROM ( 
        SELECT 
            sourceCcy, 
            destCcy, 
            create_time, 
            MAX(CASE WHEN tradeDirection = 1 THEN discountRate END) AS buyR, 
            MAX(CASE WHEN tradeDirection = 2 THEN discountRate END) AS sellR 
        FROM T_TOPIC_BAOFU_CGW_CHANNEL_RATE 
        WHERE 
            tradeRate > 0 
            AND discountRate > 0 
            AND closingType = %s 
            AND create_time > %s 
            AND create_time < %s 
            AND channelId = %s 
            AND CONCAT(sourceCcy, '/', destCcy) IN (%s) 
        GROUP BY sourceCcy, destCcy, create_time 
        HAVING buyR IS NOT NULL AND sellR IS NOT NULL 
    ) s 
    GROUP BY s.sourceCcy, s.destCcy;
    """
    params = (closing_type, start_time, end_time, channel_id, currency_pair)
    result = execute_db(env, sql, params=params)
    
    # 处理汇率单位
    if result:
        mid_price_info = result[0]
        max_mid = mid_price_info.get('maxMidPrice', 0)
        min_mid = mid_price_info.get('minMidPrice', 0)
        
        # 处理单位转换
        if unit == 1:
            max_mid = max_mid / 100
            min_mid = min_mid / 100
            mid_price_info['maxMidPrice'] = max_mid
            mid_price_info['minMidPrice'] = min_mid
        
        # 获取当前中间价
        latest = get_latest_rate(currency_pair, closing_type, start_time, end_time, channel_id, unit, env)
        if latest:
            current_buy = latest.get('buyRate', 0)
            current_sell = latest.get('sellRate', 0)
            current_mid = (current_buy + current_sell) / 2 if current_buy and current_sell else 0
            print(f"中间价计算：当前中间价={current_mid}，最高中间价={max_mid}，最低中间价={min_mid}")
        
        return mid_price_info
    return None

def calculate_change_rate(currency_pair: str, closing_type: str, start_time: str, end_time: str, channel_id: str = '1200923069', unit: int = 0, env: str = 'FAT_DATA') -> dict:
    """
    计算涨跌幅度
    涨跌幅=(当前价格/当日第一条汇率数据-1)*100%
    当前价=(当前买入+当前卖出)/2
    Args:
        currency_pair: 货币对，如 'USD/HKD'
        closing_type: 交割类型，如 'TOD'
        start_time: 开始时间，格式 '2026-02-10 00:00:00'
        end_time: 结束时间，格式 '2026-02-10 23:59:59'
        channel_id: 渠道ID，默认 '1200923069'
        unit: 汇率单位，0表示原值，1表示除以100
        env: 数据库环境，默认 'FAT_DATA'
    Returns:
        包含涨跌幅信息的字典
    """
    # 获取最新汇率
    latest_rate = get_latest_rate(currency_pair, closing_type, start_time, end_time, channel_id, unit, env)
    # 获取最旧汇率
    oldest_rate = get_oldest_rate(currency_pair, closing_type, start_time, end_time, channel_id, unit, env)
    
    if not latest_rate or not oldest_rate:
        print(f"无法获取{currency_pair}的汇率数据")
        return None
    
    # 计算当前价
    current_buy = latest_rate.get('buyRate', 0)
    current_sell = latest_rate.get('sellRate', 0)
    # 当前价=(当前买入+当前卖出)/2 
    current_price = (current_buy + current_sell) / 2 if current_buy and current_sell else 0
    
    # 计算当日第一条汇率价格
    first_buy = oldest_rate.get('buyRate', 0)
    first_sell = oldest_rate.get('sellRate', 0)
    first_price = (first_buy + first_sell) / 2 if first_buy and first_sell else 0
    
    # 计算涨跌幅
    change_rate = ((current_price / first_price) - 1) * 100 if first_price > 0 else 0
    
    # 打印日志
    print(f"当前货币对：{currency_pair}、最新买入方向汇率：{current_buy}、卖出方向汇率：{current_sell}")
    print(f"当前货币对{currency_pair}：第一条汇率 买入方向汇率：{first_buy}、卖出方向汇率：{first_sell}")
    print(f"中间价计算公式：(买入汇率+卖出汇率)/2")
    print(f"当前价格的中间价计算：({current_buy}+{current_sell})/2 = {current_price}")
    print(f"第一条汇率的中间价计算：({first_buy}+{first_sell})/2 = {first_price}")
    print(f"涨跌幅计算：(当前价格/当日第一条汇率数据-1)*100%")
    print(f"代入公式：({current_price}/{first_price}-1)*100% = {change_rate:.4f}%")
    
    # 获取中间价范围
    mid_price_range = get_mid_price_range(currency_pair, closing_type, start_time, end_time, channel_id, unit, env)
    max_mid = mid_price_range.get('maxMidPrice', 0) if mid_price_range else 0
    min_mid = mid_price_range.get('minMidPrice', 0) if mid_price_range else 0
    
    return {
        'current_buy': current_buy,
        'current_sell': current_sell,
        'change_rate': change_rate,
        'max_mid_price': max_mid,
        'min_mid_price': min_mid
    }

# 示例用法
if __name__ == "__main__":
    # 可配置参数
    env = 'FAT_DATA'  # 数据库环境参数
    currency_pair = 'USD/HKD'
    closing_type = 'TOD'
    start_time = '2026-03-05 00:00:00'
    end_time = '2026-03-05 23:59:59'
    channel_id = '1200923069'  # 1200923069-彭博
    
    # 测试单位=1（除以100）
    print("\n===== 汇率涨跌幅计算（单位=1）=====")
    result_unit_1 = calculate_change_rate(currency_pair, closing_type, start_time, end_time, channel_id, unit=1, env=env)
    if result_unit_1:
        print(f"\n最终结果：")
        print(f"最新买入汇率：{result_unit_1['current_buy']}")
        print(f"最新卖出汇率：{result_unit_1['current_sell']}")
        print(f"涨跌幅：{result_unit_1['change_rate']:.4f}%")
        print(f"最高中间价={result_unit_1['max_mid_price']}，最低中间价={result_unit_1['min_mid_price']}")
