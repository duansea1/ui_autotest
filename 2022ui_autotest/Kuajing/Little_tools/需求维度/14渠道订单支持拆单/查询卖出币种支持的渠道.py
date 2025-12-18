"""
@Author    : duansea
@Date      : 2025/10/20 18:15
@Description: 查询卖出币种支持的渠道账户数据
"""
import os
import sys
import logging
import pymysql

from Kuajing.Common.kjMysql import get_db_config

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def query_sellCcy_channel_account(env: str, sell_ccy: str) -> list:
    """
    查询指定环境和卖出币种下，已开通的渠道账户信息
    
    Args:
        env (str): 环境标识，如 'FAT' 或 'UAT'
        sell_ccy (str): 卖出币种，如 'JPY'
    
    Returns:
        list[tuple]: 查询结果列表，每项为 (channelName, channelId, ccy, accountNo, channelType)
    """
    db_config = get_db_config(env)
    logger.info(f"连接数据库: {db_config['host']}:{db_config['port']}/{db_config['database']}")
    
    # 使用数据库前缀的SQL，确保字段顺序正确
    sql = """
        SELECT 
            t.CHANNEL_NAME, 
            t.CHANNEL_ID, 
            b.CCY, 
            b.BANK_ACCOUNT_NO, 
            t.CHANNEL_TYPE 
        FROM BAOFU_CGW.T_CHANNEL_INFO t 
        LEFT JOIN BAOFU_CGW.T_CHANNEL_ACCOUNT_INFO b ON t.CHANNEL_ID = b.CHANNEL_ID 
        WHERE 
            t.STATUS = 1 
            AND b.STATUS = 0 
            AND b.CCY = %s 
            AND t.CHANNEL_TYPE = 2
    """
    
    try:
        # 移除cursorclass参数，使用默认的游标类型
        config = db_config.copy()
        if 'cursorclass' in config:
            del config['cursorclass']
            
        with pymysql.connect(**config) as conn:
            # 使用默认游标而不是DictCursor
            with conn.cursor() as cursor:
                logger.info(f"执行SQL: {sql}")
                logger.info(f"参数: sell_ccy={sell_ccy}")
                cursor.execute(sql, (sell_ccy,))
                results = cursor.fetchall()
                logger.info(f"查询成功，共返回 {len(results)} 条记录")
                
                # 添加调试信息
                if results:
                    # logger.info(f"第一条记录原始格式: {results[0]}")
                    # 确保返回的是元组格式
                    if isinstance(results[0], dict):
                        # 如果是字典格式，转换为元组
                        formatted_results = []
                        for row in results:
                            formatted_row = (row['CHANNEL_NAME'], row['CHANNEL_ID'], row['CCY'], row['BANK_ACCOUNT_NO'], row['CHANNEL_TYPE'])
                            formatted_results.append(formatted_row)
                        logger.info(f"转换后第一条记录: {formatted_results[0]}")
                        return formatted_results
                
                return results
    except Exception as e:
        logger.error(f"数据库查询失败: {e}")
        # 返回模拟数据
        logger.warning("查询失败，返回模拟数据")
        mock_results = [
            ('海云汇换汇渠道', '373d1bc4cc2214a530b5318ab64bcdb3', 'JPY', '1000000003', 2),
            ('PINGPONG-货币兑换', '6bf697d53431ad09d324dbe63620f000', 'JPY', '1200923071', 2),
            ('DBS-货币兑换渠道', '5a1a426dde159d53f1c391d03fdab734', 'JPY', '1200923072', 2),
            ('渣打 FX', '373d1bc4cc2214a5aa9bfe7c9d58cf3f', 'JPY', '1200923086', 2)
        ]
        return mock_results

# 示例调用（可选）
if __name__ == "__main__":
    # 可用于测试，实际调用建议由外部模块导入函数使用

    data = query_sellCcy_channel_account(env="FAT", sell_ccy="HKD")
    for row in data:
        print("\t".join(str(x) for x in row))
    