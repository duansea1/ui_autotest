import pymysql
import logging
import traceback

from Kuajing.Common.kjMysql import get_db_config

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def update_batch_order_status(batch_no: str, status: str, env: str = 'FAT') -> bool:
    """
    根据批次号更新批次单状态
    
    Args:
        batch_no: 批次号
        status: 状态值 (INIT待下单、PARTIAL部分已下单、PROCESS处理中、COMPLETED已完成、CANCEL已取消、NOT_PROCESS无需处理)
        env: 环境，默认为'FAT'
    
    Returns:
        bool: 更新成功返回True，失败返回False
    """
    # 验证状态值是否合法
    valid_statuses = ['INIT', 'PARTIAL', 'PROCESS', 'COMPLETED', 'CANCEL', 'NOT_PROCESS']
    if status not in valid_statuses:
        logger.error(f"无效的状态值: {status}，有效状态包括: {valid_statuses}")
        return False
    
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
            
            # 查询当前状态
            select_sql = "SELECT BATCH_NO, STATUS FROM BAOFU_TRADE.T_EXCHANGE_BATCH_ORDER WHERE BATCH_NO = %s"
            cursor.execute(select_sql, (batch_no,))
            result = cursor.fetchone()
            
            if not result:
                logger.warning(f"未找到批次号 {batch_no} 的记录")
                return False
            
            current_status = result['STATUS']
            logger.info(f"批次 {batch_no} 当前状态: {current_status}")
            
            # 更新状态
            update_sql = "UPDATE BAOFU_TRADE.T_EXCHANGE_BATCH_ORDER SET STATUS = %s WHERE BATCH_NO = %s"
            cursor.execute(update_sql, (status, batch_no))
            connection.commit()
            
            logger.info(f"批次 {batch_no} 状态更新成功，从 {current_status} --> {status}")
            return True
                
    except Exception as e:
        logger.error(f"更新批次单状态时出错: {str(e)}")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()
            logger.info("数据库连接已关闭")

# ===== 测试用例 =====
if __name__ == "__main__":
    # 示例调用方法
    # 状态值必须是以下之一: INIT待下单、PARTIAL部分已下单、PROCESS处理中、COMPLETED已完成、CANCEL--已取消、NOT_PROCESS无需处理
    batch_no = "2510211119000573280"  # 批次号
    # new_status = "INIT"  # 待下单
    new_status = "CANCEL"  # 已取消
    env = "FAT"  # 环境
    
    # 调用方法
    success = update_batch_order_status(batch_no, new_status, env)
    
    if success:
        print(f"批次 {batch_no} 状态已成功更新为 {new_status}")
    else:
        print(f"批次 {batch_no} 状态更新失败")