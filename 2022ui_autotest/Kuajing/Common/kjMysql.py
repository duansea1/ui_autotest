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
        }
    }
    return configs.get(env, configs['FAT'])



def get_db_config_topic(env: str) -> dict:
    """跨境支付系统数据库配置--数仓"""
    configs = {
        'FAT': {
            'host': '10.0.19.156',
            'port': 9030,
            'user': 'bf_hpt',
            'password': 'bf_hpt',
            'database': 'BAOFU_CGW',  # 注意你提供的SQL中是 BAOFU_CBA 而不是 BAOFU_CBCA
            'charset': 'utf8mb4',
            # 'cursorclass': DictCursor
        }
    }
    return configs.get(env, configs['FAT'])