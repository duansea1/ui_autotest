#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author    : AI Assistant
@Date      : 2026/01/06
@Description: 小币种损益汇总-客户当月买入卖出金额统计脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# 导入数据库配置模块
from Kuajing.Common.kjMysql import execute_db

class CustomerTradeStatistics:
    def __init__(self, env='FAT'):
        """初始化统计类"""
        self.env = env
    
    def statistics_trade_data(self, start_date, end_date, ccy):
        """统计客户当月买入卖出金额数据
        
        Args:
            start_date: 开始时间，格式：'%Y-%m-%d %H:%M:%S'
            end_date: 结束时间，格式：'%Y-%m-%d %H:%M:%S'
            ccy: 小币种代码列表
        """
        print(f"\n{'='*60}")
        print(f"统计时间范围: {start_date} 至 {end_date}")
        print(f"{'='*60}")
        
        for small_ccy in ccy:
            print(f"\n{'*'*40}")
            print(f"当前统计小币种: {small_ccy}")
            print(f"{'*'*40}")
            
            # 1. 严格按照用户提供的第一个SQL查询：TRADE_DIRECTION = 1
            sql_direction1 = f"""
            SELECT 
                SOURCE_CURRENCY AS buyCcy,
                TARGET_CURRENCY AS sellCcy,
                1 AS TRADE_DIRECTION,
                SUM(SALE_AMOUNT) AS sumSellAmount,
                SUM(BUY_AMOUNT) AS sumBuyAmount
                
            FROM BAOFU_TRADE.T_TRADE_RECEIPT receipt 
            WHERE 
                receipt.TARGET_CURRENCY = '{small_ccy}' 
                AND receipt.TRADE_DIRECTION = 1 
                AND receipt.STATUS = 2 
                AND receipt.CREATE_AT >= '{start_date}' 
                AND receipt.CREATE_AT <= '{end_date}'
            GROUP BY 
                receipt.SOURCE_CURRENCY,
                receipt.TARGET_CURRENCY
            """
            
            # 2. 严格按照用户提供的第二个SQL查询：TRADE_DIRECTION = 2
            sql_direction2 = f"""
            SELECT 
                SOURCE_CURRENCY AS buyCcy,
                TARGET_CURRENCY AS sellCcy,
                2 AS TRADE_DIRECTION,
                SUM(SALE_AMOUNT) AS sumSellAmount,
                SUM(BUY_AMOUNT) AS sumBuyAmount
            FROM BAOFU_TRADE.T_TRADE_RECEIPT receipt 
            WHERE 
                receipt.TARGET_CURRENCY = '{small_ccy}' 
                AND receipt.TRADE_DIRECTION = 2 
                AND receipt.STATUS = 2 
                AND receipt.CREATE_AT >= '{start_date}' 
                AND receipt.CREATE_AT <= '{end_date}'
            GROUP BY 
                receipt.SOURCE_CURRENCY,
                receipt.TARGET_CURRENCY
            """
            
            # 执行查询
            result_direction1 = execute_db(self.env, sql_direction1, database='BAOFU_TRADE')
            result_direction2 = execute_db(self.env, sql_direction2, database='BAOFU_TRADE')
            
            # 打印用户提供的SQL查询结果
            print(f"\n{'='*50}")
            print(f"用户提供的SQL查询结果")
            print(f"{'='*50}")
            
            # 打印第一个SQL结果（TRADE_DIRECTION = 1）
            print(f"\n【SQL 1: TRADE_DIRECTION = 1】")
            if result_direction1:
                print(f"buyCcy | sellCcy | sumBuyAmount | sumSellAmount")
                print(f"-"*50)
                for row in result_direction1:
                    print(f"{row['buyCcy']} | {row['sellCcy']} | {float(row['sumBuyAmount'] or 0):.2f} | {float(row['sumSellAmount'] or 0):.2f}")
            else:
                print(f"未查询到数据")
            
            # 打印第二个SQL结果（TRADE_DIRECTION = 2）
            print(f"\n【SQL 2: TRADE_DIRECTION = 2】")
            if result_direction2:
                print(f"buyCcy | sellCcy | sumBuyAmount | sumSellAmount")
                print(f"-"*50)
                for row in result_direction2:
                    print(f"{row['buyCcy']} | {row['sellCcy']} | {float(row['sumBuyAmount'] or 0):.2f} | {float(row['sumSellAmount'] or 0):.2f}")
            else:
                print(f"未查询到数据")
            
            # 计算统计结果
            print(f"\n{'='*60}")
            print(f"统计结果汇总")
            print(f"{'='*60}")
            print(f"基于SQL查询结果的统计说明：")
            print(f"- TRADE_DIRECTION 1: 买入buyCcy，卖出sellCcy")
            print(f"- TRADE_DIRECTION 2: 买入sellCcy，卖出buyCcy")
            print(f"- 交易内容格式：'用卖出金额 卖出币种 买入 买入金额 买入币种'")
            print(f"- 统计结果基于实际交易数据动态计算")
            
            # 初始化统计变量
            # 1. 客户当月卖出金额（小币种）：TRADE_DIRECTION=1时，sellCcy为小币种的sell_amount总和
            sell_small_total = 0.0
            
            # 2. 客户当月买入：按不同币种统计
            buy_currency_total = {}
            
            # 3. 客户当月买入金额（小币种）：TRADE_DIRECTION=2时，buy_amount的总和
            buy_small_total = 0.0
            
            # 4. 客户当月卖出：按不同币种统计
            sell_currency_total = {}
            
            # 处理TRADE_DIRECTION=1的数据
            print(f"\nTRADE_DIRECTION=1 交易分析：")
            print(f"交易笔数：{len(result_direction1)}")
            
            for i, trade in enumerate(result_direction1, 1):
                buy_ccy = trade['buyCcy']
                sell_ccy = trade['sellCcy']
                buy_amount = float(trade['sumBuyAmount'] or 0)
                sell_amount = float(trade['sumSellAmount'] or 0)
                
                print(f"\n{i}. 交易内容：用{sell_amount:.2f} {sell_ccy} 买入 {buy_amount:.2f} {buy_ccy}")
                
                # 统计逻辑 TRADE_DIRECTION=1
                if sell_ccy == small_ccy:  # 卖出币种是小币种
                    # 1. 客户当月卖出金额（小币种）
                    sell_small_total += sell_amount
                    print(f"   -> 计入'客户当月卖出金额（小币种-{small_ccy}）': +{sell_amount:.2f} {small_ccy}")
                
                # 2. 客户当月买入：按不同币种统计
                if buy_ccy not in buy_currency_total:
                    buy_currency_total[buy_ccy] = 0.0
                buy_currency_total[buy_ccy] += buy_amount
                print(f"   -> 计入'客户当月买入': +{buy_amount:.2f} {buy_ccy}")
            
            # 处理TRADE_DIRECTION=2的数据
            print(f"\nTRADE_DIRECTION=2 交易分析：")
            print(f"交易笔数：{len(result_direction2)}")
            
            for i, trade in enumerate(result_direction2, 1):
                buy_ccy = trade['buyCcy']
                sell_ccy = trade['sellCcy']
                buy_amount = float(trade['sumBuyAmount'] or 0)
                sell_amount = float(trade['sumSellAmount'] or 0)
                
                # TRADE_DIRECTION=2: 买入sellCcy，卖出buyCcy，所以交易内容应该是：用sell_amount buy_ccy 买入 buy_amount sell_ccy
                print(f"\n{i}. 交易内容：用{sell_amount:.2f} {buy_ccy} 买入 {buy_amount:.2f} {sell_ccy}")
                
                # 统计逻辑 TRADE_DIRECTION=2
                # 3. 客户当月买入金额（小币种）：直接使用buy_amount作为买入的小币种金额
                buy_small_total += buy_amount
                print(f"   -> 计入'客户当月买入金额（小币种-{small_ccy}）': +{buy_amount:.2f} {small_ccy}")
                
                # 4. 客户当月卖出：按不同币种统计sell_amount
                if buy_ccy not in sell_currency_total:
                    sell_currency_total[buy_ccy] = 0.0
                sell_currency_total[buy_ccy] += sell_amount
                print(f"   -> 计入'客户当月卖出': +{sell_amount:.2f} {buy_ccy}")
            
            # 打印统计结果
            print(f"\n{'='*60}")
            print(f"最终统计结果")
            print(f"{'='*60}")
            
            # 1. 客户当月卖出金额（小币种）
            print(f"1. 客户当月卖出金额（小币种-{small_ccy}）：")
            print(f"   计算方式：TRADE_DIRECTION=1时，sellCcy为{small_ccy}的sell_amount总和")
            print(f"   结果：{sell_small_total:.2f} {small_ccy}")
            
            # 2. 客户当月买入
            print(f"\n2. 客户当月买入：")
            print(f"   计算方式：TRADE_DIRECTION=1时，按不同币种统计buy_amount总和")
            print(f"   结果：")
            for ccy, amount in buy_currency_total.items():
                print(f"     {amount:.2f} {ccy}")
            
            # 3. 客户当月买入金额（小币种）
            print(f"\n3. 客户当月买入金额（小币种-{small_ccy}）：")
            print(f"   计算方式：TRADE_DIRECTION=2时，buy_amount的总和")
            print(f"   结果：{buy_small_total:.2f} {small_ccy}")
            
            # 4. 客户当月卖出
            print(f"\n4. 客户当月卖出：")
            print(f"   计算方式：TRADE_DIRECTION=2时，按不同币种统计buy_amount总和")
            print(f"   结果：")
            for ccy, amount in sell_currency_total.items():
                print(f"     {amount:.2f} {ccy}")
            
            # 如果没有数据
            if not result_direction1 and not result_direction2:
                print(f"\n未查询到 {small_ccy} 相关的交易数据")

# 主函数
if __name__ == "__main__":
    # 参数配置
    start_date = '2026-01-01 00:00:00'
    end_date = '2026-01-08 23:59:59'
    ccy = ['KRW']
    env = 'UAT'
    
    # 创建统计实例
    stats = CustomerTradeStatistics(env=env)
    # 执行统计 客户当月卖出和买入金额
    stats.statistics_trade_data(start_date, end_date, ccy)
