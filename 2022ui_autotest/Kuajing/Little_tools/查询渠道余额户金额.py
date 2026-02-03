"""
@Author    : duansea
@Date      : 2025/7/10 16:13
@Description: [文件功能的简要描述]
"""
import pymysql
from pymysql.cursors import DictCursor
from tabulate import tabulate


def _get_db_config(env: str) -> dict:
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


def query_jpm_accounts(env: str, ccys=None, params = ['%JPM%']):
    config = _get_db_config(env)

    connection = pymysql.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
        charset=config['charset'],
        cursorclass=config['cursorclass']
    )

    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT ACCOUNT_NO, ACCOUNT_ENTITY_NAME, CURRENT_BALANCE, CCY 
                FROM `T_ACC_BAL`
                WHERE `ACCOUNT_ENTITY_NAME` LIKE %s
            """
            # params = ['%JPM区块链户%']

            if ccys and isinstance(ccys, list):
                sql += " AND CCY IN (" + ",".join(["%s"] * len(ccys)) + ")"
                params.extend(ccys)

            sql += " ORDER BY `ID` DESC LIMIT 0, 15"

            cursor.execute(sql, params)
            results = cursor.fetchall()

            if not results:
                print("未找到匹配的账户。")
                return

            headers = ["ACCOUNT_NO", "ACCOUNT_ENTITY_NAME", "CURRENT_BALANCE", "CCY"]
            formatted_results = [
                [row['ACCOUNT_NO'], row['ACCOUNT_ENTITY_NAME'], f"{float(row['CURRENT_BALANCE']):,.3f}", row['CCY']]
                for row in results
            ]
            print(tabulate(formatted_results, headers=headers, tablefmt='grid'))

    finally:
        connection.close()

    
# 示例调用
if __name__ == '__main__':
    # 查询所有币种
    # query_jpm_accounts('FAT',params = ['%JPM区块链户%'] )

    # query_jpm_accounts('UAT', params=['%Tenpay%'])
    # query_jpm_accounts('FAT', params=['%wiseFx%'])  #--uat环境  用wise

    # 或者指定查询特定币种，例如 USD 和 EUR
    # query_jpm_accounts('FAT', ccys=['USD', 'EUR'])
    query_jpm_accounts('FAT', params=['%渣打%'])  #--fat环境  渣打