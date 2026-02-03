#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author    : AI Assistant
@Date      : 2024/04/15
@Description: 渠道当月结算金额调整脚本 - 处理小币种结算金额
"""
import sys
import os
from datetime import datetime

# 导入数据库配置模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Kuajing.Common.kjMysql import get_db_config
import pymysql

class ChannelSettlementAdjuster:
    def __init__(self, env='FAT'):
        """初始化数据库连接"""
        # 获取数据库配置
        self.db_config = get_db_config(env)
        self.db_config['database'] = 'BAOFU_CBCA'
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
    
    def query_fund_center_order(self, payment_ccy, start_date=None, end_date=None):
        """
        查询T_FUND_CENTER_ORDER表数据
        :param payment_ccy: 付款币种
        :param start_date: 开始日期，可选，默认为当月第一天
        :param end_date: 结束日期，可选，默认为当月最后一天
        :return: 查询结果列表和汇总数据
        """
        # 确定日期范围
        if not start_date or not end_date:
            # 使用默认时间范围：2025-11-01 至 2025-11-26
            start_date = '2025-11-01'
            end_date = '2025-11-26'
        
        # 格式化日期时间范围
        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"
        
        print(f"\n===== 查询T_FUND_CENTER_ORDER表数据 =====")
        print(f"查询条件：付款币种={payment_ccy}，日期范围={start_date}至{end_date}")
        
        # 查询需要的字段
        sql = """
        SELECT 
            ID, SOURCE_AMT, SOURCE_CCY, DEST_AMT, DEST_CCY, 
            ARRIVED_CCY, ARRIVED_AMT, CAL_DEST_CCY, CAL_DEST_AMT, 
            CAL_RATE, STATUS, API_FLAG, EXCHANGE_TRADE_PARTY, 
            POBO_PAY, CURRENCY_PAIR, VIRTUAL_USD_CCY, VIRTUAL_USD_AMT
        FROM 
            T_FUND_CENTER_ORDER
        WHERE 
            SOURCE_CCY = %s
            AND CREATE_AT BETWEEN %s AND %s
            AND STATUS = 5
        """
        
        self.cursor.execute(sql, (payment_ccy, start_datetime, end_datetime))
        results = self.cursor.fetchall()
        
        print(f"查询到 {len(results)} 条记录")
        
        # 初始化汇总数据
        summary = {
            'total_records': len(results),
            'arrived_usd_count': 0,
            'arrived_non_usd_count': 0,
            'total_payment_amount': 0.0,  # 付款小币种总金额
            'total_arrived_usd_amount': 0.0,  # 累计到账USD金额
            'total_virtual_usd_amount': 0.0,  # 累计虚拟USD金额
            'records': results,
            'usd_records': [],  # 到账币种为USD的记录
            'non_usd_records': [],  # 到账币种非USD的记录
            'usd_payment_amount': 0.0,  # USD类别的付款金额总和
            'non_usd_payment_amount': 0.0  # 非USD类别的付款金额总和
        }
        
        # 处理每条记录并分类
        for record in results:
            # 将decimal类型转换为float
            source_amt = float(record['SOURCE_AMT'] or 0.0)
            arrived_amt = float(record['ARRIVED_AMT'] or 0.0)
            virtual_usd_amt = float(record['VIRTUAL_USD_AMT'] or 0.0)
            
            # 更新总汇总数据
            summary['total_payment_amount'] += source_amt
            
            # 判断到账币种是否为USD
            arrived_ccy = record['ARRIVED_CCY'] or ''
            if arrived_ccy.upper() == 'USD':
                summary['arrived_usd_count'] += 1
                summary['total_arrived_usd_amount'] += arrived_amt
                summary['usd_records'].append(record)
                summary['usd_payment_amount'] += source_amt  # 更新USD类别付款金额
            else:
                summary['arrived_non_usd_count'] += 1
                summary['total_virtual_usd_amount'] += virtual_usd_amt
                summary['non_usd_records'].append(record)
                summary['non_usd_payment_amount'] += source_amt  # 更新非USD类别付款金额
        
        # 按照用户要求的格式打印数据
        self.print_ordered_records(summary, payment_ccy)
        
        # 应用逻辑并计算结算金额
        self.calculate_settlement_amounts(summary, payment_ccy)
        
        # 按币种对统计
        self.calculate_currency_pair_statistics(results)
        
        # 查看当前数据的到账币种
        print("\n===== 当前数据的到账币种情况 =====")
        arrived_ccys = set()
        for record in results:
            if record['ARRIVED_CCY']:
                arrived_ccys.add(record['ARRIVED_CCY'])
            if record['DEST_CCY']:
                arrived_ccys.add(record['DEST_CCY'])
        print(f"当前数据中出现的币种: {', '.join(sorted(arrived_ccys))}")
        
        return summary
    
    def get_status_text(self, status_code):
        """获取状态的文本描述"""
        status_map = {
            1: '待审核',
            2: '待出款',
            3: '出款中',
            4: '已出款',
            5: '已入账',
            6: '已取消'
        }
        return status_map.get(status_code, '未知')
    
    def print_ordered_records(self, summary, payment_ccy):
        """按照用户要求的格式打印分类记录"""
        
        # 1. 打印付款是小币种-到账是美金的数据
        print("\n" + "=" * 120)
        print(f"付款是小币种({payment_ccy})-到账是美金的数据如下：")
        print("=" * 120)
        
        if summary['usd_records']:
            # 打印表头
            print(f"{'订单号':<15}|{'付款金额':<15}|{'到账金额':<15}|{'状态':<8}")
            print("-" * 120)
            
            # 计算当前分类的到账USD总和
            usd_arrived_total = sum(float(record['ARRIVED_AMT'] or 0.0) for record in summary['usd_records'])
            
            # 打印每条记录
            for record in summary['usd_records']:
                status_text = self.get_status_text(record['STATUS'])
                source_amt = float(record['SOURCE_AMT'] or 0.0)
                arrived_amt = float(record['ARRIVED_AMT'] or 0.0)
                source_ccy = record['SOURCE_CCY'] or ''
                arrived_ccy = record['ARRIVED_CCY'] or ''
                print(f"{record['ID']:<15}|{source_amt:<10.2f} {source_ccy:<3}|{arrived_amt:<10.2f} {arrived_ccy:<3}|{status_text:<8}")
            
            # 打印累计金额（仅当前分类）
            print("-" * 120)
            print(f"{'累计金额':<15}|{summary['usd_payment_amount']:<10.2f} {payment_ccy:<3}|{usd_arrived_total:<10.2f} USD|")
        else:
            print("暂无相关数据")
        
        # 2. 打印付款是小币种-到账不是美金的数据
        print("\n" + "=" * 120)
        print(f"付款是小币种({payment_ccy})-到账不是美金的数据如下：")
        print("=" * 120)
        
        if summary['non_usd_records']:
            # 打印表头
            print(f"{'订单号':<15}|{'付款金额':<15}|{'虚拟美金':<15}|{'状态':<8}")
            print("-" * 120)
            
            # 计算当前分类的虚拟USD总和
            non_usd_virtual_total = sum(float(record['VIRTUAL_USD_AMT'] or 0.0) for record in summary['non_usd_records'])
            
            # 打印每条记录
            for record in summary['non_usd_records']:
                status_text = self.get_status_text(record['STATUS'])
                source_amt = float(record['SOURCE_AMT'] or 0.0)
                virtual_usd_amt = float(record['VIRTUAL_USD_AMT'] or 0.0)
                source_ccy = record['SOURCE_CCY'] or ''
                print(f"{record['ID']:<15}|{source_amt:<10.2f} {source_ccy:<3}|{virtual_usd_amt:<10.2f} USD  |{status_text:<8}")
            
            # 打印累计金额（仅当前分类）
            print("-" * 120)
            print(f"{'累计金额':<15}|{summary['non_usd_payment_amount']:<10.2f} {payment_ccy:<3}|{non_usd_virtual_total:<10.2f} USD|")
        else:
            print("暂无相关数据")
    
    def print_detailed_fields(self, results):
        """打印所有需要的详细字段数据"""
        print("\n所有字段详细数据：")
        print("-" * 150)
        
        for i, record in enumerate(results, 1):
            print(f"\n记录 {i}：")
            print(f"  付款金额(SOURCE_AMT): {record['SOURCE_AMT']}")
            print(f"  付款币种(SOURCE_CCY): {record['SOURCE_CCY']}")
            print(f"  收款金额(DEST_AMT): {record['DEST_AMT']}")
            print(f"  收款币种(DEST_CCY): {record['DEST_CCY']}")
            print(f"  实际出款币种(ARRIVED_CCY): {record['ARRIVED_CCY']}")
            print(f"  实际出款金额(ARRIVED_AMT): {record['ARRIVED_AMT']}")
            print(f"  实际计算收款币种(CAL_DEST_CCY): {record['CAL_DEST_CCY']}")
            print(f"  实际计算收款金额(CAL_DEST_AMT): {record['CAL_DEST_AMT']}")
            print(f"  实际计算汇率(CAL_RATE): {record['CAL_RATE']}")
            print(f"  状态(STATUS): {record['STATUS']} - {self.get_status_text(record['STATUS'])}")
            print(f"  是否走API(API_FLAG): {'是' if record['API_FLAG'] == 1 else '否'}")
            print(f"  汇兑发生方(EXCHANGE_TRADE_PARTY): {'收款' if record['EXCHANGE_TRADE_PARTY'] == 1 else '付款' if record['EXCHANGE_TRADE_PARTY'] == 2 else '未知'}")
            print(f"  是否POBO付款(POBO_PAY): {'是' if record['POBO_PAY'] == 1 else '否'}")
            print(f"  货币对(CURRENCY_PAIR): {record['CURRENCY_PAIR']}")
            print(f"  虚拟美金币种(VIRTUAL_USD_CCY): {record['VIRTUAL_USD_CCY']}")
            print(f"  虚拟美金金额(VIRTUAL_USD_AMT): {record['VIRTUAL_USD_AMT']}")
            print("-" * 150)
    
    def calculate_settlement_amounts(self, summary, payment_ccy):
        """计算结算金额并应用逻辑"""
        print("\n===== 结算金额计算结果 =====")
        
        # 统计数据
        print(f"\n统计数据：")
        print(f"  总记录数: {summary['total_records']}")
        print(f"  到账币种为USD的记录数: {summary['arrived_usd_count']}")
        print(f"  到账币种非USD的记录数: {summary['arrived_non_usd_count']}")
        
        # 汇总金额
        print(f"\n汇总金额：")
        print(f"  付款小币种({payment_ccy})总金额: {summary['total_payment_amount']:.2f} {payment_ccy}")
        print(f"  累计到账USD金额: {summary['total_arrived_usd_amount']:.2f} USD")
        print(f"  累计虚拟USD金额: {summary['total_virtual_usd_amount']:.2f} USD")
        
        # 应用逻辑1和逻辑2
        print(f"\n应用结算规则：")
        print("逻辑1：当付款币种是小币种，到账币种非美金，则渠道当月结算金额（小币种）取付款金额，渠道当月结算金额（美金）取虚拟美金字段")
        print("逻辑2：当付款币种是小币种，到账币种为美金，则渠道当月结算金额（小币种）取付款金额，渠道当月结算金额（美金）取到账美金字段")
        
        # 计算最终结算金额
        final_local_amount = summary['total_payment_amount']  # 渠道当月结算金额（小币种）
        final_usd_amount = summary['total_arrived_usd_amount'] + summary['total_virtual_usd_amount']  # 渠道当月结算金额（美金）
        
        print(f"\n最终结算金额：")
        print(f"  渠道当月结算金额（小币种-{payment_ccy}）: {final_local_amount:.2f} {payment_ccy}")
        print(f"  渠道当月结算金额（美金-USD）: {final_usd_amount:.2f} USD")
    
    def calculate_currency_pair_statistics(self, results):
        """
        按币种对统计付款和收款金额
        :param results: 查询结果列表
        """
        print("\n===== 币种对统计结果 =====")
        
        # 按币种对分组统计
        currency_stats = {}
        for record in results:
            sell_ccy = record['SOURCE_CCY'] or ''
            buy_ccy = record['DEST_CCY'] or ''
            sell_amt = float(record['SOURCE_AMT'] or 0.0)
            buy_amt = float(record['DEST_AMT'] or 0.0)
            
            pair_key = f"{sell_ccy}-{buy_ccy}"
            if pair_key not in currency_stats:
                currency_stats[pair_key] = {
                    'sellCcy': sell_ccy,
                    'buyCcy': buy_ccy,
                    'total_sellAmt': 0.0,
                    'total_buyAmt': 0.0,
                    'count': 0
                }
            
            currency_stats[pair_key]['total_sellAmt'] += sell_amt
            currency_stats[pair_key]['total_buyAmt'] += buy_amt
            currency_stats[pair_key]['count'] += 1
        
        # 打印统计结果
        print(f"{'币种对':<20}|{'sellCcy':<10}|{'buyCcy':<10}|{'sellAmt':<15}|{'buyAmt':<15}|{'交易笔数':<10}")
        print("-" * 90)
        
        for pair_key, stats in currency_stats.items():
            print(f"{pair_key:<20}|{stats['sellCcy']:<10}|{stats['buyCcy']:<10}|{stats['total_sellAmt']:<15.2f}|{stats['total_buyAmt']:<15.2f}|{stats['count']:<10}")
        
        # 打印总计
        total_sell = sum(stats['total_sellAmt'] for stats in currency_stats.values())
        total_buy = sum(stats['total_buyAmt'] for stats in currency_stats.values())
        total_count = sum(stats['count'] for stats in currency_stats.values())
        
        print("-" * 90)
        print(f"{'总计':<20}|{'':<10}|{'':<10}|{total_sell:<15.2f}|{total_buy:<15.2f}|{total_count:<10}")
    
    def calculate_small_currency_usd_payment(self, results, ccy):
        """
        统计到账币种是小币种，付款币种是美金USD的情况
        :param results: 查询结果列表
        :param ccy: 要统计的小币种
        """
        print(f"\n===== 到账币种是小币种({ccy})，付款币种是美金USD的统计结果 =====")
        
        # 使用传入的ccy参数作为唯一的小币种
        small_currency = ccy.upper()
        
        # 初始化统计数据
        usd_payment_stats = {
            'records': [],
            'total_small_currency': 0.0,
            'total_usd': 0.0
        }
        
        # 处理每条记录
        for record in results:
            # 先确定实际的到账币种（优先使用ARRIVED_CCY，如果为空则使用DEST_CCY）
            arrived_ccy = record['ARRIVED_CCY'] or record['DEST_CCY'] or ''
            source_ccy = record['SOURCE_CCY'] or ''
            
            # 判断到账币种是否为指定的小币种且付款币种是USD
            if arrived_ccy.upper() == small_currency and source_ccy.upper() == 'USD':
                # 使用ARRIVED_AMT作为到账金额，如果为空则使用DEST_AMT，或者检查其他可能存储到账金额的字段
                arrived_amt = float(record['ARRIVED_AMT'] or record['DEST_AMT'] or record['CAL_DEST_AMT'] or 0.0)
                source_amt = float(record['SOURCE_AMT'] or 0.0)
                
                usd_payment_stats['records'].append(record)
                usd_payment_stats['total_small_currency'] += arrived_amt
                usd_payment_stats['total_usd'] += source_amt
        
        # 打印付款币种是USD的情况
        print("\n" + "=" * 120)
        print("到账币种是小币种，付款币种是美金USD的数据如下：")
        print("=" * 120)
        
        if usd_payment_stats['records']:
            # 打印表头
            print(f"{'订单号':<15}|{'付款金额(USD)':<18}|{'到账金额(小币种)':<20}|{'虚拟美金币种':<15}|{'虚拟美金金额':<18}|{'状态':<8}")
            print("-" * 140)
            
            # 打印每条记录
            for record in usd_payment_stats['records']:
                status_text = self.get_status_text(record['STATUS'])
                source_amt = float(record['SOURCE_AMT'] or 0.0)
                # 使用与统计累计金额时相同的逻辑来获取到账金额
                arrived_amt = float(record['ARRIVED_AMT'] or record['DEST_AMT'] or record['CAL_DEST_AMT'] or 0.0)
                arrived_ccy = record['ARRIVED_CCY'] or record['DEST_CCY'] or ''
                virtual_usd_ccy = record['VIRTUAL_USD_CCY'] or ''
                virtual_usd_amt = float(record['VIRTUAL_USD_AMT'] or 0.0)
                print(f"{record['ID']:<15}|{source_amt:<13.2f} USD|{arrived_amt:<15.2f} {arrived_ccy:<3}|{virtual_usd_ccy:<15}|{virtual_usd_amt:<13.2f}|{status_text:<8}")
            
            # 打印累计金额
            print("-" * 140)
            print(f"{'累计金额':<15}|{usd_payment_stats['total_usd']:<13.2f} USD|{usd_payment_stats['total_small_currency']:<15.2f} {small_currency}|{'':<15}|{'':<18}|{''}")
        else:
            print("暂无相关数据")
    
    def calculate_small_currency_non_usd_payment(self, results, ccy):
        """
        统计到账币种是小币种，付款币种是非美金的情况
        :param results: 查询结果列表
        :param ccy: 要统计的小币种
        """
        print(f"\n===== 到账币种是小币种({ccy})，付款币种是非美金的统计结果 =====")
        
        # 使用传入的ccy参数作为唯一的小币种
        small_currency = ccy.upper()
        
        # 初始化统计数据
        non_usd_payment_stats = {
            'records': [],
            'total_small_currency': 0.0,
            'total_non_usd': 0.0
        }
        
        # 处理每条记录
        for record in results:
            # 先确定实际的到账币种（优先使用ARRIVED_CCY，如果为空则使用DEST_CCY）
            arrived_ccy = record['ARRIVED_CCY'] or record['DEST_CCY'] or ''
            source_ccy = record['SOURCE_CCY'] or ''
            
            # 判断到账币种是否为指定的小币种且付款币种是非USD
            if arrived_ccy.upper() == small_currency and source_ccy.upper() != 'USD':
                # 使用ARRIVED_AMT作为到账金额，如果为空则使用DEST_AMT，或者检查其他可能存储到账金额的字段
                arrived_amt = float(record['ARRIVED_AMT'] or record['DEST_AMT'] or record['CAL_DEST_AMT'] or 0.0)
                source_amt = float(record['SOURCE_AMT'] or 0.0)
                
                non_usd_payment_stats['records'].append(record)
                non_usd_payment_stats['total_small_currency'] += arrived_amt
                non_usd_payment_stats['total_non_usd'] += source_amt
        
        # 打印付款币种是非USD的情况
        print("\n" + "=" * 120)
        print("到账币种是小币种，付款币种是非美金的数据如下：")
        print("=" * 120)
        
        if non_usd_payment_stats['records']:
            # 打印表头
            print(f"{'订单号':<15}|{'付款金额(非USD)':<20}|{'到账金额(小币种)':<20}|{'虚拟美金币种':<15}|{'虚拟美金金额':<18}|{'状态':<8}")
            print("-" * 140)
            
            # 打印每条记录
            for record in non_usd_payment_stats['records']:
                status_text = self.get_status_text(record['STATUS'])
                source_amt = float(record['SOURCE_AMT'] or 0.0)
                arrived_amt = float(record['ARRIVED_AMT'] or 0.0)
                source_ccy = record['SOURCE_CCY'] or ''
                arrived_ccy = record['ARRIVED_CCY'] or ''
                virtual_usd_ccy = record['VIRTUAL_USD_CCY'] or ''
                virtual_usd_amt = float(record['VIRTUAL_USD_AMT'] or 0.0)
                print(f"{record['ID']:<15}|{source_amt:<15.2f} {source_ccy:<3}|{arrived_amt:<15.2f} {arrived_ccy:<3}|{virtual_usd_ccy:<15}|{virtual_usd_amt:<13.2f}|{status_text:<8}")
            
            # 打印累计金额
            print("-" * 140)
            # 对于非USD付款，我们需要确定共同的付款币种和到账币种
            if non_usd_payment_stats['records']:
                # 获取第一条记录的付款币种和到账币种作为累计金额的币种
                common_source_ccy = non_usd_payment_stats['records'][0]['SOURCE_CCY'] or ''
                # 使用与统计时相同的逻辑来确定到账币种
                common_arrived_ccy = non_usd_payment_stats['records'][0]['ARRIVED_CCY'] or non_usd_payment_stats['records'][0]['DEST_CCY'] or ''
                print(f"{'累计金额':<15}|{non_usd_payment_stats['total_non_usd']:<15.2f} {common_source_ccy:<3}|{non_usd_payment_stats['total_small_currency']:<15.2f} {common_arrived_ccy:<3}|{'':<15}|{'':<18}|{''}")
            else:
                print(f"{'累计金额':<15}|{non_usd_payment_stats['total_non_usd']:<15.2f}|{non_usd_payment_stats['total_small_currency']:<15.2f}|{'':<15}|{'':<18}|{''}")
        else:
            print("暂无相关数据")
    
    def calculate_arrived_small_currency_statistics(self, results, ccy):
        """
        调用两个独立的方法分别统计到账币种是小币种的情况
        :param results: 查询结果列表
        :param ccy: 要统计的小币种
        """
        # 调用两个独立的统计方法
        self.calculate_small_currency_usd_payment(results, ccy)
        self.calculate_small_currency_non_usd_payment(results, ccy)
    
    def query_small_currency_arrived_records(self, start_date, end_date, ccy):
        """
        查询到账币种是指定小币种的所有记录，用于统计分析
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param ccy: 要查询的小币种
        :return: 查询结果列表
        """
        # 使用传入的ccy参数作为唯一的小币种
        small_currency = ccy.upper()
        
        # 格式化日期时间范围
        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"
        
        print(f"\n===== 查询到账币种是小币种({small_currency})的所有记录 =====")
        print(f"查询条件：日期范围={start_date}至{end_date}，到账币种={small_currency}")
        
        # 查询需要的字段
        sql = """
        SELECT 
            ID, SOURCE_AMT, SOURCE_CCY, DEST_AMT, DEST_CCY, 
            ARRIVED_CCY, ARRIVED_AMT, CAL_DEST_CCY, CAL_DEST_AMT, 
            CAL_RATE, STATUS, API_FLAG, EXCHANGE_TRADE_PARTY, 
            POBO_PAY, CURRENCY_PAIR, VIRTUAL_USD_CCY, VIRTUAL_USD_AMT
        FROM 
            T_FUND_CENTER_ORDER
        WHERE 
            (ARRIVED_CCY = %s OR DEST_CCY = %s)
            AND CREATE_AT BETWEEN %s AND %s
            AND STATUS = 5
        """
        
        self.cursor.execute(sql, (small_currency, small_currency, start_datetime, end_datetime))
        results = self.cursor.fetchall()
        
        print(f"查询到 {len(results)} 条到账币种是小币种的记录")
        return results
    
   

if __name__ == "__main__":
    """主函数入口"""
    # 从命令行参数获取币种和日期范围
    ccy = 'MYR'
    start_date = '2025-11-01'
    end_date = '2025-11-26'
    
    print(f"启动渠道当月结算金额调整脚本")
    print(f"查询币种: {ccy}")
    
    # 创建实例
    adjuster = ChannelSettlementAdjuster(env='FAT')
    
    # 直接使用指定的日期范围，不调用已删除的get_default_date_range方法
    
    # 查询指定付款币种的数据
    summary = adjuster.query_fund_center_order(ccy, start_date, end_date)
    
    # 查询所有到账币种是指定小币种的记录，用于统计分析
    small_currency_results = adjuster.query_small_currency_arrived_records(start_date, end_date, ccy)
    
    # 对到账币种是指定小币种的记录进行统计
    adjuster.calculate_arrived_small_currency_statistics(small_currency_results, ccy)
    
    # 关闭数据库连接
    adjuster.close_db()
    
    print("\n脚本执行完成")