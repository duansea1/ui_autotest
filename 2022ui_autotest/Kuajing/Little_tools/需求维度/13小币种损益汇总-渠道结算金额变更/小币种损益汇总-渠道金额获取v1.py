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
        查询资金调拨交易订单表(T_FUND_TRANSFER_ORDER)数据
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
        
        for ccy in currencies:
            ccy = ccy.strip()  # 去除空格
            result[ccy] = {
                'count': 0,
                'local_amount': 0.0,  # 小币种金额
                'usd_amount': 0.0    # 美元金额
            }
            
            try:
                # 查询符合条件的记录
                sql = """SELECT COUNT(*) as count, SUM(SOURCE_AMT) as local_sum, SUM(DEST_AMT) as usd_sum 
                         FROM T_FUND_TRANSFER_ORDER 
                         WHERE CREATE_AT >= %s AND CREATE_AT <= %s 
                         AND TRANSFER_STATE IN (3)  -- 已汇出或已到账（相当于结算成功）
                         AND SOURCE_CCY = %s  -- 汇出币种为小币种
                         AND DEST_CCY = 'USD'  -- 目标币种为美元
                      """
                
                self.cursor.execute(sql, (start_of_month, end_of_month, ccy))
                row = self.cursor.fetchone()
                
                if row:
                    result[ccy]['count'] = row['count'] or 0
                    # 将decimal.Decimal类型转换为float类型
                    result[ccy]['local_amount'] = float(row['local_sum'] or 0.0)
                    result[ccy]['usd_amount'] = float(row['usd_sum'] or 0.0)
                    
                # 打印日志
                print(f"T_FUND_TRANSFER_ORDER表  {ccy} 符合条件的明细{result[ccy]['count']}条")
                print(f"T_FUND_TRANSFER_ORDER表  渠道当月结算金额（小币种-{ccy}）：{result[ccy]['local_amount']}   渠道当月结算金额（美元）：{result[ccy]['usd_amount']}")
                
            except Exception as e:
                print(f"查询T_FUND_TRANSFER_ORDER表{ccy}数据时发生错误: {str(e)}")
        
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
                ft.CCY as CCY,
                ft.AMOUNT as TRANSFER_AMT,
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
                sql += " AND ft.CCY = %s AND fc.SOURCE_CCY = %s"
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
            
            # 按币种分组统计并转换结果格式
            currency_stats = {}
            total_records = 0
            total_source_amount = 0.0
            total_dest_amount = 0.0
            
            # 转换结果为包含ORDER_NO的字典列表
            results = []
            for row in raw_results:
                ccy = row['SOURCE_CCY']
                source_amt = float(row['SOURCE_AMT'] or 0.0)
                dest_amt = float(row['DEST_AMT'] or 0.0)
                
                # 将ID重命名为ORDER_NO
                record = {
                    'ORDER_NO': row['ID'],
                    'ID': row['ID'],
                    'SOURCE_CCY': row['SOURCE_CCY'],
                    'SOURCE_AMT': row['SOURCE_AMT'],
                    'DEST_AMT': row['DEST_AMT'],
                    'CREATE_AT': row['CREATE_AT']
                }
                results.append(record)
                
                if ccy not in currency_stats:
                    currency_stats[ccy] = {
                        'count': 0,
                        'total_source_amt': 0.0,
                        'total_dest_amt': 0.0
                    }
                
                currency_stats[ccy]['count'] += 1
                currency_stats[ccy]['total_source_amt'] += source_amt
                currency_stats[ccy]['total_dest_amt'] += dest_amt
                
                total_records += 1
                total_source_amount += source_amt
                total_dest_amount += dest_amt
            
            # 打印统计信息
            print(f"\n查询结果统计：")
            print(f"总记录数: {total_records}")
            print(f"总金额 (小币种): {total_source_amount}")
            print(f"总金额 (美元): {total_dest_amount}")
            
            print(f"\n各币种统计：")
            for ccy, stats in currency_stats.items():
                print(f"币种 {ccy}: 记录数={stats['count']}, 总金额={stats['total_source_amt']} {ccy}, 美元金额={stats['total_dest_amt']} USD")
            
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
    # 默认参数
    default_params = {
        'startRunDate': '2025-09-01',
        'endRunDate': '2025-09-30',
        'ccy': ['DKK']
    }
    
    params = default_params
    
    # 如果有命令行参数，则解析JSON格式的参数
    if len(sys.argv) > 1:
        try:
            params = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("命令行参数不是有效的JSON格式，使用默认参数")
    
    # 查询指定币种和期限内的汇总金额
    query_channel_ccy_amount(params)
    
    # 测试新增的数据一致性比对功能
    print("\n\n===== 测试T_FUND_TRANSFER_ORDER和T_FUND_CENTER_ORDER数据一致性比对功能 =====")
    try:
        # 创建查询实例
        query = CurrencyAmountQuery(env='FAT')
        
        # 定义日期范围
        start_date = '2025-09-01'
        end_date = '2025-09-30'
        
        # 执行数据一致性比对，不指定币种查询所有币种
        # 使用正确的参数名currency而非ccy
        inconsistent_data = query.compare_fund_transfer_center(start_date, end_date)
        
        print(f"\n数据一致性比对完成，共发现 {len(inconsistent_data)} 条不一致记录")
        
        # 打印不一致记录详情（如果有）
        if inconsistent_data:
            print("\n不一致记录详情（前5条）:")
            for i, record in enumerate(inconsistent_data[:5]):
                print(f"\n记录 {i+1}:")
                print(f"  转账订单ID: {record.get('TRANSFER_ORDER_ID', 'N/A')}")
                print(f"  中心订单ID: {record.get('CENTER_ORDER_ID', 'N/A')}")
                print(f"  币种: {record.get('CCY', 'N/A')}")
                print(f"  转账金额: {record.get('TRANSFER_AMT', 'N/A')} {record.get('CCY', '')}")
                print(f"  中心金额: {record.get('CENTER_AMT', 'N/A')} {record.get('CCY', '')}")
    
    except Exception as e:
        print(f"测试数据一致性比对功能时发生错误: {str(e)}")
    finally:
        # 确保关闭数据库连接
        if 'query' in locals():
            query.close_db()
    
    # 测试新增的T_FUND_CENTER_ORDER STATUS=5数据查询功能
    print("\n\n===== 测试T_FUND_CENTER_ORDER STATUS=5数据查询功能 =====")
    try:
        # 创建新的查询实例
        query = CurrencyAmountQuery(env='FAT')
        
        # 使用与上面相同的日期范围
        start_date = '2025-09-01'
        end_date = '2025-09-30'
        
        # 执行查询，不指定币种查询所有币种
        # 使用正确的参数名currency而非ccy
        center_data = query.query_fund_center_status5(start_date, end_date)
        
        print(f"\nT_FUND_CENTER_ORDER STATUS=5数据查询完成，共获取 {len(center_data)} 条记录")
        
        # 打印前5条记录作为示例
        if center_data:
            print("\n前5条记录示例:")
            for i, record in enumerate(center_data[:5]):
                print(f"\n记录 {i+1}:")
                # 使用get方法避免KeyError
                print(f"  订单ID: {record.get('ORDER_NO', record.get('ID', 'N/A'))}")
                print(f"  币种: {record.get('SOURCE_CCY', 'N/A')}")
                print(f"  金额: {record.get('SOURCE_AMT', 'N/A')} {record.get('SOURCE_CCY', '')}")
                print(f"  美元金额: {record.get('DEST_AMT', 'N/A')} USD")
                print(f"  创建时间: {record.get('CREATE_AT', 'N/A')}")
    
    except Exception as e:
        print(f"测试T_FUND_CENTER_ORDER STATUS=5数据查询功能时发生错误: {str(e)}")
    finally:
        # 确保关闭数据库连接
        if 'query' in locals():
            query.close_db()