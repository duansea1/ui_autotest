#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author    : AI Assistant
@Date      : 2024/04/15
@Description: 小币种损益汇总-渠道金额获取脚本
"""
import sys
import os
import json
from datetime import datetime

# 导入数据库配置模块
from Kuajing.Common.kjMysql import get_db_config
import pymysql

class CurrencyAmountQuery:
    def __init__(self, env='FAT'):
        """初始化数据库连接"""
        # 获取数据库配置
        self.db_config = get_db_config(env)
        # 注意：用户提供的表结构中数据库名是BAOFU_CBCA，但配置文件中是BAOFU_CBA
        # 这里我们使用用户提供的表结构中的数据库名
        self.db_config['database'] = 'BAOFU_CBCA'
        self.conn = None
        self.cursor = None
        self.connect_db()
    
    def connect_db(self):
        """建立数据库连接"""
        try:
            self.conn = pymysql.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            print(f"成功连接到数据库：{self.db_config['host']}:{self.db_config['port']} - {self.db_config['database']}")
        except Exception as e:
            print(f"数据库连接失败: {str(e)}")
            raise
    
    def close_db(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def query_channel_settle_data(self, start_date, end_date, currencies):
        """
        查询渠道结算订单表(T_CHANNEL_SETTLE_ORDER)数据
        :param start_date: 开始日期，格式：YYYY-MM-DD
        :param end_date: 结束日期，格式：YYYY-MM-DD
        :param currencies: 小币种列表
        :return: 查询结果字典
        """
        result = {}
        
        # 格式化日期为datetime对象
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        # 转换为当月的第一天和最后一天
        start_of_month = start_dt.replace(day=1).strftime('%Y-%m-%d 00:00:00')
        # 计算当月最后一天
        import calendar
        last_day = calendar.monthrange(end_dt.year, end_dt.month)[1]
        end_of_month = end_dt.replace(day=last_day).strftime('%Y-%m-%d 23:59:59')
        
        print(f"查询区间：{start_of_month} 至 {end_of_month}")
        
        for ccy in currencies:
            ccy = ccy.strip()  # 去除空格
            result[ccy] = {
                'count': 0,
                'local_amount': 0.0,  # 小币种金额
                'usd_amount': 0.0    # 美元金额
            }
            
            try:
                # 查询符合条件的记录
                sql = """SELECT COUNT(*) as count, SUM(SETTLE_AMT) as local_sum, SUM(REAL_SETTLE_AMT) as usd_sum 
                         FROM T_CHANNEL_SETTLE_ORDER 
                         WHERE CREATE_AT >= %s AND CREATE_AT <= %s 
                         AND STATE = 2  -- 结算成功
                         AND SETTLE_CCY = %s  -- 小币种
                         AND REAL_SETTLE_CCY = 'USD'  -- 实际到账币种为美元
                      """
                
                self.cursor.execute(sql, (start_of_month, end_of_month, ccy))
                row = self.cursor.fetchone()
                
                if row:
                    result[ccy]['count'] = row['count'] or 0
                    # 将decimal.Decimal类型转换为float类型
                    result[ccy]['local_amount'] = float(row['local_sum'] or 0.0)
                    result[ccy]['usd_amount'] = float(row['usd_sum'] or 0.0)
                    
                # 打印日志
                print(f"T_CHANNEL_SETTLE_ORDER表  {ccy} 符合条件的明细{result[ccy]['count']}条")
                print(f"T_CHANNEL_SETTLE_ORDER表  渠道当月结算金额（小币种-{ccy}）：{result[ccy]['local_amount']}   渠道当月结算金额（美元）：{result[ccy]['usd_amount']}")
                
            except Exception as e:
                print(f"查询T_CHANNEL_SETTLE_ORDER表{ccy}数据时发生错误: {str(e)}")
        
        return result
    
    def query_fund_transfer_data(self, start_date, end_date, currencies):
        """
        查询资金调拨交易订单表(T_FUND_TRANSFER_ORDER)数据，并根据需求计算渠道当月结算金额
        :param start_date: 开始日期，格式：YYYY-MM-DD
        :param end_date: 结束日期，格式：YYYY-MM-DD
        :param currencies: 小币种列表
        :return: 查询结果字典
        """
        result = {}
        
        # 格式化日期为datetime对象
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        # 转换为当月的第一天和最后一天（筛选条件：开始时间为当月1号凌晨，结束时间为当月最后一天24点）
        start_of_month = start_dt.replace(day=1).strftime('%Y-%m-%d 00:00:00')
        # 计算当月最后一天
        import calendar
        last_day = calendar.monthrange(end_dt.year, end_dt.month)[1]
        end_of_month = end_dt.replace(day=last_day).strftime('%Y-%m-%d 23:59:59')
        
        for ccy in currencies:
            ccy = ccy.strip()  # 去除空格
            result[ccy] = {
                'count': 0,
                'local_amount': 0.0,  # 小币种金额
                'usd_amount': 0.0     # 美元金额
            }
            
            try:
                print(f"\n===== 处理小币种 {ccy} 资金调拨数据 =====")
                print(f"查询区间：{start_of_month} 至 {end_of_month}")
                print(f"结算状态：结算成功 (TRANSFER_STATE IN (3))")
                
                # 查询所有相关记录
                sql = """SELECT 
                            ID, SOURCE_CCY, DEST_CCY, SOURCE_AMT, DEST_AMT
                         FROM T_FUND_TRANSFER_ORDER 
                         WHERE CREATE_AT >= %s AND CREATE_AT <= %s 
                         AND TRANSFER_STATE IN (3)  -- 已汇出或已到账（相当于结算成功）
                         AND (SOURCE_CCY = %s OR DEST_CCY = %s)  -- 源或目标币种为当前小币种
                      """
                
                self.cursor.execute(sql, (start_of_month, end_of_month, ccy, ccy))
                rows = self.cursor.fetchall()
                
                if rows:
                    result[ccy]['count'] = len(rows)
                    print(f"共找到 {len(rows)} 条相关记录")
                    
                    for i, row in enumerate(rows, 1):
                        transfer_id = row['ID']
                        source_ccy = row['SOURCE_CCY']
                        dest_ccy = row['DEST_CCY']
                        source_amt = float(row['SOURCE_AMT'] or 0.0)
                        dest_amt = float(row['DEST_AMT'] or 0.0)
                        virtual_usd_amt = 0.0
                        
                        print(f"\n记录 {i}: 订单ID={transfer_id}")
                        print(f"  付款币种: {source_ccy}, 付款金额: {source_amt:.2f} {source_ccy}")
                        print(f"  到账币种: {dest_ccy}, 到账金额: {dest_amt:.2f} {dest_ccy}")
                        
                        # 情况1：付款币种是小币种，到账币种是美金
                        if source_ccy == ccy and dest_ccy == 'USD':
                            print(f"  处理类型: 情况1 - 付款小币种，到账美金")
                            
                            # 渠道当月结算金额（小币种）取付款小币种金额之和
                            result[ccy]['local_amount'] += source_amt
                            # 渠道当月结算金额（美金）取到账美金字段之和
                            result[ccy]['usd_amount'] += dest_amt
                            
                            print(f"  累计小币种金额: {result[ccy]['local_amount']:.2f} {ccy}")
                            print(f"  累计美元金额: {result[ccy]['usd_amount']:.2f} USD")
                        
                        # 情况2：付款币种是小币种，到账币种非美金
                        elif source_ccy == ccy and dest_ccy != 'USD':
                            print(f"  处理类型: 情况2 - 付款小币种，到账非美金")
                            
                            # 从T_FUND_CENTER_ORDER表获取虚拟美金字段
                            center_sql = """SELECT VIRTUAL_USD_AMT 
                                           FROM T_FUND_CENTER_ORDER 
                                           WHERE ID = %s AND STATUS = 5"""
                            self.cursor.execute(center_sql, (transfer_id,))
                            center_row = self.cursor.fetchone()
                            
                            if center_row:
                                virtual_usd_amt = float(center_row['VIRTUAL_USD_AMT'] or 0.0)
                                print(f"  虚拟美金金额: {virtual_usd_amt:.2f} USD")
                            else:
                                print(f"  警告: 未找到对应T_FUND_CENTER_ORDER记录，虚拟美金金额默认0")
                            
                            # 渠道当月结算金额（小币种）取付款金额之和
                            result[ccy]['local_amount'] += source_amt
                            # 渠道当月结算金额（美金）取虚拟美金字段之和
                            result[ccy]['usd_amount'] += virtual_usd_amt
                            
                            print(f"  累计小币种金额: {result[ccy]['local_amount']:.2f} {ccy}")
                            print(f"  累计美元金额: {result[ccy]['usd_amount']:.2f} USD")
                        
                        # 情况3：到账币种是小币种，付款币种是美金
                        elif dest_ccy == ccy and source_ccy == 'USD':
                            print(f"  处理类型: 情况3 - 到账小币种，付款美金")
                            
                            # 渠道当月结算金额（小币种）减少到账金额
                            result[ccy]['local_amount'] -= dest_amt
                            # 渠道当月结算金额（美元）减少付款金额
                            result[ccy]['usd_amount'] -= source_amt
                            
                            print(f"  累计小币种金额: {result[ccy]['local_amount']:.2f} {ccy}")
                            print(f"  累计美元金额: {result[ccy]['usd_amount']:.2f} USD")
                        
                        # 情况4：到账币种是小币种，付款币种是非美金
                        elif dest_ccy == ccy and source_ccy != 'USD':
                            print(f"  处理类型: 情况4 - 到账小币种，付款非美金")
                            
                            # 从T_FUND_CENTER_ORDER表获取虚拟美金字段
                            center_sql = """SELECT VIRTUAL_USD_AMT 
                                           FROM T_FUND_CENTER_ORDER 
                                           WHERE ID = %s AND STATUS = 5"""
                            self.cursor.execute(center_sql, (transfer_id,))
                            center_row = self.cursor.fetchone()
                            
                            if center_row:
                                virtual_usd_amt = float(center_row['VIRTUAL_USD_AMT'] or 0.0)
                                print(f"  虚拟美金金额: {virtual_usd_amt:.2f} USD")
                            else:
                                print(f"  警告: 未找到对应T_FUND_CENTER_ORDER记录，虚拟美金金额默认0")
                            
                            # 渠道当月结算金额（小币种）减少到账金额
                            result[ccy]['local_amount'] -= dest_amt
                            # 渠道当月结算金额（美元）减少虚拟美金字段
                            result[ccy]['usd_amount'] -= virtual_usd_amt
                            
                            print(f"  累计小币种金额: {result[ccy]['local_amount']:.2f} {ccy}")
                            print(f"  累计美元金额: {result[ccy]['usd_amount']:.2f} USD")
                
                # 打印最终统计结果
                print(f"\n===== T_FUND_TRANSFER_ORDER表 {ccy} 统计结果 =====")
                print(f"符合条件的明细: {result[ccy]['count']}条")
                print(f"渠道当月结算金额（小币种-{ccy}）：{result[ccy]['local_amount']:.2f} {ccy}")
                print(f"渠道当月结算金额（美元）：{result[ccy]['usd_amount']:.2f} USD")
                
            except Exception as e:
                print(f"\n查询T_FUND_TRANSFER_ORDER表{ccy}数据时发生错误: {str(e)}")
                import traceback
                traceback.print_exc()
        
        return result
    
    def calculate_total(self, channel_data, fund_data):
        """
        计算T_CHANNEL_SETTLE_ORDER表和T_FUND_TRANSFER_ORDER表的汇总数据
        :param channel_data: T_CHANNEL_SETTLE_ORDER表查询结果
        :param fund_data: T_FUND_TRANSFER_ORDER表查询结果
        :return: 汇总结果
        """
        total = {}
        
        # 获取所有币种
        currencies = set(channel_data.keys()).union(set(fund_data.keys()))
        
        for ccy in currencies:
            channel_ccy_data = channel_data.get(ccy, {'local_amount': 0.0, 'usd_amount': 0.0})
            fund_ccy_data = fund_data.get(ccy, {'local_amount': 0.0, 'usd_amount': 0.0})
            
            total_local = channel_ccy_data['local_amount'] + fund_ccy_data['local_amount']
            total_usd = channel_ccy_data['usd_amount'] + fund_ccy_data['usd_amount']
            
            total[ccy] = {
                'local_amount': total_local,
                'usd_amount': total_usd
            }
            
            # 打印汇总日志
            print(f"小币种{ccy} T_CHANNEL_SETTLE_ORDER表、T_FUND_TRANSFER_ORDER表汇总   渠道当月结算金额（小币种-{ccy}）：{total_local}   渠道当月结算金额（美元）：{total_usd}")
        
        return total
    
    def run(self, params):
        """
        执行查询并汇总结果
        :param params: 参数字典，包含startRunDate、endRunDate、ccy等
        """
        try:
            # 从参数中提取数据
            start_date = params.get('startRunDate', '')
            end_date = params.get('endRunDate', '')
            currencies = params.get('ccy', [])
            
            # 验证参数
            if not start_date or not end_date:
                raise ValueError("缺少必要的日期参数")
            if not currencies:
                raise ValueError("缺少币种参数")
            
            # 查询T_CHANNEL_SETTLE_ORDER表数据
            print("\n===== 查询T_CHANNEL_SETTLE_ORDER表数据 =====")
            channel_data = self.query_channel_settle_data(start_date, end_date, currencies)
            
            # 查询T_FUND_TRANSFER_ORDER表数据
            print("\n===== 查询T_FUND_TRANSFER_ORDER表数据 =====")
            fund_data = self.query_fund_transfer_data(start_date, end_date, currencies)
            
            # 计算汇总数据
            print("\n===== 计算汇总数据 =====")
            total_data = self.calculate_total(channel_data, fund_data)
            
            return {
                'channel_data': channel_data,
                'fund_data': fund_data,
                'total_data': total_data
            }
            
        finally:
            # 确保关闭数据库连接
            self.close_db()
    
    def compare_fund_transfer_center(self, start_date, end_date, currency=None):
        """
        比对T_FUND_TRANSFER_ORDER和T_FUND_CENTER_ORDER表的数据一致性
        
        Args:
            start_date: 开始日期，格式如'2025-09-01'
            end_date: 结束日期，格式如'2025-09-30'
            currency: 币种，可选参数，不指定则查询所有币种
            
        Returns:
            不一致记录的列表，每条记录包含单号、金额和币种信息
        """
        try:
            # 参数验证
            if not start_date or not end_date:
                raise ValueError("开始日期和结束日期不能为空")
            
            # 连接数据库
            if not self.conn:
                self.connect_db()
                
            print(f"\n===== 比对T_FUND_TRANSFER_ORDER和T_FUND_CENTER_ORDER数据一致性 =====")
            print(f"查询区间：{start_date} 00:00:00 至 {end_date} 23:59:59")
            
            # 简化实现，直接查询两张表的交集并比对
            sql = """
            SELECT 
                ft.ID as TRANSFER_ID,
                fc.ID as CENTER_ID,
                ft.SOURCE_CCY as CCY,
                ft.SOURCE_AMT as TRANSFER_AMT,
                fc.SOURCE_AMT as CENTER_AMT
            FROM 
                T_FUND_TRANSFER_ORDER ft
            JOIN 
                T_FUND_CENTER_ORDER fc ON ft.ID = fc.ID
            WHERE 
                ft.CREATE_AT BETWEEN %s AND %s
                AND fc.CREATE_AT BETWEEN %s AND %s
                AND fc.STATUS = 5
            """
            
            # 参数列表（注意需要重复日期参数）
            params = [
                f"{start_date} 00:00:00", 
                f"{end_date} 23:59:59",
                f"{start_date} 00:00:00", 
                f"{end_date} 23:59:59"
            ]
            
            # 如果指定了币种，添加币种条件
            if currency:
                sql += " AND ft.SOURCE_CCY = %s AND fc.SOURCE_CCY = %s"
                params.append(currency)
                params.append(currency)
            
            # 创建游标并执行查询
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            results = cursor.fetchall()
            cursor.close()
            
            # 筛选不一致的记录
            inconsistent_records = []
            
            # 遍历结果记录
            print(f"\n查询到 {len(results)} 条关联记录进行比对")
            
            for i, row in enumerate(results):
                try:
                    # 检查记录结构
                    if len(row) >= 5:
                        # 安全获取数据
                        transfer_id = row[0] if row[0] is not None else '未知'
                        center_id = row[1] if row[1] is not None else '未知'
                        ccy = row[2] if len(row) > 2 and row[2] is not None else '未知'
                        
                        # 安全转换金额
                        try:
                            transfer_amt = float(row[3]) if len(row) > 3 and row[3] is not None else 0.0
                        except (ValueError, TypeError):
                            print(f"警告：无法将转账金额转换为数字，记录索引 {i}，值: {row[3]}")
                            transfer_amt = 0.0
                            
                        try:
                            center_amt = float(row[4]) if len(row) > 4 and row[4] is not None else 0.0
                        except (ValueError, TypeError):
                            print(f"警告：无法将中心金额转换为数字，记录索引 {i}，值: {row[4]}")
                            center_amt = 0.0
                        
                        # 当金额不一致时记录
                        if abs(transfer_amt - center_amt) > 0.0001:
                            print(f"发现不一致记录：订单ID={transfer_id}, 转账金额={transfer_amt}, 中心金额={center_amt}")
                            inconsistent_records.append({
                                'TRANSFER_ORDER_ID': transfer_id,
                                'CENTER_ORDER_ID': center_id,
                                'CCY': ccy,
                                'TRANSFER_AMT': transfer_amt,
                                'CENTER_AMT': center_amt
                            })
                    else:
                        print(f"警告：记录索引 {i} 数据不完整，只有 {len(row)} 个字段: {row}")
                except Exception as e:
                    print(f"错误：处理记录索引 {i} 时出错: {str(e)}, 记录: {row}")
                    # 继续处理下一条记录而不是中断
                    continue
            
            print(f"\n比对完成，共发现 {len(inconsistent_records)} 条不一致记录")
            return inconsistent_records
            
        except Exception as e:
            import traceback
            print(f"比对数据一致性时发生错误: {str(e)}")
            print("错误详情:")
            traceback.print_exc()
            # 确保在异常情况下返回空列表而不是None
            return []
    
    def query_fund_center_status5(self, start_date, end_date, currency=None):
        """
        查询T_FUND_CENTER_ORDER表中STATUS=5的数据
        
        :param start_date: 开始日期，格式：YYYY-MM-DD
        :param end_date: 结束日期，格式：YYYY-MM-DD
        :param currency: 指定币种，如不指定则查询所有币种
        :return: 查询结果列表，每条记录包含ORDER_NO等字段
        """
        # 验证参数
        if not start_date or not end_date:
            raise ValueError("缺少日期参数")
        
        # 格式化日期为带时间的格式
        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"
        
        print(f"\n===== 查询T_FUND_CENTER_ORDER表STATUS=5的数据 =====")
        print(f"查询区间：{start_datetime} 至 {end_datetime}")
        
        # 构建查询条件
        currency_condition = f"AND SOURCE_CCY = '{currency}'" if currency else ""
        
        # 构建查询SQL
        sql = f"""
        SELECT 
            ID, 
            SOURCE_CCY, 
            SOURCE_AMT, 
            DEST_CCY, 
            DEST_AMT,
            VIRTUAL_USD_CCY,
            VIRTUAL_USD_AMT,
            STATUS,
            CREATE_AT,
            UPDATE_AT
        FROM T_FUND_CENTER_ORDER 
        WHERE CREATE_AT >= '{start_datetime}' 
        AND CREATE_AT <= '{end_datetime}' 
        AND STATUS = 5  -- 成功状态
        {currency_condition}
        ORDER BY CREATE_AT DESC
        """
        
        try:
            # 执行查询
            self.cursor.execute(sql)
            raw_results = self.cursor.fetchall()
            
            # 定义小币种列表（根据实际情况调整）
            small_currencies = ['DKK', 'KRW', 'CNH', 'JPY', 'EUR', 'GBP']
            
            # 初始化渠道结算金额统计，按币种分别统计
            channel_settlement = {
                'by_currency': {},  # 按币种统计的小币种结算金额
                'usd_amount': 0.0     # 渠道当月结算金额（美元）
            }
            
            # 按交易类型分组统计
            transaction_groups = {}
            
            # 转换结果为包含ORDER_NO的字典列表
            results = []
            for row in raw_results:
                source_ccy = row['SOURCE_CCY']
                dest_ccy = row['DEST_CCY']
                source_amt = float(row['SOURCE_AMT'] or 0.0)
                dest_amt = float(row['DEST_AMT'] or 0.0)
                virtual_usd_amt = float(row['VIRTUAL_USD_AMT'] or 0.0)
                
                # 将ID重命名为ORDER_NO
                record = {
                    'ORDER_NO': row['ID'],
                    'ID': row['ID'],
                    'SOURCE_CCY': row['SOURCE_CCY'],
                    'SOURCE_AMT': row['SOURCE_AMT'],
                    'DEST_CCY': row['DEST_CCY'],
                    'DEST_AMT': row['DEST_AMT'],
                    'VIRTUAL_USD_CCY': row['VIRTUAL_USD_CCY'],
                    'VIRTUAL_USD_AMT': row['VIRTUAL_USD_AMT'],
                    'CREATE_AT': row['CREATE_AT']
                }
                results.append(record)
                
                # 构建交易类型标识
                transaction_key = f"{source_ccy}->{dest_ccy}"
                if transaction_key not in transaction_groups:
                    transaction_groups[transaction_key] = {
                        'count': 0,
                        'source_total': 0.0,
                        'dest_total': 0.0,
                        'virtual_usd_total': 0.0
                    }
                
                # 累加交易统计
                transaction_groups[transaction_key]['count'] += 1
                transaction_groups[transaction_key]['source_total'] += source_amt
                transaction_groups[transaction_key]['dest_total'] += dest_amt
                transaction_groups[transaction_key]['virtual_usd_total'] += virtual_usd_amt
            
            # 打印统计信息
            total_records = len(raw_results)
            print(f"\n查询结果统计：")
            print(f"总记录数: {total_records}")
            
            # 按交易类型打印详细统计
            print(f"\n交易类型统计：")
            for txn_type, stats in transaction_groups.items():
                source_ccy = txn_type.split('->')[0]
                dest_ccy = txn_type.split('->')[1]
                
                # 根据业务逻辑计算渠道结算金额
                if source_ccy in small_currencies:
                    # 付款币种是小币种
                    if dest_ccy == 'USD':
                        # 情况1：付款币种是小币种，到账币种是美金
                        # 按币种统计渠道结算金额
                        if source_ccy not in channel_settlement['by_currency']:
                            channel_settlement['by_currency'][source_ccy] = 0.0
                        channel_settlement['by_currency'][source_ccy] += stats['source_total']
                        channel_settlement['usd_amount'] += stats['dest_total']
                        print(f"\n{txn_type} 付款币种是小币种，到账币种是美金：")
                        print(f"  付款币种{source_ccy} 汇总{stats['source_total']:.2f} {source_ccy}")
                        print(f"  到账币种{dest_ccy} 汇总{stats['dest_total']:.2f} {dest_ccy}")
                        print(f"  渠道当月结算金额（小币种）: +{stats['source_total']:.2f} {source_ccy}")
                        print(f"  渠道当月结算金额（美金）: +{stats['dest_total']:.2f} USD")
                    else:
                        # 情况2：付款币种是小币种，到账币种非美金
                        # 按币种统计渠道结算金额
                        if source_ccy not in channel_settlement['by_currency']:
                            channel_settlement['by_currency'][source_ccy] = 0.0
                        channel_settlement['by_currency'][source_ccy] += stats['source_total']
                        channel_settlement['usd_amount'] += stats['virtual_usd_total']
                        print(f"\n{txn_type} 付款币种是小币种，到账币种非美金：")
                        print(f"  付款币种{source_ccy} 汇总{stats['source_total']:.2f} {source_ccy}")
                        print(f"  到账币种{dest_ccy} 汇总{stats['dest_total']:.2f} {dest_ccy}")
                        print(f"  虚拟美金金额: {stats['virtual_usd_total']:.2f} USD")
                        print(f"  渠道当月结算金额（小币种）: +{stats['source_total']:.2f} {source_ccy}")
                        print(f"  渠道当月结算金额（美金）: +{stats['virtual_usd_total']:.2f} USD")
                elif dest_ccy in small_currencies:
                    # 到账币种是小币种
                    if source_ccy == 'USD':
                        # 情况3：到账币种是小币种，付款币种是美金
                        # 按币种统计渠道结算金额
                        if dest_ccy not in channel_settlement['by_currency']:
                            channel_settlement['by_currency'][dest_ccy] = 0.0
                        channel_settlement['by_currency'][dest_ccy] -= stats['dest_total']
                        channel_settlement['usd_amount'] -= stats['source_total']
                        print(f"\n{txn_type} 到账币种是小币种，付款币种是美金：")
                        print(f"  付款币种{source_ccy} 汇总{stats['source_total']:.2f} {source_ccy}")
                        print(f"  到账币种{dest_ccy} 汇总-{stats['dest_total']:.2f} {dest_ccy}（代表减少）")
                        print(f"  渠道当月结算金额（小币种）: -{stats['dest_total']:.2f} {dest_ccy}")
                        print(f"  渠道当月结算金额（美金）: -{stats['source_total']:.2f} USD")
                    else:
                        # 情况4：到账币种是小币种，付款币种是非美金
                        # 按币种统计渠道结算金额
                        if dest_ccy not in channel_settlement['by_currency']:
                            channel_settlement['by_currency'][dest_ccy] = 0.0
                        channel_settlement['by_currency'][dest_ccy] -= stats['dest_total']
                        channel_settlement['usd_amount'] -= stats['virtual_usd_total']
                        print(f"\n{txn_type} 到账币种是小币种，付款币种是非美金：")
                        print(f"  付款币种{source_ccy} 汇总{stats['source_total']:.2f} {source_ccy}")
                        print(f"  到账币种{dest_ccy} 汇总-{stats['dest_total']:.2f} {dest_ccy}（代表减少）")
                        print(f"  虚拟美金金额: {stats['virtual_usd_total']:.2f} USD")
                        print(f"  渠道当月结算金额（小币种）: -{stats['dest_total']:.2f} {dest_ccy}")
                        print(f"  渠道当月结算金额（美金）: -{stats['virtual_usd_total']:.2f} USD")
            
            # 打印最终渠道结算金额
            print(f"\n===== 渠道当月结算金额汇总 =====")
            for ccy, amount in channel_settlement['by_currency'].items():
                print(f"渠道当月结算金额（小币种-{ccy}）: {amount:.2f} {ccy}")
            print(f"渠道当月结算金额（美元）: {channel_settlement['usd_amount']:.2f} USD")
            
            return results
            
        except Exception as e:
            print(f"查询T_FUND_CENTER_ORDER表数据时发生错误: {str(e)}")
            raise

def query_channel_ccy_amount(params=None, env='FAT'):
    """
    查询渠道小币种结算金额
    :param params: 参数字典，包含startRunDate、endRunDate、ccy等
    :param env: 环境名称，默认'FAT'
    :return: 查询结果字典
    """
    # 默认参数示例
    default_params = {
        'startRunDate': '2025-09-01',
        'endRunDate': '2025-09-30',
        'ccy': ['DKK']
    }
    
    # 如果没有提供参数，使用默认参数
    if params is None:
        params = default_params
    
    print(f"使用参数: {json.dumps(params, ensure_ascii=False)}")
    
    # 创建查询实例并执行
    query = CurrencyAmountQuery(env=env)  # 使用传入的环境参数
    result = query.run(params)
    
    # 可以根据需要将结果保存到文件
    # with open('result.json', 'w', encoding='utf-8') as f:
    #     json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("\n查询完成！")
    return result

# 保留命令行执行功能，方便测试
if __name__ == '__main__':
    # 固定参数设置
    start_date = '2026-01-01'
    end_date = '2026-01-06'
    
    # 只查询T_FUND_CENTER_ORDER表的数据
    print("===== 查询T_FUND_CENTER_ORDER表STATUS=5的数据 =====")
    
    # 创建查询实例
    query = CurrencyAmountQuery(env='FAT')
    
    # 执行查询，不指定币种查询所有币种
    center_data = query.query_fund_center_status5(start_date, end_date)
    
    print(f"\nT_FUND_CENTER_ORDER STATUS=5数据查询完成，共获取 {len(center_data)} 条记录")
    
    # 确保关闭数据库连接
    query.close_db()