import requests
import json
from dataclasses import dataclass
from django.utils.log import log_response
from enum import Enum
from decimal import Decimal
from icecream import ic
from typing import Optional, List, Tuple, Dict, Any
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime



# ========== 货币对查询==========
class CurrencyRuleDAO:
    def __init__(self, env: str = 'FAT'):
        config = _get_db_config(env)
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
    def __init__(self, env: str):
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
            print("⏩客买-购汇方向-ask")
            return "buy"
        elif from_source_ccy == base_ccy and to_target_ccy == quote_ccy:
            print("⏩客卖-结汇方向-bid")
            return "sell"
        else:
            return "NoDirection"

def find_real_ccy_pair(from_source_ccy, to_target_ccy, env='FAT'):
    """ 查找真实货币对，返回货币对及方向 """
    service = CurrencyRuleService(env)
    # 查到货币对
    real_ccy_pair = service.find_real_ccy_pair(from_source_ccy, to_target_ccy)
    if not real_ccy_pair:
        real_ccy_pair = "NoRealCurrency"
        direction = "NoDirection"
        return "未知的货币对"

    if from_source_ccy==to_target_ccy:
        real_ccy_pair = "NoRealCurrency"
        direction = "NoDirection"
        return  direction
    # 判断方向
    direction = service.determine_direction(from_source_ccy, to_target_ccy, real_ccy_pair)
    print(f"⏩---》货币对{real_ccy_pair}   [{from_source_ccy} -> {to_target_ccy}] 交易方向为：{direction}")
    return  direction


# 银行code映射表
BANK_CODE_MAP = {
    "44": "Guangxi Dongxing Rural Commercial Bank Co., Ltd.",
    "45": "CHINA EVERBRIGHT BANK, SHANGHAI BRANCH",
    "24": "ZHEJIANG CHOUZHOU COMMERCIAL BANK",
    "35": "KINCHENG BANK OF TIANJIN CO., LTD",
    "25": "Ping An Bank Shanghai Branch",
    "36": "Mlg BANK OF TIANJIN CO., LTD",
    "37": "COMMUNITY RURAL BANK OF ROMBLON, INC.(NetBank)",
    "39": "BANK OF CHINA SHENZHEN BRANCH",
    "0": "本地收款银行",
    "1": "DBS Bank (Hong Kong) Limited",
    "2": "J.P.morgan",
    "3": "Standard Chartered Korea(SC First)",
    "5": "Banking Circle S.A.",
    "6": "The Currency Cloud Limited",
    "41": "Standard Chartered Bank (Hong Kong) Limited",
    "42": "BIDV-Joint Stock Commercial Bank for Investment and Development of Vietnam",
    "31": "BANK OF KUNLUN CO., LTD",
    "43": "MSB-Vietnam Maritime Commercial Stock Bank",
    "32": "VIETNAM MARITIME COMMERCIAL JOINT STOCK BANK",
}

class RateBusinessTypeEnum(Enum):
    BUSINESS_all = "0"
    BUSINESS_gep = "GEP_EXCHANGE"    # GEP_EXCHANGE("7", "GEP汇兑"),
    BUSINESS_shop = "PLATFORM_LOGISTICS"    # PLATFORM_LOGISTICS("8", "电商&服贸"),
    BUSINESS_b2b = "B2B_BUSINESS"  # B2B_BUSINESS("9", "E贸汇"),

RATE_BUSINESS_TYPE_MAP = {
    "ALL": "0",  # 全局
    "GEP_EXCHANGE": "7",
    "PLATFORM_LOGISTICS": "8",
    "B2B_BUSINESS": "9"
}

@dataclass
class AccountFxRateReq:
    userNo: Optional[int] = None  # 用户号，默认0全局
    orderNo: Optional[str] = None  # 交易号
    business: Optional[RateBusinessTypeEnum] = None  # 业务线
    receiveChannel: Optional[str] = None  # 收款渠道
    bank: Optional[str] = None  # 银行
    ReceiveCcy: Optional[str] = None  # 渠道收款币种
    ReceiveAmt: Optional[Decimal] = None  # 渠道收款金额
    accountCcy: Optional[str] = None  # 渠道入账币种
    accountAmt: Optional[Decimal] = None  # 渠道入账金额
    merchantCcy: Optional[str] = None  # 商户入账币种


def _get_db_config(env: str) -> dict:
    configs = {
        'FAT': {
            'host': '10.0.19.206',
            'port': 3306,
            'user': 'GEPHOLDING',
            'password': 'GEPHOLDING',
            'database': 'BAOFU_CBCA',
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        },
        'UAT': {
            'host': '10.0.23.200',
            'port': 3306,
            'user': 'BAOFOO_CBPAY',
            'password': 'BAOFOO_CBPAY',
            'database': 'BAOFU_CBCA',
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        }
    }
    return configs.get(env, configs['FAT'])


def _build_query_conditions(req: AccountFxRateReq) -> List[Tuple[Dict[str, Any], str]]:
    def clean_value(val):
        return val.value if isinstance(val, Enum) else val

    # 提取字段（允许部分字段为None）
    rcv_channel = req.receiveChannel if hasattr(req, 'receiveChannel') and req.receiveChannel is not None else None
    rcv_ccy = req.ReceiveCcy
    acct_ccy = req.accountCcy
    merch_ccy = req.merchantCcy

    conditions = []

    # 构建兜底候选值
    user_nos = []
    if req.userNo is not None:
        user_nos.append(req.userNo)
    user_nos.append(0)  # 兜底值

    businesses = []
    if req.business is not None:
        business_value = clean_value(req.business)
        business_code = RATE_BUSINESS_TYPE_MAP.get(business_value, business_value)
        businesses.append(business_code)
    businesses.append("0")  # 兜底值

    banks = []
    if req.bank is not None:
        banks.append(req.bank)
    banks.append("")  # 兜底值

    # 按优先级生成查询组合
    for user_no in user_nos:
        for business in businesses:
            for bank in banks:
                cond = {
                    "USER_NO": user_no,
                    "BUSINESS": business,
                    "BANK": bank,
                    "RECEIVE_CCY": rcv_ccy,
                    "ACCOUNT_CCY": acct_ccy,
                    "MERCHANT_CCY": merch_ccy,
                    "STATUS": "OPEN"
                }
                # 动态添加RECEIVE_CHANNEL（如果不为None）
                if rcv_channel is not None:
                    cond["RECEIVE_CHANNEL"] = rcv_channel

                desc = f"商户号={user_no}, 业务线={business}, 银行={bank}" + \
                       (f", 渠道={rcv_channel}" if rcv_channel is not None else "")
                conditions.append((cond, desc))

    return conditions


def query_config_from_db(req: AccountFxRateReq, env: str = 'FAT') -> Optional[dict]:
    db_config = _get_db_config(env)

    with pymysql.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            conditions = _build_query_conditions(req)
            for condition, desc in conditions:
                where_clause = " AND ".join([f"`{k}` = %s" for k in condition if k != "STATUS"])
                where_clause += " AND STATUS = 'OPEN'"
                values = [condition[k] for k in condition if k != "STATUS"]
                sql = f"""
                    SELECT * FROM T_ACCOUNT_FX_FLOAT_CONFIG
                    WHERE {where_clause}
                """
                print(f"尝试查询: {desc}")
                cursor.execute(sql, values)
                result = cursor.fetchone()
                if result:
                    print(f"✅ 匹配成功: {desc}")
                    return result
            print("❌ 未找到匹配配置")
            return None

def format_config_display(config: dict) -> str:
    formatted = {k: v for k, v in config.items()}
    for k, v in formatted.items():
        if isinstance(v, (Decimal, datetime)):
            formatted[k] = str(v)
    bank_code = formatted.get("BANK", "")
    bank_name = BANK_CODE_MAP.get(bank_code, f"未知银行({bank_code})")
    formatted["BANK"] = bank_name
    output = "\n【匹配配置】:\n"
    # for key, value in formatted.items():
    #     output += f"  {key:<5} : {value}\n"
    return output


# 接口调用部分保持不变 ip取容器的ip-漫道云
base_url = "http://10.254.192.119:21103/accountFxFloatConfig/queryRate"
headers = {"Content-Type": "application/json"}

def default_serializer(obj):
    if isinstance(obj, RateBusinessTypeEnum):
        return obj.value  # 显式转为 "B2B_BUSINESS"
    if isinstance(obj, Decimal):
        return str(obj)  # 避免精度丢失
    if isinstance(obj, datetime):
        return obj.isoformat()  # 标准时间格式
    return str(obj)

def query_rate(req_dto: AccountFxRateReq) -> dict:
    try:
        payload = json.dumps(req_dto.__dict__, default=default_serializer)
        # print("发送请求体:", payload)  # 可选：打印请求内容便于调试
        response = requests.post(base_url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {}


from decimal import Decimal


def calculate_merchant_amount(direction, channel_amount,  exchange_rate, fluctuation, channel_ccy, merchant_ccy):
    """
    计算商户入账金额（不使用 Decimal）。

    :param direction: 交易方向 ('BUY' 表示客买-购汇方向， 'SELL' 表示客卖-结汇方向)
    :param channel_amount: 渠道入账金额 (int 或 float)
    :param exchange_rate: 报价源汇率 (int 或 float)
    :param fluctuation: 浮动值（百分比，如 1 表示 1%）
    :return: 商户入账金额 (float)
    """

    # 统一转换为 float 避免类型冲突
    channel_amount = float(channel_amount)
    exchange_rate = float(exchange_rate)
    fluctuation = float(fluctuation)
    if channel_ccy==merchant_ccy:
        merchant_amount = round(channel_amount * (1 - fluctuation / 100), 6)
        print(f"⚠️{direction}方向-相同货币对，渠道入账金额={channel_amount}-{channel_ccy}, "
              f"报价源汇率={exchange_rate}, "
              f"浮动值={fluctuation}%, 商户入账金额={merchant_amount}-{merchant_ccy}")
        return merchant_amount
    print(f"⏩--------------{direction}")
    if direction.upper() == 'BUY':
        # 客买-购汇方向：渠道金额 ÷ 汇率 × (1 - 浮动%)
        merchant_amount = (channel_amount*100 / exchange_rate) * (1 - fluctuation / 100)
    elif direction.upper() == 'SELL':
        # 客卖-结汇方向：渠道金额 × 汇率 × (1 - 浮动%)
        merchant_amount = (channel_amount * exchange_rate/100) * (1 - fluctuation / 100)
    else:
        raise ValueError(f"未知的交易方向: {direction}")

    # 保留6位小数输出
    merchant_amount = round(merchant_amount, 6)

    print(f"客{direction}方向，渠道入账金额={channel_amount}{channel_ccy}, "
          f"报价源汇率={exchange_rate}, "
          f"浮动值={fluctuation}%, 商户入账金额={merchant_amount}{merchant_ccy}")

    return merchant_amount



if __name__ == "__main__":
    req_dto = AccountFxRateReq(
        userNo=5181240628000024148,  # 5181240821000008798-五五 、5181240628000024148-桐乡
        orderNo="ORDER123456",
        business=RateBusinessTypeEnum.BUSINESS_b2b,
        # receiveChannel="120092303811",  # GME-电商收款-1200923038 1108301001 1200923077-pay
        # bank="45",
        ReceiveCcy="PHP",
        ReceiveAmt=Decimal("10.00"),
        accountCcy="PHP",    # 渠道入账币种
        accountAmt=Decimal("10000"),
        merchantCcy="USD"     # 商户入账币种
    )
    log_response=  {"accountAmt":9890,"accountCcy":"VND","business":"B2B_BUSINESS","merchantCcy":"USD","orderNo":"20250625150859148","receiveAmt":9890,"receiveCcy":"VND","receiveChannel":"1200923050","userNo":5181240628000024148}

    req_dto1 = AccountFxRateReq(
        userNo=log_response.get("userNo"),  # 5181240821000008798-五五 、5181240628000024148-桐乡
        orderNo="ORDER123456",
        business=log_response.get("business"),
        # business="BUSINESS_b2b",
        receiveChannel=log_response.get("receiveChannel",None),  # GME-电商收款-1200923038 1108301001 1200923077-pay
        bank=log_response.get("bank"),
        ReceiveCcy=log_response.get("receiveCcy"),
        ReceiveAmt=Decimal(log_response.get("receiveAmt")),
        accountCcy=log_response.get("accountCcy"),  # 渠道入账币种
        accountAmt=Decimal(log_response.get("accountAmt")),
        merchantCcy=log_response.get("merchantCcy")     # 商户入账币种
    )
    # ic(req_dto)


    db_result = query_config_from_db(req_dto, env='FAT')
    if db_result:
        print("匹配的配置信息", db_result)
        print("🎉匹配的汇率渠道🎉", db_result.get("RATE_RESOURCE", ""))
        print("🎉匹配的浮动值🎉", db_result.get("FLOAT_PERCENT", ""))
        # print(format_config_display(db_result))

    else:
        print("⚠️没有找到符合条件的配置⚠")

    # 调用汇率查询接口


    result = query_rate(req_dto)

    # 货币对查询
    print("\n")
    direction = find_real_ccy_pair(req_dto.accountCcy, req_dto.merchantCcy, env='FAT')
    if result.get("success", None):
        print("🎉api调用OK，查询到的汇率和入账金额", result)

        # 计算商户入账金额
        calculate_merchant_amount(direction, channel_amount=req_dto.accountAmt,
                                  exchange_rate=result['result'].get('rate', 0),
                                  fluctuation=float(db_result.get("FLOAT_PERCENT") or 0),
                                  channel_ccy=req_dto.accountCcy, merchant_ccy=req_dto.merchantCcy)
    else:
        print("⚠️汇率查询计算失败：",result)






