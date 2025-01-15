import pymysql as ms

# 数据库连接配置
db_config = {
    'host': '10.0.19.206',
    'user': 'GEPHOLDING',
    'password': 'GEPHOLDING',
    'database': 'BAOFU_CBCA',  # 替换为你的数据库名称
    'charset': 'utf8mb4',  # 指定字符集
    'cursorclass': ms.cursors.DictCursor  # 返回字典格式的结果
}

def connect_to_db():
    """建立数据库连接"""
    try:
        connection = ms.connect(**db_config)
        print("成功连接到数据库")
        return connection
    except ms.MySQLError as e:
        print(f"连接数据库失败: {e}")
        raise

def get_exchange_rate(user_no, biz_type, ccy_pair, closing_type):
    """根据用户号、业务类型、货币对和期限获取汇率"""
    connection = None
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            # 定义查询语句，一次性获取用户、代理商和全局的配置
            query = """
            SELECT BID_CHANNEL_ID, ASK_CHANNEL_ID, QUOTE_MODE 
            FROM T_USER_CHANNEL_CONFIG 
            WHERE USER_NO = %s 
              AND BIZ_TYPE = %s 
              AND CCY_PAIR = %s 
              AND CLOSING_TYPE = %s 
              AND STATUS = '1'
            ORDER BY FIELD(QUOTE_MODE, 2, 1, 0);  -- 按照用户 > 代理商 > 全局的顺序排序
            """

            cursor.execute(query, (user_no, biz_type, ccy_pair, closing_type))
            results = cursor.fetchall()

            official_rate = "DEFAULT_OFFICIAL_RATE"  # 假设这是官方渠道的默认汇率值

            for result in results:
                if check_rate_exists(cursor, result, ccy_pair):
                    return {
                        'rate': get_rate_from_channel(cursor, result['BID_CHANNEL_ID'], result['ASK_CHANNEL_ID'], ccy_pair),
                        'source': 'User' if result['QUOTE_MODE'] == 2 else 'Agent' if result['QUOTE_MODE'] == 1 else 'Global'
                    }

            # 如果所有优先级都没有找到对应的货币对汇率，则取官方渠道的默认配置
            return {
                'rate': official_rate,
                'source': 'Official'
            }

    except ms.MySQLError as e:
        print(f"查询数据库失败: {e}")
        raise
    finally:
        if connection:
            connection.close()

def check_rate_exists(cursor, channel_info, ccy_pair):
    """检查给定渠道是否包含所需的货币对汇率"""
    # 这里可以是另一个SQL查询或者API调用，具体取决于你的系统架构
    rate = get_rate_from_channel(cursor, channel_info['BID_CHANNEL_ID'], channel_info['ASK_CHANNEL_ID'], ccy_pair)
    return rate is not None

def get_rate_from_channel(cursor, bid_channel_id, ask_channel_id, ccy_pair):
    """从指定渠道获取汇率"""
    # 这里可以是另一个SQL查询或者API调用，具体取决于你的系统架构
    # 例如，假设我们有一个函数可以根据渠道ID和货币对获取汇率
    # 返回汇率值，如果没有找到则返回None
    # 示例：
    # query = "SELECT rate FROM exchange_rates WHERE BID_CHANNEL_ID = %s AND ASK_CHANNEL_ID = %s AND currency_pair = %s"
    # cursor.execute(query, (bid_channel_id, ask_channel_id, ccy_pair))
    # result = cursor.fetchone()
    # return result['rate'] if result else None

    return "RATE_FROM_CHANNEL"  # 假设这是从渠道获取的汇率值

def main():
    # 请求参数
    request_params = {
        'bizType': 7,
        'userNo': 5181240821000008798,
        'sourceCcy': 'USD',
        'destCcy': 'CNH',
        'ccyPairList': ['USD/CNH'],
        'closingType': 'TOD'
    }

    # 获取汇率
    try:
        result = get_exchange_rate(
            request_params['userNo'],
            request_params['bizType'],
            request_params['ccyPairList'][0],
            request_params['closingType']
        )
        print(f"汇率: {result['rate']}, 来源: {result['source']}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()