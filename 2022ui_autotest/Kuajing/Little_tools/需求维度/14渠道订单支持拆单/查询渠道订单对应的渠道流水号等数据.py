#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author    : duansea
@Date      : 2025/10/14
@Description: 查询渠道订单对应的渠道流水号等数据
"""

import sys
import os
import pymysql
import logging
import traceback
from tabulate import tabulate

# 添加kjMysql.py所在路径到系统路径
from Kuajing.Common.kjMysql import get_db_config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def query_channel_exchange_price(channel_order, env='FAT'):
    """
    查询T_CHANNEL_EXCHANGE_PRICE表数据
    
    Args:
        channel_order: 渠道订单号，用于EXCHANGE_ORDER_NO字段
        env: 环境，可选值为'FAT'或'UAT'，默认为'FAT'
    
    Returns:
        查询结果字典列表
    """
    if not channel_order:
        logger.error("渠道订单号不能为空")
        return []
    
    try:
        # 获取数据库配置
        db_config = get_db_config(env)
        # 修改数据库名称为BAOFU_CGW
        db_config['database'] = 'BAOFU_CGW'
        
        # 确保数据库配置中包含cursorclass参数
        if 'cursorclass' not in db_config:
            from pymysql.cursors import DictCursor
            db_config['cursorclass'] = DictCursor
            logger.info("数据库配置中已添加cursorclass参数")
        else:
            logger.info("数据库配置中已包含cursorclass参数")
        
        # 连接数据库
        logger.info(f"准备连接数据库: {db_config['host']}:{db_config['port']} - {db_config['database']}")
        conn = pymysql.connect(**db_config)
        
        # 查询SQL
        sql = """SELECT * FROM `BAOFU_CGW`.`T_CHANNEL_EXCHANGE_PRICE` 
                WHERE `EXCHANGE_ORDER_NO` = %s"""
        
        logger.info(f"执行SQL查询T_CHANNEL_EXCHANGE_PRICE表，订单号: {channel_order}")
        
        # 执行查询
        with conn.cursor() as cursor:
            cursor.execute(sql, (channel_order,))
            results = cursor.fetchall()
        
        # 关闭连接
        conn.close()
        logger.info(f"数据库连接已关闭，查询到 {len(results)} 条T_CHANNEL_EXCHANGE_PRICE记录")
        
        return results
        
    except Exception as e:
        logger.error(f"查询T_CHANNEL_EXCHANGE_PRICE表时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        return []

def query_channel_order_info(channel_order, env='FAT'):
    """
    查询渠道订单对应的信息
    
    Args:
        channel_order: 渠道订单号，对应表中的ORDER_NO字段
        env: 环境，可选值为'FAT'或'UAT'，默认为'FAT'
    
    Returns:
        dict: 查询结果
    """
    if not channel_order:
        logger.error("渠道订单号不能为空")
        return None
    
    try:
        # 获取数据库配置
        db_config = get_db_config(env)
        # 修改数据库名称为BAOFU_TRADE
        db_config['database'] = 'BAOFU_TRADE'
        
        logger.info(f"准备连接数据库: {db_config['host']}:{db_config['port']} - {db_config['database']}")
        
        # 检查db_config中是否已包含cursorclass参数，避免重复指定
        if 'cursorclass' in db_config:
            logger.info("数据库配置中已包含cursorclass参数")
        else:
            # 如果没有，添加DictCursor以确保返回字典格式结果
            from pymysql.cursors import DictCursor
            db_config['cursorclass'] = DictCursor
            logger.info("已添加DictCursor到数据库配置")
        
        # 建立数据库连接
        connection = pymysql.connect(**db_config)
        
        try:
            with connection.cursor() as cursor:
                # 构建SQL查询语句，查询指定字段
                sql = """
                SELECT 
                    STATUS,  -- 交割状态
                    CHANNEL_ID,  -- 渠道
                    PAYMENT_STATUS,  -- 付款到渠道状态
                    SETTLE_STATUS,  -- 渠道结算状态
                    RELATION_PAYMENT_NO,  -- 关联付款到渠道订单号
                    RELATION_SETTLE_NO,  -- 关联渠道结算订单号
                    TRADE_ID AS 交易id,  -- 交易id
                    BATCH_NO AS 批次号,  -- 批次号
                    CHANNEL_RECONCILIATION_NO,  -- 渠道对账流水
                    CLOSING_TYPE,  -- 交割模式
                    CLOSING_DATE,  -- 交割日期
                    CHANNEL_ERR_MSG  -- 渠道返回的msg
                FROM 
                    `BAOFU_TRADE`.`T_CURRENCY_EXCHANGE_ORDER` 
                WHERE 
                    ORDER_NO = %s
                """
                
                logger.info(f"执行SQL查询，订单号: {channel_order}")
                cursor.execute(sql, (channel_order,))
                result = cursor.fetchone()
                
                if result:
                    logger.info(f"查询到订单信息: {channel_order}")
                    return result
                else:
                    logger.warning(f"未找到订单: {channel_order}")
                    return None
                    
        finally:
            connection.close()
            logger.info("数据库连接已关闭")
            
    except Exception as e:
        logger.error(f"查询渠道订单信息时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        return None

# 渠道代码到中文名称的映射字典（全局变量）
channel_map = {
    "1000000003": "海云汇换汇渠道",
    "1200923003": "中国银行",
    "1200923009": "宝付潜在用户官方汇率渠道",
    "1200923010": "货币兑换用户官方汇率渠道",
    "1200923011": "收款账户用户官方汇率渠道",
    "1200923013": "wiseFx货币兑换",
    "1200923017": "中国外汇交易中心",
    "1200923029": "汇率报价-中国外汇交易中心",
    "1200923030": "汇率报价-新浪",
    "1200923031": "汇率报价-dbs 香港",
    "1200923032": "汇率报价-中银香港",
    "1200923033": "第三方汇率渠道-货币兑换",
    "1200923039": "交叉汇率-内部",
    "1200923060": "M-DAQ-货币兑换",
    "1200923063": "WALLX-换汇渠道",
    "1200923069": "彭博数据",
    "1200923071": "PINGPONG-货币兑换",
    "1200923072": "DBS-货币兑换渠道",
    "1200923074": "稠州银行",
    "1200923075": "彭博数据（在岸）",
    "1200923079": "自定义报价源-彭博+2%",
    "1200923080": "自定义报价源-海云测试",
    "1200923086": "渣打 FX",
    "1200923090": "autotest-全部货币汇率渠道",
    "1200923102": "JPM-货币兑换",
    "1200923112": "Flutter-货币兑换",
    "1200923119": "中国银行-汇兑渠道",
    "1200923117": "xe汇率渠道"
}

def print_order_info(order_info):
    """
    打印订单信息（表格形式）
    
    Args:
        order_info: 订单信息字典
    """
    if not order_info:
        logger.info("没有查询到订单信息")
        return
    
    # 状态映射字典
    status_map = {
        1: "下单中",
        2: "已交割",
        5: "下单中",
        6: "待交割",
        8: "下单失败",
        11: "交割处理中"
    }
    
    payment_status_map = {
        0: "待付款",
        1: "付款中",
        2: "付款成功",
        3: "无需付款"
    }
    
    settle_status_map = {
        0: "待结算",
        1: "结算中",
        2: "结算成功",
        3: "无需结算"
    }
    
    # 获取渠道信息，同时显示代码和中文名称
    channel_id = order_info.get('CHANNEL_ID', '未知')
    channel_name = channel_map.get(str(channel_id), '未知渠道')
    
    # 构建表格数据
    table_data = [
        ["交割状态", status_map.get(order_info.get('STATUS'), order_info.get('STATUS', '未知'))],
        ["渠道", f"{channel_id} ({channel_name})"],
        ["付款到渠道状态", payment_status_map.get(order_info.get('PAYMENT_STATUS'), order_info.get('PAYMENT_STATUS', '未知'))],
        ["渠道结算状态", settle_status_map.get(order_info.get('SETTLE_STATUS'), order_info.get('SETTLE_STATUS', '未知'))],
        ["关联付款到渠道订单号", order_info.get('RELATION_PAYMENT_NO', '无')],
        ["关联渠道结算订单号", order_info.get('RELATION_SETTLE_NO', '无')],
        ["trad_id", order_info.get('交易id', '无')],
        ["批次号", order_info.get('批次号', '无')],
        ["渠道对账流水号", order_info.get('CHANNEL_RECONCILIATION_NO', '无')],
        ["交割模式", order_info.get('CLOSING_TYPE', '无')],
        ["交割日期", order_info.get('CLOSING_DATE', '无')],
        ["渠道返回的msg", order_info.get('CHANNEL_ERR_MSG', '无')],
        
    ]
    
    # 使用tabulate打印表格
    logger.info("\n" + "="*60)
    logger.info("渠道订单信息详情")
    logger.info("="*60)
    logger.info("\n" + tabulate(table_data, headers=["项目", "值"], tablefmt="grid"))
    logger.info("="*60)

def print_exchange_price_info(exchange_price_list, channel_map):
    """打印T_CHANNEL_EXCHANGE_PRICE表的相关字段信息（表格形式）
    
    Args:
        exchange_price_list: T_CHANNEL_EXCHANGE_PRICE表查询结果列表
        channel_map: 渠道代码到中文名称的映射字典
    """
    logger = logging.getLogger(__name__)
    
    if not exchange_price_list:
        logger.info("未查询到T_CHANNEL_EXCHANGE_PRICE表记录")
        return
    
    # STATUS状态映射
    status_map = {
        -1: "处理中",
        0: "初始",
        1: "待交割",
        2: "已交割",
        3: "已拒绝",
        4: "已取消"
    }
    
    logger.info("\n" + "="*60)
    logger.info("T_CHANNEL_EXCHANGE_PRICE表信息")
    logger.info("="*60)
    
    # 如果有多个记录，逐个打印
    for i, price_info in enumerate(exchange_price_list, 1):
        if len(exchange_price_list) > 1:
            logger.info(f"\n记录 {i}:")
            logger.info("-"*30)
        
        # 获取渠道信息，同时显示代码和中文名称
        channel_id = price_info.get('CHANNEL_ID', '未知')
        channel_name = channel_map.get(str(channel_id), '未知渠道')
        
        # 构建表格数据
        table_data = [
            ["渠道", f"{channel_id} ({channel_name})"],
            ["交易金额", price_info.get('CURR_AMOUNT', '未知')],
            ["状态", status_map.get(price_info.get('STATUS'), price_info.get('STATUS', '未知'))],
            ["货币兑换订单号", price_info.get('EXCHANGE_ORDER_NO', '未知')],
            ["银行参考号", price_info.get('BANK_REFERENCE', '未知')],
            ["渠道对账流水", price_info.get('CHANNEL_RECONCILIATION_NO', '未知')]
        ]
        
        # 使用tabulate打印表格
        logger.info("\n" + tabulate(table_data, headers=["项目", "值"], tablefmt="grid"))
    
    logger.info("="*60)

# ============= 使用示例 =============
if __name__ == "__main__":
    # 示例1: 查询FAT环境下的渠道订单信息 
    channel_order = "2511061108001831174"  # 替换为实际的渠道订单号，之前测试能查询到记录的订单号
    env = "UAT"
    print(f"\n=== 查询 {env} 环境下的渠道订单信息 ===")
    order_info = query_channel_order_info(channel_order, env)
    print_order_info(order_info)
    
    # 查询T_CHANNEL_EXCHANGE_PRICE表信息
    # print(f"\n=== 查询 {env} 环境下的T_CHANNEL_EXCHANGE_PRICE表信息 ===")
    # exchange_price_info = query_channel_exchange_price(channel_order, env)
    # print(f"--------------------------------查询到的T_CHANNEL_EXCHANGE_PRICE表记录数: {len(exchange_price_info)}")
    # if exchange_price_info:
    #     # 将channel_map作为参数传递
    #     print_exchange_price_info(exchange_price_info, channel_map)
    # else:
    #     print("未查询到T_CHANNEL_EXCHANGE_PRICE表记录")
    
