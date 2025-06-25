import pymysql


# ========== 配置 ==========
def get_db_config(env='UAT'):
    configs = {
        'FAT': {
            'host': '10.0.19.206',
            'port': 3306,
            'user': 'GEPHOLDING',
            'password': 'GEPHOLDING',
            'database': 'BAOFU_CBCA',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        },
        'UAT': {
            'host': '10.0.23.200',
            'port': 3306,
            'user': 'BAOFOO_CBPAY',
            'password': 'BAOFOO_CBPAY',
            'database': 'BAOFU_CBCA',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
    }
    return configs.get(env, configs['UAT'])


# ========== 数据访问层（DAO）==========
class CurrencyRuleDAO:
    def __init__(self):
        config = get_db_config()
        self.connection = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config['charset'],
            cursorclass=config['cursorclass']
        )

    def find_ccy_group(self, possible_pairs):
        try:
            with self.connection.cursor() as cursor:
                query = """
                    SELECT DISTINCT CCY_GROUP FROM `BAOFU_CRM`.T_CCY_TRADE_TIME_RULE 
                    WHERE CCY_GROUP IN (%s, %s) AND STATUS = 1
                """
                cursor.execute(query, possible_pairs)
                result = cursor.fetchone()
                return result['CCY_GROUP'] if result else None
        finally:
            self.connection.close()


# ========== 业务逻辑层（Service）==========
class CurrencyRuleService:
    def __init__(self):
        self.dao = CurrencyRuleDAO()

    def find_real_ccy_pair(self, source_ccy, target_ccy):
        possible_pairs = [f"{source_ccy}/{target_ccy}", f"{target_ccy}/{source_ccy}"]
        found_pair = self.dao.find_ccy_group(possible_pairs)
        return found_pair

    def determine_direction(self, from_source_ccy, to_target_ccy, real_ccy_pair):
        """
        根据输入币种和真实货币对，判断是“客买”还是“客卖”
        :param from_source_ccy: 用户传入的原始卖出币种
        :param to_target_ccy: 用户传入的目标买入币种
        :param real_ccy_pair: 真实存在的货币对（如 CNH/PHP）
        :return: str -> "客买" 或 "客卖"
        """
        base_ccy, quote_ccy = real_ccy_pair.split('/')

        if from_source_ccy == quote_ccy and to_target_ccy == base_ccy:
            return "客买"
        elif from_source_ccy == base_ccy and to_target_ccy == quote_ccy:
            return "客卖"
        else:
            return "未知方向"

# ========== 主程序入口 ==========
if __name__ == "__main__":
    service = CurrencyRuleService()
    source_ccy = "CNH"
    target_ccy = "PHP"

    # 查询真实货币对
    real_pair = service.find_real_ccy_pair(source_ccy, target_ccy)


    if not real_pair:
        print("未找到对应的货币对配置。")
    else:
        print(f"找到真实货币对: {real_pair}")

        # 示例1: 客户从 PHP 换成 CNH （即 PHP -> CNH）
        from_source_ccy = "PHP"
        to_target_ccy = "CNH"
        direction = service.determine_direction(from_source_ccy, to_target_ccy, real_pair)
        print(f"[{from_source_ccy} -> {to_target_ccy}] 交易方向为：{direction}")

        # 示例2: 客户从 CNH 换成 PHP （即 CNH -> PHP）
        from_source_ccy = "CNH"
        to_target_ccy = "PHP"
        direction = service.determine_direction(from_source_ccy, to_target_ccy, real_pair)
        print(f"[{from_source_ccy} -> {to_target_ccy}] 交易方向为：{direction}")