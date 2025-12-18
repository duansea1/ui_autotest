import pymysql
import logging
import traceback
from tabulate import tabulate

from Kuajing.Common.kjMysql import get_db_config

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def query_batch_order_fields(batch_no: str, env: str = 'FAT') -> dict:
    """
    查询批次单指定字段信息
    
    Args:
        batch_no: 批次号
        env: 环境，默认为'FAT'
    
    Returns:
        dict: 包含指定字段的字典，如果查询失败返回空字典
    """
    # 获取数据库配置
    db_config = get_db_config(env).copy()
    logger.info(f"数据库配置: host={db_config.get('host')}, user={db_config.get('user')}, database={db_config.get('database')}")
    
    # 移除db_config中可能已存在的cursorclass参数，避免重复指定
    if 'cursorclass' in db_config:
        del db_config['cursorclass']
    
    connection = None
    try:
        # 建立数据库连接并设置为字典游标
        connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        
        with connection.cursor() as cursor:
            # 手动切换到BAOFU_TRADE数据库
            cursor.execute("USE BAOFU_TRADE")
            
            # 查询指定字段
            select_sql = """
            SELECT 
                CLOSING_DATE,      -- 交割日 yyyy-MM-dd
                SYS_SELL_CCY,       -- GEP卖出币种
                SYS_SELL_AMT,       -- GEP卖出金额
                SYS_BUY_CCY,        -- GEP买入币种
                SYS_BUY_AMT,        -- GEP买入金额
                CHANNEL_RATE,       -- 渠道成交汇率
                TRADE_CCY,          -- 交易币种
                AMT_DIRECTION,      -- 金额方向，1：买入，2：卖出
                PENDING_AMT,        -- 待交易金额
                PROCESS_AMT,        -- 处理中金额
                USING_AMT,          -- 已下单金额
                STANDING_AMT        -- 挂单金额
            FROM 
                BAOFU_TRADE.T_EXCHANGE_BATCH_ORDER 
            WHERE 
                BATCH_NO = %s
            """
            
            cursor.execute(select_sql, (batch_no,))
            result = cursor.fetchone()
            
            if not result:
                logger.warning(f"未找到批次号 {batch_no} 的记录")
                print(f"\n查询失败或未找到批次号 {batch_no} 的记录")
                return {}
            
            # 打印查询结果（表格形式）
            print("\n" + "="*60)
            print("批次单字段信息详情")
            print("="*60)
            
            # 金额方向转换
            amt_direction = result.get('AMT_DIRECTION')
            amt_direction_text = '买入' if amt_direction == 1 else '卖出' if amt_direction == 2 else 'N/A'
            
            # 构建表格数据
            table_data = [
                ["批次号", batch_no],
                ["交割日", result.get('CLOSING_DATE', 'N/A')],
                ["GEP卖出币种", result.get('SYS_SELL_CCY', 'N/A')],
                ["GEP卖出金额", result.get('SYS_SELL_AMT', 'N/A')],
                ["GEP买入币种", result.get('SYS_BUY_CCY', 'N/A')],
                ["GEP买入金额", result.get('SYS_BUY_AMT', 'N/A')],
                ["渠道成交汇率", result.get('CHANNEL_RATE', 'N/A')],
                ["交易币种", result.get('TRADE_CCY', 'N/A')],
                ["金额方向", f"{amt_direction_text} ({amt_direction})"] if amt_direction else ["金额方向", "N/A"],
                ["待交易金额", result.get('PENDING_AMT', 'N/A')],
                ["处理中金额", result.get('PROCESS_AMT', 'N/A')],
                ["已下单金额", result.get('USING_AMT', 'N/A')],
                ["挂单金额", result.get('STANDING_AMT', 'N/A')]
            ]
            
            # 使用tabulate打印表格
            print("\n" + tabulate(table_data, headers=["项目", "值"], tablefmt="grid"))
            print("="*60)
            
            # 在函数内部打印查询成功信息
            print(f"\n查询成功，返回了 {len(result)} 个字段")
            return result
                
    except Exception as e:
        logger.error(f"查询批次单字段时出错: {str(e)}")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        return {}
    finally:
        if connection:
            connection.close()
            logger.info("数据库连接已关闭")

def query_standing_orders(batch_no: str = None, standing_no: str = None, env: str = 'FAT') -> list:
    """
    查询批次关联的挂单数据或指定挂单数据
    
    Args:
        batch_no: 批次号，可选
        standing_no: 挂单单号，可选
        env: 环境，默认为'FAT'
    
    Returns:
        list: 包含挂单信息的列表
    """
    if not batch_no and not standing_no:
        logger.error("批次号和挂单单号至少需要提供一个")
        print("批次号和挂单单号至少需要提供一个")
        return []
    
    # 获取数据库配置
    db_config = get_db_config(env).copy()
    logger.info(f"数据库配置: host={db_config.get('host')}, user={db_config.get('user')}, database={db_config.get('database')}")
    
    # 移除db_config中可能已存在的cursorclass参数
    if 'cursorclass' in db_config:
        del db_config['cursorclass']
    
    connection = None
    try:
        # 建立数据库连接并设置为字典游标
        connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        
        with connection.cursor() as cursor:
            # 手动切换到BAOFU_TRADE数据库
            cursor.execute("USE BAOFU_TRADE")
            
            # 根据参数构建查询条件
            where_conditions = []
            params = []
            
            if batch_no:
                where_conditions.append("BATCH_NO = %s")
                params.append(batch_no)
            if standing_no:
                where_conditions.append("STANDING_NO = %s")
                params.append(standing_no)
            
            where_clause = " AND ".join(where_conditions)
            
            # 查询挂单数据
            select_sql = f"""
            SELECT 
                ID, STANDING_NO, BATCH_NO, CHANNEL_ORDER_NO, CCY_PAIR, 
                ORDER_TYPE, TRADE_DIRECTION, AMT_DIRECTION, SELL_CCY, BUY_CCY, 
                SELL_AMT, BUY_AMT, STANDING_RATE, DEAL_RATE, CHANNEL_CODE, 
                C_SELL_AMT, C_BUY_AMT, CLOSING_TYPE, CLOSING_DATE, VALID_DATE, 
                STATUS, REASON, COMPLETE_DATE
            FROM 
                BAOFU_TRADE.T_CHANNEL_STANDING_ORDER 
            WHERE 
                {where_clause}
            """
            
            cursor.execute(select_sql, params)
            results = cursor.fetchall()
            
            if not results:
                logger.warning(f"未找到符合条件的挂单记录")
                print(f"\n未找到符合条件的挂单记录")
                return []
            
            # 打印查询结果（表格形式）
            print("\n" + "="*80)
            print(f"挂单数据（共{len(results)}条）")
            print("="*80)
            
            # 状态映射字典
            status_map = {
                'VALID': '有效',
                'DEALED': '已成交',
                'CANCELED': '已取消',
                'EXPIRED': '已过期'
            }
            
            # 如果有多个记录，逐个打印
            for i, row in enumerate(results, 1):
                if len(results) > 1:
                    print(f"\n记录 {i}:")
                    print("-"*60)
                
                # 构建表格数据
                table_data = [
                    ["ID-记录ID", str(row.get('ID', 'N/A'))],
                    ["STANDING_NO-挂单单号", str(row.get('STANDING_NO', 'N/A'))],
                    ["BATCH_NO-批次号", str(row.get('BATCH_NO', 'N/A'))],
                    ["CHANNEL_ORDER_NO-渠道订单号", str(row.get('CHANNEL_ORDER_NO', 'N/A'))],
                    ["CCY_PAIR-货币对", str(row.get('CCY_PAIR', 'N/A'))],
                    ["ORDER_TYPE-订单类型", str(row.get('ORDER_TYPE', 'N/A'))],
                    ["TRADE_DIRECTION-交易方向", str(row.get('TRADE_DIRECTION', 'N/A'))],
                    ["AMT_DIRECTION-固定金额方向", str(row.get('AMT_DIRECTION', 'N/A'))],
                    ["SELL_CCY-卖出币种", str(row.get('SELL_CCY', 'N/A'))],
                    ["BUY_CCY-买入币种", str(row.get('BUY_CCY', 'N/A'))],
                    ["SELL_AMT-卖出金额", str(row.get('SELL_AMT', 'N/A'))],
                    ["BUY_AMT-买入金额", str(row.get('BUY_AMT', 'N/A'))],
                    ["STANDING_RATE-挂单汇率", str(row.get('STANDING_RATE', 'N/A'))],
                    ["DEAL_RATE-成交汇率", str(row.get('DEAL_RATE', 'N/A'))],
                    ["CHANNEL_CODE-成交渠道编码", str(row.get('CHANNEL_CODE', 'N/A'))],
                    ["C_SELL_AMT-成交卖出金额", str(row.get('C_SELL_AMT', 'N/A'))],
                    ["C_BUY_AMT-成交买入金额", str(row.get('C_BUY_AMT', 'N/A'))],
                    ["CLOSING_TYPE-期限", str(row.get('CLOSING_TYPE', 'N/A'))],
                    ["CLOSING_DATE-交割日期", str(row.get('CLOSING_DATE', 'N/A'))],
                    ["VALID_DATE-有效期", str(row.get('VALID_DATE', 'N/A'))],
                    ["STATUS-状态", status_map.get(str(row.get('STATUS', 'N/A')), str(row.get('STATUS', 'N/A')))],
                    ["REASON-原因", str(row.get('REASON', 'N/A'))],
                    ["COMPLETE_DATE-成交时间", str(row.get('COMPLETE_DATE', 'N/A'))]
                ]
                
                # 使用tabulate打印表格
                print("\n" + tabulate(table_data, headers=["项目", "值"], tablefmt="grid"))
            
            print("="*80)
            
            return results
                
    except Exception as e:
        logger.error(f"查询挂单数据时出错: {str(e)}")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        return []
    finally:
        if connection:
            connection.close()
            logger.info("数据库连接已关闭")


def query_standing_order_monitor(standing_no_list: list = None, status_filter: str = 'VALID', env: str = 'FAT') -> None:
    """
    查询指定状态的挂单监控策略
    
    Args:
        standing_no_list: 挂单单号列表，如果为None则不根据挂单号过滤
        status_filter: 状态过滤条件，默认为'VALID'
        env: 环境，默认为'FAT'
    """
    if not standing_no_list:
        logger.warning("挂单单号列表为空，不执行查询")
        return
    
    logger.info(f"开始查询状态为{status_filter}的挂单监控策略，共{len(standing_no_list)}个挂单号")
    
    for i, standing_no in enumerate(standing_no_list, 1):
        logger.info(f"正在查询第{i}/{len(standing_no_list)}个挂单 {standing_no} 的监控策略")
        print(f"\n[{i}/{len(standing_no_list)}] 查询挂单 {standing_no} 的监控策略:")
        query_standing_monitor(standing_no=standing_no, env=env)
    
    logger.info("所有挂单监控策略查询完成")

def update_standing_monitor(standing_no: str, monitor_type: str = None, start_time: str = None, end_time: str = None, env: str = 'FAT') -> bool:
    """
    更新挂单监控策略的指定字段
    
    Args:
        standing_no: 挂单单号
        monitor_type: 监控类型，如果为None则不更新
        start_time: 开始时间，如果为None则不更新
        end_time: 结束时间，如果为None则不更新
        env: 环境，默认为'FAT'
    
    Returns:
        bool: 更新成功返回True，否则返回False
    """
    if not standing_no:
        logger.error("挂单单号不能为空")
        print("挂单单号不能为空")
        return False
    
    # 检查是否有需要更新的字段
    update_fields = []
    update_params = []
    
    if monitor_type is not None:
        update_fields.append("MONITOR_TYPE = %s")
        update_params.append(monitor_type)
    if start_time is not None:
        update_fields.append("START_TIME = %s")
        update_params.append(start_time)
    if end_time is not None:
        update_fields.append("END_TIME = %s")
        update_params.append(end_time)
    
    if not update_fields:
        logger.warning(f"没有需要更新的字段，挂单单号: {standing_no}")
        print("没有需要更新的字段，请至少提供一个非None的参数")
        return True  # 没有更新但不报错，视为成功
    
    # 构建更新SQL
    update_sql = f"""
    UPDATE BAOFU_TRADE.T_CHANNEL_STANDING_MONITOR
    SET {', '.join(update_fields)}
    WHERE STANDING_NO = %s
    """
    
    update_params.append(standing_no)
    
    # 获取数据库配置
    db_config = get_db_config(env).copy()
    logger.info(f"数据库配置: host={db_config.get('host')}, user={db_config.get('user')}, database={db_config.get('database')}")
    
    # 移除db_config中可能已存在的cursorclass参数
    if 'cursorclass' in db_config:
        del db_config['cursorclass']
    
    connection = None
    try:
        # 建立数据库连接
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # 手动切换到BAOFU_TRADE数据库
            cursor.execute("USE BAOFU_TRADE")
            
            logger.info(f"执行更新SQL: {update_sql}")
            logger.info(f"更新参数: {update_params}")
            
            # 执行更新
            affected_rows = cursor.execute(update_sql, update_params)
            
            if affected_rows > 0:
                connection.commit()
                logger.info(f"成功更新挂单单号 {standing_no} 的监控策略，影响行数: {affected_rows}")
                print(f"\n更新成功！挂单单号 {standing_no} 的监控策略已更新，影响行数: {affected_rows}")
                
                # 打印更新的字段信息
                updated_fields_info = []
                if monitor_type is not None:
                    updated_fields_info.append(f"MONITOR_TYPE = {monitor_type}")
                if start_time is not None:
                    updated_fields_info.append(f"START_TIME = {start_time}")
                if end_time is not None:
                    updated_fields_info.append(f"END_TIME = {end_time}")
                
                print(f"更新的字段: {', '.join(updated_fields_info)}")
                return True
            else:
                logger.warning(f"未找到挂单单号 {standing_no} 对应的监控策略记录，无法更新")
                print(f"\n更新失败！未找到挂单单号 {standing_no} 对应的监控策略记录")
                return False
                
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"更新挂单监控策略时出错: {str(e)}")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        print(f"\n更新出错: {str(e)}")
        return False
    finally:
        if connection:
            connection.close()
            logger.info("数据库连接已关闭")

def query_standing_monitor(standing_no: str, env: str = 'FAT') -> list:
    """
    查询挂单对应的监控策略
    
    Args:
        standing_no: 挂单单号
        env: 环境，默认为'FAT'
    
    Returns:
        list: 包含监控策略信息的列表
    """
    if not standing_no:
        logger.error("挂单单号不能为空")
        print("挂单单号不能为空")
        return []
    
    # 获取数据库配置
    db_config = get_db_config(env).copy()
    logger.info(f"数据库配置: host={db_config.get('host')}, user={db_config.get('user')}, database={db_config.get('database')}")
    
    # 移除db_config中可能已存在的cursorclass参数
    if 'cursorclass' in db_config:
        del db_config['cursorclass']
    
    connection = None
    try:
        # 建立数据库连接并设置为字典游标
        connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        
        with connection.cursor() as cursor:
            # 手动切换到BAOFU_TRADE数据库
            cursor.execute("USE BAOFU_TRADE")
            
            # 查询监控策略
            select_sql = """
            SELECT 
                STANDING_NO, CHANNEL_CODE, MONITOR_TYPE, START_TIME, 
                END_TIME, CLOSING_TYPE, CLOSING_DATE
            FROM 
                BAOFU_TRADE.T_CHANNEL_STANDING_MONITOR 
            WHERE 
                STANDING_NO = %s
            """
            
            cursor.execute(select_sql, (standing_no,))
            results = cursor.fetchall()
            
            if not results:
                logger.warning(f"未找到挂单单号 {standing_no} 对应的监控策略")
                print(f"\n未找到挂单单号 {standing_no} 对应的监控策略")
                return []
            
            # 打印查询结果（表格形式）
            print("\n" + "="*80)
            print(f"挂单监控策略（共{len(results)}条）")
            print("="*80)
            
            # 构建表格数据
            table_data = []
            for row in results:
                table_data.append([
                    str(row.get('STANDING_NO', 'N/A')),
                    str(row.get('CHANNEL_CODE', 'N/A')),
                    str(row.get('MONITOR_TYPE', 'N/A')),
                    str(row.get('START_TIME', 'N/A')),
                    str(row.get('END_TIME', 'N/A')),
                    str(row.get('CLOSING_TYPE', 'N/A')),
                    str(row.get('CLOSING_DATE', 'N/A'))
                ])
            
            # 使用tabulate打印表格
            headers = ["STANDING_NO", "CHANNEL_CODE", "MONITOR_TYPE", "START_TIME", "END_TIME", "CLOSING_TYPE", "CLOSING_DATE"]
            print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
            print("="*80)
            
            return results
                
    except Exception as e:
        logger.error(f"查询挂单监控策略时出错: {str(e)}")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        return []
    finally:
        if connection:
            connection.close()
            logger.info("数据库连接已关闭")


# ===== 测试用例 =====
if __name__ == "__main__":
    try:
        # 示例调用方法
        batch_no = "2511201715000667113"  # 批次号
        env = "FAT"  # 环境
        
        # 功能：查询客单批次单的字段
        query_batch_order_fields(batch_no, env)
        
        # 功能：查询挂单数据，可以查询单条挂单或批次单对应的挂单数据
        print("\n" + "="*80)
        print("查询批次关联的挂单数据:")
        # standing_orders = query_standing_orders(batch_no=batch_no,env=env)
        standing_orders = query_standing_orders( standing_no="2511241041000000024",env=env)
        
        # 功能：获取状态为VALID(生效中)的挂单单号列表并查询监控策略
        valid_standing_nos = [order.get('STANDING_NO') for order in standing_orders if order.get('STATUS') == 'VALID']
        if valid_standing_nos:
            query_standing_order_monitor(standing_no_list=valid_standing_nos, status_filter='VALID', env=env)
        
        # 演示更新监控策略功能（仅作示例，实际使用时请取消注释并提供有效的参数）
        # 示例1：更新MONITOR_TYPE
        # update_standing_monitor(standing_no="2511241114000000025", monitor_type="HOLIDAY", env="FAT")
        
        # 示例2：更新START_TIME和END_TIME
        update_standing_monitor(
            standing_no="2511241041000000024", 
            start_time="10:00:00", 
            end_time="23:59:59", 
            env="FAT"
        )
        
        # 示例3：更新所有字段
        # update_standing_monitor(
        #     standing_no="2511241114000000025", 
        #     monitor_type="HOLIDAY",
        #     start_time="2024-06-01 10:00:00", 
        #     end_time="2024-06-30 23:59:59", 
        #     env="FAT"
        # )
        
        print("\n" + "="*80)
        print("所有查询完成")
    except Exception as e:
        logger.error(f"执行过程中出错: {str(e)}")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        print(f"\n执行出错: {str(e)}")
    finally:
        logger.info("程序执行完毕")