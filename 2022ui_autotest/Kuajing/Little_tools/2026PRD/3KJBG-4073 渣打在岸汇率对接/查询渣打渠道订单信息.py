#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from Kuajing.Common.kjMysql import execute_db

def get_exchange_order_info(env, order_no):
    """获取货币兑换订单信息"""
    # 状态映射字典
    status_map = {
        1: '下单中',
        2: '已交割',
        5: '下单中',
        6: '待交割',
        8: '下单失败',
        11: '交割处理中'
    }
    
    # 查询T_CURRENCY_EXCHANGE_ORDER表
    sql = "SELECT ORDER_NO, CHANNEL_ID, STATUS FROM `BAOFU_TRADE`.`T_CURRENCY_EXCHANGE_ORDER` WHERE `ORDER_NO` = %s ORDER BY `ID` DESC LIMIT 0,1000"
    result = execute_db(env, sql, params=(order_no,))
    
    print("\n===== 货币兑换订单信息 =====")
    if result:
        for row in result:
            print(f"订单号: {row['ORDER_NO']}")
            print(f"渠道ID: {row['CHANNEL_ID']}")
            print(f"状态: {status_map.get(row['STATUS'], '未知')} ({row['STATUS']})")
            print()
        return result[0] if result else None
    else:
        print("未找到该订单号的货币兑换订单信息")
        return None

def get_channel_exchange_price(env, order_no):
    """获取渠道汇率报价信息"""
    # 状态映射字典
    status_map = {
        -1: '处理中',
        0: '初始',
        1: '待交割',
        2: '已交割',
        3: '已拒绝',
        4: '已取消'
    }
    
    # 查询T_CHANNEL_EXCHANGE_PRICE表
    sql = "SELECT CHANNEL_ID, STATUS, EXCHANGE_ORDER_NO, CHANNEL_ORDER_ID FROM `BAOFU_CGW`.`T_CHANNEL_EXCHANGE_PRICE` WHERE `EXCHANGE_ORDER_NO` = %s ORDER BY `ID` DESC LIMIT 0,1000"
    result = execute_db(env, sql, params=(order_no,))
    
    print("\n===== 渠道汇率报价信息 =====")
    if result:
        for row in result:
            print(f"渠道ID: {row['CHANNEL_ID']}")
            print(f"状态: {status_map.get(row['STATUS'], '未知')} ({row['STATUS']})")
            print(f"兑换订单号: {row['EXCHANGE_ORDER_NO']}")
            print(f"渠道订单号: {row['CHANNEL_ORDER_ID']}")
            print()
        return result[0] if result else None
    else:
        print("未找到该订单号的渠道汇率报价信息")
        return None

def get_channel_detail_json(env, channel_order_id):
    """获取渠道详细信息"""
    # 查询T_CHANNEL_DETAIL_JSON表
    sql = "SELECT CHANNEL_ID, JSON_DETAIL FROM `BAOFU_CGW`.`T_CHANNEL_DETAIL_JSON` WHERE `JSON_DETAIL` LIKE %s ORDER BY `ID` DESC LIMIT 0,1000"
    result = execute_db(env, sql, params=(f"%{channel_order_id}%",))
    
    print("\n===== 渠道详细信息-动账文件数据 =====")
    if result:
        for row in result:
            print(f"渠道ID: {row['CHANNEL_ID']}")
            print(f"详细信息: {row['JSON_DETAIL']}")
            print()
        return result
    else:
        print("未找到该渠道订单号的详细信息")
        return None

if __name__ == "__main__":
    # ==================== 参数配置区 ====================
    env = 'UAT'  # 数据库环境参数 (FAT/UAT/FAT_DATA)
    order_no = 2604021540002398200
    # ===================================================
    
    print("=" * 80)
    print(" 🚀🚀🚀渣打渠道订单信息查询")
    print("=" * 80)
    print(f" 环境参数: env={env}")
    print(f" 渠道订单号: {order_no}")
    print("=" * 80)
    
    # 步骤1: 查询货币兑换订单信息
    exchange_order = get_exchange_order_info(env, order_no)
    
    # 步骤2: 查询渠道汇率报价信息
    channel_price = get_channel_exchange_price(env, order_no)
    
    # 步骤3: 如果有渠道订单号，查询渠道详细信息
    if channel_price and channel_price.get('CHANNEL_ORDER_ID'):
        get_channel_detail_json(env, channel_price['CHANNEL_ORDER_ID'])

