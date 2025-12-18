#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author    : AI Assistant
@Date      : 2025/12/15
@Description: 当月总损益字段计算脚本 - 处理小币种结算金额
"""
import sys
import os
from datetime import datetime

# 导入数据库配置模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Kuajing.Common.kjMysql import get_db_config
import pymysql

class MonthlyProfitLossCalculator:
    def __init__(self, env='FAT'):
        """初始化数据库连接"""
        # 获取数据库配置
        self.db_config = get_db_config(env)
        self.conn = None
        self.cursor = None
        self.connect_db()
    
    def connect_db(self):
        """建立数据库连接"""
        self.conn = pymysql.connect(**self.db_config)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        print(f"成功连接到数据库：{self.db_config['host']}:{self.db_config['port']} - {self.db_config['database']}")
    
    def close_db(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def query_distribution_profit(self, start_date, end_date, currency):
        """
        获取分发兑换损益字段
        
        :param start_date: CREATE_AT 开始日期 (YYYY-MM-DD)
        :param end_date: CREATE_AT 结束日期 (YYYY-MM-DD)
        :param currency: 小币种字段 (如 'KRW')
        :return: 分发兑换损益总和 (USD)
        """
        print(f"\n===== 查询分发兑换损益数据 =====")
        print(f"查询条件：小币种={currency}，日期范围={start_date}至{end_date}")
        
        # 格式化日期时间范围
        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"
        
        # 数据库核心SQL - 添加GROUP BY PROFIT_CCY实现分组查询
        sql = """
        SELECT 
            PROFIT_CCY AS sellCcy, 
            IFNULL(SUM(PROFIT_AMT), 0) AS sumSellAmount
        FROM 
            BAOFU_TRADE.T_TRADE_RECEIPT 
        WHERE 
            (SOURCE_CURRENCY = %s OR TARGET_CURRENCY = %s)
            AND TRADE_STATUS = 2
            AND STATUS = 2
            AND CREATE_AT BETWEEN %s AND %s
        GROUP BY PROFIT_CCY;
        """
        
        self.cursor.execute(sql, (currency, currency, start_datetime, end_datetime))
        results = self.cursor.fetchall()
        
        print(f"查询结果：")
        print(f"  📊 共查询到 {len(results)} 种损益币种")
        
        # 初始化USD损益金额
        usd_profit_loss = 0.0
        
        # 遍历所有分组结果
        for idx, result in enumerate(results, 1):
            current_ccy = result['sellCcy']
            current_amount = float(result['sumSellAmount'] or 0.0)
            
            # 如果是USD，保存返回值
            if current_ccy == 'USD':
                usd_profit_loss = current_amount
                print(f"  {idx}. 🎉损益币种: {current_ccy}")
                print(f"     🎉🎉🎉分发兑换损益(USD)--: {current_amount}")
            else:
                print(f"  {idx}. 📈损益币种: {current_ccy}")
                print(f"     📈📈📈分发兑换损益--: {current_amount}")
        
        # 返回USD的分发兑换损益总和（保持方法返回值兼容性）
        return usd_profit_loss
    
    def calculate_monthly_total_profit_loss(self, gep_record_ccy_exposure, current_day_rate, distribution_profit_amt, gep_usd_exposure=0.0):
        """
        计算当月总损益
        
        :param gep_record_ccy_exposure: GEP小币种敞口字段值 (float)
        :param current_day_rate: 当月报表汇率 (float)
        :param distribution_profit_amt: 分发兑换损益(美元) (float)
        :param gep_usd_exposure: GEP美元敞口 (float, 默认值为0.0)
        :return: 总损益(美元) (float)
        """
        print(f"\n===== 计算当月总损益 =====")
        print(f"输入参数：")
        print(f"  GEP小币种敞口: {gep_record_ccy_exposure}")
        print(f"  当月报表汇率: {current_day_rate}")
        print(f"  分发兑换损益(USD): {distribution_profit_amt}")
        print(f"  GEP美元敞口: {gep_usd_exposure}")
        
        # 计算总损益
        # 总损益(美元) = GEP小币种敞口 * 当月报表汇率 + GEP美元敞口 + 分发兑换损益(美元)
        total_profit_loss = (gep_record_ccy_exposure * current_day_rate) + gep_usd_exposure + distribution_profit_amt
        
        print(f"\n计算结果：")
        print(f"  🚀总损益(美元) = {gep_record_ccy_exposure} * {current_day_rate} + {gep_usd_exposure} + {distribution_profit_amt}")
        print(f"  🚀总损益(美元) = {total_profit_loss:.2f} USD")
        
        return total_profit_loss
    
    def get_exchange_rates(self, ccy, rate_date=None):
        """
        获取两个方向的汇率：USD→小币种 和 小币种→USD
        
        :param ccy: 小币种（如 'KRW'）
        :param rate_date: 汇率查询日期，默认为当天
        :return: 包含两个方向汇率的字典
        """
        # 默认使用当天日期
        if not rate_date:
            rate_date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"\n===== 查询汇率数据 =====")
        print(f"查询条件：小币种={ccy}，汇率查询日期={rate_date}")
        
        # 初始化汇率结果
        exchange_rates = {
            'usd_to_ccy': None,
            'ccy_to_usd': None
        }
        
        # 1. 查询 USD → 小币种 的汇率
        print(f"\n1. 查询 USD → {ccy} 方向的汇率：")
        sql1 = """
        SELECT 
            ID, RECORD_ID, CHANNEL_ID, SOURCE_CCY, DEST_CCY, TRADE_DIRECTION,
            CHANNEL_RATE, RATE_QUERY_DATE, STATUS, REMARKS, CREATE_AT, CREATE_BY,
            UPDATE_AT, UPDATE_BY, ORIGINAL_CCY, TARGET_CCY
        FROM 
            BAOFU_CGW.T_CHANNEL_FIXED_RATE_DETAIL
        WHERE 
            RATE_QUERY_DATE = %s
            AND STATUS = 1
            AND ORIGINAL_CCY = 'USD'
            AND TARGET_CCY = %s;
        """
        
        self.cursor.execute(sql1, (rate_date, ccy))
        usd_to_ccy_result = self.cursor.fetchone()
        
        if usd_to_ccy_result:
            usd_to_ccy_rate = float(usd_to_ccy_result['CHANNEL_RATE'])
            exchange_rates['usd_to_ccy'] = usd_to_ccy_rate
            print(f"  USD→{ccy}方向的汇率如下：{usd_to_ccy_rate}")
            print(f"  详细信息：")
            print(f"    ID: {usd_to_ccy_result['ID']}")
            print(f"    CHANNEL_ID: {usd_to_ccy_result['CHANNEL_ID']}")
            print(f"    CHANNEL_RATE: {usd_to_ccy_result['CHANNEL_RATE']}")
            print(f"    STATUS: {'生效' if usd_to_ccy_result['STATUS'] == 1 else '失效'}")
        else:
            print(f"  未查询到 USD→{ccy} 方向的汇率")
        
        # 2. 查询 小币种 → USD 的汇率
        print(f"\n2. 查询 {ccy} → USD 方向的汇率：")
        sql2 = """
        SELECT 
            ID, RECORD_ID, CHANNEL_ID, SOURCE_CCY, DEST_CCY, TRADE_DIRECTION,
            CHANNEL_RATE, RATE_QUERY_DATE, STATUS, REMARKS, CREATE_AT, CREATE_BY,
            UPDATE_AT, UPDATE_BY, ORIGINAL_CCY, TARGET_CCY
        FROM 
            BAOFU_CGW.T_CHANNEL_FIXED_RATE_DETAIL
        WHERE 
            RATE_QUERY_DATE = %s
            AND STATUS = 1
            AND ORIGINAL_CCY = %s
            AND TARGET_CCY = 'USD';
        """
        
        self.cursor.execute(sql2, (rate_date, ccy))
        ccy_to_usd_result = self.cursor.fetchone()
        
        if ccy_to_usd_result:
            ccy_to_usd_rate = float(ccy_to_usd_result['CHANNEL_RATE'])
            exchange_rates['ccy_to_usd'] = ccy_to_usd_rate
            print(f"  {ccy}→USD方向的汇率如下：{ccy_to_usd_rate}")
            print(f"  详细信息：")
            print(f"    ID: {ccy_to_usd_result['ID']}")
            print(f"    CHANNEL_ID: {ccy_to_usd_result['CHANNEL_ID']}")
            print(f"    CHANNEL_RATE: {ccy_to_usd_result['CHANNEL_RATE']}")
            print(f"    STATUS: {'生效' if ccy_to_usd_result['STATUS'] == 1 else '失效'}")
        else:
            print(f"  未查询到 {ccy}→USD 方向的汇率")
        
        print(f"\n===== 汇率查询结果汇总 =====")
        print(f"USD/{ccy} 汇率：")
        print(f"  USD→{ccy}：{exchange_rates['usd_to_ccy'] if exchange_rates['usd_to_ccy'] is not None else '未查询到'}")
        print(f"  {ccy}→USD：{exchange_rates['ccy_to_usd'] if exchange_rates['ccy_to_usd'] is not None else '未查询到'}")
        
        return exchange_rates


if __name__ == "__main__":
    """主函数入口"""
    print("启动当月总损益计算脚本")
    
    # 从命令行参数获取币种和日期范围
    env = "UAT"
    ccy = 'VND'
    start_date = '2025-12-01'
    end_date = '2025-12-18'
    rate_date = '2025-12-18'
    
    print(f"查询币种: {ccy}")
    print(f"日期范围: {start_date} 至 {end_date}")
    
    # 创建实例
    calculator = MonthlyProfitLossCalculator(env)
    
    # 示例1：查询分发兑换损益(USD)并计算总损益
    print("\n" + "="*80)
    print("示例1：查询分发兑换损益(USD)并计算总损益")
    print("="*80)
    
    # 查询分发兑换损益(USD)
    distribution_profit = calculator.query_distribution_profit(start_date, end_date, ccy)
    
    # 计算总损益
    gep_ccy_exposure = -1889147  # GEP小币种敞口
    current_rate = 0.0006873002  # 当月报表汇率
    gep_usd_exp = -20.61  # GEP美元敞口
    
    total_profit_loss = calculator.calculate_monthly_total_profit_loss(
        gep_record_ccy_exposure=gep_ccy_exposure,
        current_day_rate=current_rate,
        distribution_profit_amt=distribution_profit,
        gep_usd_exposure=gep_usd_exp
    )
    
    # 示例2：独立使用获取汇率方法
    print("\n" + "="*80)
    print("示例2：独立使用获取汇率方法")
    print("="*80)
    
    # 调用独立的获取汇率方法，查询报表的汇率
    exchange_rates = calculator.get_exchange_rates(ccy, rate_date)
    
    # 关闭数据库连接
    calculator.close_db()
    
    print(f"\n⏩脚本执行完成，总损益计算结果：{total_profit_loss:.2f} USD")