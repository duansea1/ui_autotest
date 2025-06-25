
"""
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
import pymysql
from datetime import datetime

# # 数据库连接配置-fat
DB_CONFIG = {
    'host': '10.0.19.206',
    'port': 3306,
    'user': 'GEPHOLDING',
    'password': 'GEPHOLDING',
    'database': 'BAOFU_CBCA',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 数据库连接配置-uat环境
# DB_CONFIG = {
#     'host': '10.0.23.200',
#     'port': 3306,
#     'user': 'BAOFOO_CBPAY',
#     'password': 'BAOFOO_CBPAY',
#     'database': 'BAOFU_CBCA',
#     'charset': 'utf8mb4',
#     'cursorclass': pymysql.cursors.DictCursor
# }

# --------------------------
# 增强型数据访问层 (DAL)
# --------------------------
def _get_db_connection():
    """创建数据库连接（自动选择主库）"""
    return pymysql.connect(**DB_CONFIG)


def _query_full_order(conn, exchange_id):
    """获取订单全量数据"""
    with conn.cursor() as cursor:
        sql = """
            SELECT 
                EXCHANGE_ID, 
                CLOSING_DATE,
                CLOSING_STATUS,
                CREATE_AT,
                UPDATE_AT 
            FROM BAOFU_CBCA.T_USER_EXCHANGE_ORDER 
            WHERE EXCHANGE_ID = %s"""
        cursor.execute(sql, (exchange_id,))
        return cursor.fetchone()


def _query_full_receipt(conn, exchange_id):
    """获取凭证全量数据"""
    with conn.cursor() as cursor:
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
            WHERE REQUEST_NO = %s """
              # AND CLOSING_TYPE = 'FORWARD'
        cursor.execute(sql, (exchange_id,))
        return cursor.fetchone()


def _update_dates(conn, exchange_id, new_date):
    """执行双表日期更新"""
    with conn.cursor() as cursor:
        # 更新订单表
        # ,CREATE_AT = '2025-04-06 11:42:20'
        cursor.execute(""" 
                UPDATE BAOFU_CBCA.T_USER_EXCHANGE_ORDER 
                SET CLOSING_DATE = %s,
                    UPDATE_AT = NOW()
                WHERE EXCHANGE_ID = %s""",
                       (new_date, exchange_id))

        # 更新凭证表
        cursor.execute(""" 
                UPDATE BAOFU_TRADE.T_TRADE_RECEIPT 
                SET CLOSING_DATE = %s,
                    UPDATE_AT = NOW() 
                WHERE REQUEST_NO = %s""",
                       (new_date, exchange_id))


# --------------------------
# 增强型业务逻辑层 (BLL)
# --------------------------
def format_closing_status(code):
    """订单状态解码"""
    status_map = {
        0: '待交割', 1: '处理中', 2: '完成',
        3: '失败', 4: '超时', 5: '部分成功', 6: '已违约'
    }
    return status_map.get(code, f'未知状态({code})')


def format_trade_status(code):
    """交易状态解码"""
    return {1: '待交易', 2: '处理中', 3: '完成'}.get(code, f'未知({code})')


def show_data_details(order, receipt):
    """可视化数据展示"""
    print("\n【订单明细】BAOFU_CBCA.T_USER_EXCHANGE_ORDER")
    print(f"订单号: {order['EXCHANGE_ID']}")
    print(f"创建时间: {order['CREATE_AT'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"最后更新: {order['UPDATE_AT'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"交割日期: {order['CLOSING_DATE']}")
    print(f"状态: {format_closing_status(order['CLOSING_STATUS'])}")

    print("\n【凭证明细】BAOFU_TRADE.T_TRADE_RECEIPT")
    print(f"交易日期: {receipt['TRADE_DATE']} {receipt['TRADE_TIME']}")
    print(f"交易订单号: {receipt['RECEIPT_NO']}")
    print(f"交割日期: {receipt['CLOSING_DATE']}")
    print(f"交易状态: {format_trade_status(receipt['TRADE_STATUS'])}")
    print(f"最后更新: {receipt['UPDATE_AT'].strftime('%Y-%m-%d %H:%M:%S')}")


def process_forward_order(exchange_id, action='query', new_date=None):
    """
    远期订单处理器
    :param exchange_id: 订单号
    :param action: 操作类型 [query|update]
    :param new_date: 新交割日期 (仅action=update时需传入)
    """
    conn = _get_db_connection()
    try:
        # 数据获取
        order = _query_full_order(conn, exchange_id)
        receipt = _query_full_receipt(conn, exchange_id)

        if not all([order, receipt]):
            raise ValueError("查询无结果，请检查订单号是否正确")

        # 当前状态展示
        print("\n" + "=" * 40)
        print(f"订单号 {exchange_id} 当前状态")
        show_data_details(order, receipt)

        # 执行更新逻辑
        if action == 'update':
            if not new_date:
                raise ValueError("更新操作必须提供new_date参数")

            # 执行更新
            _update_dates(conn, exchange_id, new_date)
            conn.commit()

            # 获取更新后数据
            updated_order = _query_full_order(conn, exchange_id)
            updated_receipt = _query_full_receipt(conn, exchange_id)

            # 变更对比展示
            print("\n" + "=" * 40)
            print(f"订单号 {exchange_id} 变更结果")
            print(f"交割日期变更: {order['CLOSING_DATE']} → {new_date}")
            show_data_details(updated_order, updated_receipt)
            print("\n✅ 数据更新完成")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ 操作异常: {str(e)}")
        raise
    finally:
        conn.close()

        # --------------------------



if __name__ == "__main__":

    # 示例1：仅查询
    # process_forward_order("2503191907006119109")

    # # 示例2：查询并更新
    process_forward_order(exchange_id="2504230956006150277",action="update",new_date="2025-04-23")  # 更新交割日

    # # 批量执行
    # orders = [
    #     ("2503171533006118013", "2025-03-18"),
    #     ("2503171533006118014", "2025-03-19")
    # ]
    # for order_id, new_date in orders:
    #     process_forward_order(exchange_id=order_id, action="update",new_date=new_date)