
"""
【修改交割日期】
修改FORWARD订单日期，可以修改到当前日期之前的日期。

# 汇兑订单表
1、SELECT * FROM `BAOFU_CBCA`.`T_USER_EXCHANGE_ORDER` WHERE `EXCHANGE_ID` = '2503171533006118013'
`BAOFU_CBCA`.`T_USER_EXCHANGE_ORDER`:
数据库字段：
--CLOSING_DATE` 交割日期，格式YYYY-MM-DD',
 --`CLOSING_STATUS`  '交割状态：0-待交割，1-交割处理中，2-交割完成，3-交割失败，4-交割超时，5-部分交割成功，6、已违约',
UPDATE `BAOFU_CBCA`.`T_USER_EXCHANGE_ORDER` SET `CLOSING_DATE` = '2025-03-17' WHERE `EXCHANGE_ID` = '2503171533006118013'


2、费率表：SELECT * FROM `BAOFU_CBCA`.`T_USER_EXCHANGE_ORDER_FEE` WHERE `EXCHANGE_ID` = '2503171533006118013'
数据库字段：
--
# 兑换凭证表
3、SELECT * FROM `BAOFU_TRADE`.`T_TRADE_RECEIPT` WHERE `REQUEST_NO` = '2503171533006118013' AND `CLOSING_TYPE` = 'FORWARD'
--CLOSING_TYPE` '交割模式',
-`TRADE_DATE` '交易日期',
  `TRADE_TIME`  '交易时间',

  ---`CLOSING_DATE`  '交割日期',
  `TRADE_STATUS`  '渠道交易状态：1-待交易、2-处理中、3-交易完成',
  `STATUS`  '关联订单交易状态，1：处理中，2：已完成',

  UPDATE `BAOFU_TRADE`.`T_TRADE_RECEIPT` SET `CLOSING_DATE` = '2025-03-17' WHERE `REQUEST_NO` = '2503171533006118013';
数据库mysql：
10.0.19.206:3306
用户名密码：GEPHOLDING  GEPHOLDING
"""
# -*- coding: utf-8 -*-
"""
远期汇兑订单交割日期修改工具
支持 FAT / UAT 环境切换
使用统一数据库配置模块
"""

import logging
from datetime import datetime
from typing import Dict, Optional, Tuple

# 使用统一数据库配置
from Kuajing.Common.kjMysql import get_db_config
import pymysql
from pymysql.cursors import DictCursor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# --------------------------
# 增强型数据访问层 (DAL)
# --------------------------
def _get_connection(env: str = 'FAT'):
    """根据环境获取数据库连接"""
    try:
        db_config = get_db_config(env)
        if not db_config:
            raise ValueError(f"无效的环境配置: {env}")

        # 确保使用 DictCursor
        if 'cursorclass' not in db_config:
            db_config['cursorclass'] = DictCursor

        conn = pymysql.connect(**db_config)
        logger.info(f"✅ 成功连接到 {env} 环境数据库: {db_config['host']}")
        return conn
    except Exception as e:
        logger.error(f"❌ 连接数据库失败: {e}")
        raise


def _query_order(conn, exchange_id: str) -> Optional[Dict]:
    """查询汇兑订单表"""
    sql = """
        SELECT 
            EXCHANGE_ID, 
            CLOSING_DATE,
            CLOSING_STATUS,
            CREATE_AT,
            UPDATE_AT 
        FROM BAOFU_CBCA.T_USER_EXCHANGE_ORDER 
        WHERE EXCHANGE_ID = %s
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (exchange_id,))
            return cursor.fetchone()
    except Exception as e:
        logger.error(f"❌ 查询订单表失败: {e}")
        raise


def _query_receipt(conn, exchange_id: str) -> Optional[Dict]:
    """查询交易凭证表"""
    sql = """
        SELECT 
            REQUEST_NO,
            RECEIPT_NO,
            CLOSING_DATE,
            TRADE_STATUS,
            TRADE_DATE,
            TRADE_TIME,
            CREATE_AT,
            UPDATE_AT 
        FROM BAOFU_TRADE.T_TRADE_RECEIPT 
        WHERE REQUEST_NO = %s 
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (exchange_id,))
            return cursor.fetchone()
    except Exception as e:
        logger.error(f"❌ 查询凭证表失败: {e}")
        raise


def _update_order_and_receipt(conn, exchange_id: str, new_date: str):
    """更新两个表的交割日期"""
    try:
        with conn.cursor() as cursor:
            # 更新订单表
            cursor.execute("""
                UPDATE BAOFU_CBCA.T_USER_EXCHANGE_ORDER 
                SET CLOSING_DATE = %s, UPDATE_AT = NOW()
                WHERE EXCHANGE_ID = %s
            """, (new_date, exchange_id))

            # 更新凭证表
            cursor.execute("""
                UPDATE BAOFU_TRADE.T_TRADE_RECEIPT 
                SET CLOSING_DATE = %s, UPDATE_AT = NOW()
                WHERE REQUEST_NO = %s 
            """, (new_date, exchange_id))

            affected_rows = conn.affected_rows()
            if affected_rows == 0:
                raise ValueError(f"⚠️ 未找到匹配的订单或凭证，可能订单号错误或非远期订单: {exchange_id}")
            logger.info(f"🔄 已更新 {affected_rows} 行数据")

    except Exception as e:
        logger.error(f"❌ 更新数据失败: {e}")
        raise


# --------------------------
# 业务逻辑层 (BLL)
# --------------------------
def _format_closing_status(code) -> str:
    status_map = {
        0: '待交割', 1: '交割处理中', 2: '交割完成',
        3: '交割失败', 4: '交割超时', 5: '部分交割成功', 6: '已违约'
    }
    return status_map.get(code, f'未知状态({code})')


def _format_trade_status(code) -> str:
    return {1: '待交易', 2: '处理中', 3: '交易完成'}.get(code, f'未知({code})')


def _show_data_details(order: Dict, receipt: Dict):
    """打印订单与凭证明细"""
    print("\n" + "=" * 50)
    print("【订单明细】BAOFU_CBCA.T_USER_EXCHANGE_ORDER")
    print(f"订单号: {order['EXCHANGE_ID']}")
    print(f"创建时间: {order['CREATE_AT'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"最后更新: {order['UPDATE_AT'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"原交割日期: {order['CLOSING_DATE']}")
    print(f"状态: {_format_closing_status(order['CLOSING_STATUS'])}")

    print("\n【凭证明细】BAOFU_TRADE.T_TRADE_RECEIPT")
    print(f"交易订单号: {receipt['RECEIPT_NO']}")
    print(f"交易时间: {receipt['TRADE_DATE']} {receipt['TRADE_TIME']}")
    print(f"原交割日期: {receipt['CLOSING_DATE']}")
    print(f"交易状态: {_format_trade_status(receipt['TRADE_STATUS'])}")
    print(f"最后更新: {receipt['UPDATE_AT'].strftime('%Y-%m-%d %H:%M:%S')}")


def process_forward_order(
    exchange_id: str,
    action: str = 'query',
    new_date: Optional[str] = None,
    env: str = 'FAT'
):
    """
    远期订单处理器：查询或更新交割日期
    :param exchange_id: 订单号
    :param action: 操作类型 ['query', 'update']
    :param new_date: 新交割日期，格式 'YYYY-MM-DD'
    :param env: 环境 ['FAT', 'UAT']
    """
    conn = None
    try:
        # 获取数据库连接
        conn = _get_connection(env.upper())
        logger.info(f"🔍 开始处理订单: {exchange_id} (环境: {env.upper()}, 操作: {action})")

        # 查询数据
        order = _query_order(conn, exchange_id)
        receipt = _query_receipt(conn, exchange_id)

        if not order:
            raise ValueError(f"❌ 订单表未找到订单: {exchange_id}")
        if not receipt:
            raise ValueError(f"❌ 凭证表未找到远期订单记录: {exchange_id}")

        # 展示当前状态
        _show_data_details(order, receipt)

        # 执行更新
        if action == 'update':
            if not new_date:
                raise ValueError("❌ 更新操作必须提供 new_date 参数")

            logger.info(f"📅 正在将交割日期从 {order['CLOSING_DATE']} 修改为 {new_date}...")

            _update_order_and_receipt(conn, exchange_id, new_date)
            conn.commit()

            # 查询更新后数据
            updated_order = _query_order(conn, exchange_id)
            updated_receipt = _query_receipt(conn, exchange_id)

            # 显示变更结果
            print("\n" + "=" * 50)
            print("✅ 更新完成！变更结果：")
            print(f"交割日期: {order['CLOSING_DATE']} → {new_date}")
            _show_data_details(updated_order, updated_receipt)
            logger.info(f"✅ 订单 {exchange_id} 更新成功")

        elif action == 'query':
            logger.info(f"✅ 查询完成")
        else:
            raise ValueError(f"❌ 不支持的操作类型: {action}")

    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"❌ 操作失败: {str(e)}")
        raise

    finally:
        if conn:
            conn.close()
            logger.info("🔗 数据库连接已关闭")


# --------------------------
# 主程序入口
# --------------------------
if __name__ == "__main__":
    # 示例：单个订单更新（UAT环境）
    try:
        process_forward_order(
            exchange_id="2605141101000564866",
            action="update",
            new_date="2026-05-13",
            env="UAT"  # 可改为 "FAT"
        )
    except Exception as e:
        logger.error(f"程序执行失败: {e}")

    # 示例：批量更新（可选）
    # batch_orders = [
    #     ("2503171533006118013", "2025-03-18"),
    #     ("2503171533006118014", "2025-03-19")
    # ]
    # for order_id, date in batch_orders:
    #     try:
    #         process_forward_order(exchange_id=order_id, action="update", new_date=date, env="FAT")
    #     except Exception as e:
    #         logger.error(f"批量处理失败: {order_id} - {e}")