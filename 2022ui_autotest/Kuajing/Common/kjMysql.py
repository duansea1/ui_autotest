"""
@Author    : duansea
@Date      : 2025/7/18 15:42
@Description: [跨境支付系统数据库配置]
"""
import pymysql
from pymysql.cursors import DictCursor

def get_db_config(env: str) -> dict:
    """跨境支付系统数据库配置"""
    configs = {
        'FAT': {
            'host': '10.0.19.206',
            'port': 3306,
            'user': 'GEPHOLDING',
            'password': 'GEPHOLDING',
            'database': 'BAOFU_CBA',  # 注意你提供的SQL中是 BAOFU_CBA 而不是 BAOFU_CBCA
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        },
        'UAT': {
            'host': '10.0.23.200',
            'port': 3306,
            'user': 'BAOFOO_CBPAY',
            'password': 'BAOFOO_CBPAY',
            'database': 'BAOFU_CBA',
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        },

        'FAT_DATA': {
            'host': '10.0.19.156',    # 数仓库
            'port': 9030,
            'user': 'bf_hpt',
            'password': 'bf_hpt',
            'database': 'BAOFU_CGW',  # 
            'charset': 'utf8mb4',
            # 'cursorclass': DictCursor
    }}
    return configs.get(env, configs['FAT'])



def get_db_config_topic(env: str) -> dict:
    """"""
    configs = {
        'FAT': {
            'host': '10.0.19.156',
            'port': 9030,
            'user': 'bf_hpt',
            'password': 'bf_hpt',
            'database': 'BAOFU_CGW',  # 
            'charset': 'utf8mb4',
            # 'cursorclass': DictCursor
        }
        ,
        'UAT': {
            'host': '10.0.19.156',
            'port': 9030,
            'user': 'bf_hpt',
            'password': 'bf_hpt',
            'database': 'BAOFU_CGW',  # 
            'charset': 'utf8mb4',
            # 'cursorclass': DictCursor
        }
    }
    return configs.get(env, configs['FAT'])


def execute_db_topic(env, sql, database=None, params=None):
    """数仓数据库操作方法（使用 get_db_config_topic，StarRocks/Doris）
    Args:
        env: 环境名称（FAT/UAT）
        sql: SQL语句（必填）
        database: 数据库名称（可选，默认使用配置中的database）
        params: SQL参数（可选）
    Returns:
        查询结果或影响行数
    """
    conn = None
    cursor = None
    try:
        db_config = get_db_config_topic(env)
        if database:
            db_config['database'] = database

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        if sql.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"数仓数据库操作失败：{str(e)}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute_db(env, sql, database=None, params=None):
    """通用数据库操作方法
    Args:
        env: 环境名称（FAT/UAT）
        sql: SQL语句（必填）
        database: 数据库名称（可选，默认使用配置中的database）
        params: SQL参数（可选）
    Returns:
        查询结果或影响行数
    """
        
    conn = None
    cursor = None
    try:
        # 获取数据库配置
        db_config = get_db_config(env)
        # 如果传入了database参数，覆盖配置中的database
        if database:
            db_config['database'] = database
        
        # 建立数据库连接
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # 执行SQL
        if params:
            affected_rows = cursor.execute(sql, params)
        else:
            affected_rows = cursor.execute(sql)
        
        # 处理查询结果
        if sql.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
            return result
        else:
            # 提交事务
            conn.commit()
            return affected_rows
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"数据库操作失败：{str(e)}")
        raise
    finally:
        # 关闭数据库连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()
