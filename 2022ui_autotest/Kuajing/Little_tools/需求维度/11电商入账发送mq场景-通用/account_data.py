"""
@Author      : duansea
@Date        : 2025/7/31 10:30
@Description : 统一管理各环境的测试账户数据
              结构：{env: {userNo: {account_key: data}}}
              支持通过 env + userNo + account_key 动态获取
"""

# 所有测试数据按 {env: {userNo: {account_key: data}}} 结构组织
# 每个字段均附带详细说明，便于维护与调试
TEST_DATA_POOL = {
    "fat": {
        5181240823000000178: {
            "yiyi_shop": {
                "bankPayeeFeeCcy": "USD",   # 渠道手续费币种 (BANK_PAYEE_FEE_CCY)
                "channelId": 1200923023,    # 收款渠道ID → DBS银行-电商收款
                "payeeAccountNo": "7990024100002962",  # 收款方银行账号
                "payeeCcy": "USD",          # 渠道入账币种 (PAYEE_CCY)，即资金到账币种
                "payeeType": 1,             # 账号类型 1-电商  3-B2B收款  2-gep收款  4-服贸交易
                "remitCcy": "USD",          # 汇款币种 (REMIT_CCY)，即出款行汇出币种
                "storeNo": 2502191503307939572,  # 关联店铺号（电商平台专用），非电商则为0
                "remarks": "fat环境-上海一一网络科技有限公司-自动化--gep-电商收款账户"
            }
        },
    5181241126000123328: {
            "qiya_shop": {
                "bankPayeeFeeCcy": "EUR",   # 渠道手续费币种 (BANK_PAYEE_FEE_CCY)
                "channelId": 1108701001,    # 收款渠道ID → BC
                "payeeAccountNo": "20250527172221152",  # 收款方银行账号
                "payeeCcy": "EUR",          # 渠道入账币种 (PAYEE_CCY)，即资金到账币种
                "payeeType": 1,             # 账号类型 1-电商  3-B2B收款  2-gep收款  4-服贸交易
                "remitCcy": "EUR",          # 汇款币种 (REMIT_CCY)，即出款行汇出币种
                "storeNo": 2507161346006207661,  # 关联店铺号（电商平台专用），非电商则为0
                "remarks": "fat环境-qiya"
            }
        },
        5181240731000102528: {  # 用户信息：手机号 17681032993，姓名 董春旭
            "shop_ozon_cnh": {
                "bankPayeeFeeCcy": "CNH",   # 渠道手续费币种 → CNH离岸人民币
                "channelId": 1200923065,    # 收款渠道ID → GEP自有银行渠道
                "payeeAccountNo": "81561210000000100299",  # 收款方虚拟银行账号
                "payeeCcy": "CNH",          # 入账币种：CNH
                "payeeType": 1,             # 账号类型：1-电商
                "remitCcy": "CNH",          # 汇款币种：CNH
                "storeNo": 2509111817006266227,               # 非电商平台使用，设为0
                "remarks": "董春旭-fat-ozon-CNH-电商收款账户"
            },
            "shop_wb_cnh": {
                "bankPayeeFeeCcy": "USD",   # 渠道手续费币种 → USD美元
                "channelId": 1200923065,    # 收款渠道ID → GEP自有银行渠道
                "payeeAccountNo": "81561210000000100297",  # 收款方虚拟银行账号
                "payeeCcy": "CNH",          # 入账币种：USD
                "payeeType": 1,             # 账号类型：1-电商
                "remitCcy": "CNH",          # 汇款币种：USD
                "storeNo": 2509111736006266219,               # 非电商平台使用，设为0
                "remarks": "董春旭-fat-wb-USD-电商收款账户"
            },
        },
        5181240821000008798:{    # 17681032991 香港五五网络科技公司

            "shop_alone_hkd": {
                "bankPayeeFeeCcy": "HKD",   # 渠道手续费币种 → HKD港币
                "channelId": 1200923023,    # DBS-收款渠道
                "payeeAccountNo": "799001056414681",  # 收款方虚拟银行账号
                "payeeCcy": "HKD",          # 入账币种：HKD
                "payeeType": 1,             # 账号类型：1-电商
                "remitCcy": "HKD",          # 汇款币种：HKD
                "storeNo": 2509091904006264535,               # 独立站
                "remarks": "香港五五网络科技公司-fat-独立站-hkd-电商收款账户"
            },
            "b2b_eur": {
                            "bankPayeeFeeCcy": "EUR",   # 渠道手续费币种 → EUR欧元
                            "channelId": 1200923053,    # Banking Circle S.A. - E贸汇
                            "payeeAccountNo": "DK9189000020547275",  # 收款方虚拟银行账号
                            "payeeCcy": "EUR",          # 入账币种：HKD
                            "payeeType": 3,             # 账号类型：3-B2B收款
                            "remitCcy": "EUR",          # 汇款币种：HKD
                            "storeNo": 0,               #
                            "remarks": "香港五五网络科技公司-fat-b2b-EUR-B2B收款账户"
                        },

            "b2b_php": {
                            "bankPayeeFeeCcy": "PHP",   # 渠道手续费币种 → VND越南盾
                            "channelId": 1200923077 ,    # Payso-电商收款-API- E贸汇
                            "payeeAccountNo": "P900100109721",  # 收款方虚拟银行账号
                            "payeeCcy": "PHP",          # 入账币种：VND
                            "payeeType": 3,             # 账号类型：3-B2B收款   
                            "remitCcy": "PHP",          # 汇款币种：VND
                            "storeNo": 0,               #
                            "remarks": "香港五五网络科技公司-fat-b2b-VND-B2B收款账户"
                        },
        },
        5181240628000024148: {  # 用户信息：手机号 13166210872，商户名 桐乡市高桥旭木汽车咨询服务部
            "cc_vnd": {
                "bankPayeeFeeCcy": "VND",   # 渠道手续费币种 → VND越南盾
                "channelId": 1200923050,    # 收款渠道ID → CurrencyCloud - 电商平台
                "payeeAccountNo": "GB85TCCL12345669644978",  # 英国IBAN账号（CurrencyCloud提供）
                "payeeCcy": "VND",          # 入账币种：VND
                "payeeType": 3,             # 账号类型：3=B2B收款
                "remitCcy": "VND",          # 汇款币种：VND
                "storeNo": 0,               # 非独立站/平台店，无店铺号
                "remarks": "fat:的B2B入账-CurrencyCloud - 电商平台"
            },
            "ebay_usd": {
                "bankPayeeFeeCcy": "PHP",   # 渠道手续费币种 → PHP菲律宾比索（模拟多币种场景）
                "channelId": 1200923050,    # 收款渠道ID → CurrencyCloud - 电商平台
                "payeeAccountNo": "0333597819",  # 虚拟子账号（对应 ebay-usd 站点）
                "payeeCcy": "PHP",          # 入账币种：PHP
                "payeeType": 1,             # 账号类型：1=gep电商收款（平台卖家）
                "remitCcy": "PHP",          # 汇款币种：PHP
                "storeNo": 2507111628006204734,  # 店铺号 → 推断为 ebay-usd 平台站点
                "remarks": "我的桐乡-fat-CurrencyCloud - 电商平台"
            },
            "local_eur_gbp": {
                "bankPayeeFeeCcy": "GBP",   # 渠道手续费币种 → PHP菲律宾比索（模拟多币种场景）
                "channelId": 1108701001,    # 收款渠道ID → Banking Circle S.A.
                "payeeAccountNo": "20250709154816821",  # 虚拟子账号
                "payeeCcy": "GBP",          # 入账币种：PHP
                "payeeType": 1,             # 账号类型：1=gep电商收款（平台卖家）
                "remitCcy": "GBP",          # 汇款币种：PHP
                "storeNo": 2509101920006265584,  # 店铺号 → 推断为 ebay-usd 平台站点
                "remarks": "我的桐乡-fat-new-local-other"
            },
            "shopify_eur": {
                "bankPayeeFeeCcy": "GBP",   # 渠道手续费币种 → PHP菲律宾比索（模拟多币种场景）
                "channelId": 1108701001,    # 收款渠道ID → Banking Circle S.A.
                "payeeAccountNo": "20250709154816821",  # 虚拟子账号
                "payeeCcy": "GBP",          # 入账币种：PHP
                "payeeType": 1,             # 账号类型：1=gep电商收款（平台卖家）
                "remitCcy": "GBP",          # 汇款币种：PHP
                "storeNo": 2509101451006265371,  # 店铺号 → 推断为 ebay-usd 平台站点
                "remarks": "我的桐乡-fat-new-use-user-rule"

            },
            "b2b_php": {
                            "bankPayeeFeeCcy": "PHP",   # 渠道手续费币种 → VND越南盾
                            "channelId": 1200923077 ,    # Payso-电商收款-API- E贸汇
                            "payeeAccountNo": "P900100108612",  # 收款方虚拟银行账号
                            "payeeCcy": "PHP",          # 入账币种：VND
                            "payeeType": 3,             # 账号类型：3-B2B收款   
                            "remitCcy": "PHP",          # 汇款币种：VND
                            "storeNo": 0,               #
                            "remarks": "桐乡-fat-b2b-VND-B2B收款账户"
                        },
        }
    },
    "uat": {
        5181240702000026848: {  # 用户信息：手机号 13166210870，姓名 待确认（桐乡主账号）
            "tx_shop": {
                "bankPayeeFeeCcy": "EUR",   # 渠道手续费币种 → EUR欧元
                "channelId": 1108701001,    # 收款渠道ID → Adyen-电商收款
                "payeeAccountNo": "DK20240183",  # 收款账号（Adyen提供，丹麦格式）
                "payeeCcy": "EUR",          # 入账币种：EUR
                "payeeType": 1,             # 账号类型：1=gep电商收款
                "remitCcy": "EUR",          # 汇款币种：EUR
                "storeNo": 2407221607000032510,  # 店铺号 → uat环境电商店铺
                "remarks": "uat环境-桐乡--gep-电商收款账户"
            },
            "bank_pln": {
                "bankPayeeFeeCcy": "PLN",   # 渠道手续费币种 → PLN波兰兹罗提
                "channelId": 1200923053,    # 收款渠道ID → CurrencyCloud - B2B收款
                "payeeAccountNo": "79900202404773",  # 共用虚拟账号（B2B业务线）
                "payeeCcy": "PLN",          # 入账币种：PLN
                "payeeType": 3,             # 账号类型：3=B2B收款
                "remitCcy": "PLN",          # 汇款币种：PLN
                "storeNo": 0,               # B2B无店铺概念
                "remarks": "我的桐乡-uat-B2B收款账户"
            },
            "bank_php": {
                "bankPayeeFeeCcy": "PHP",   # 渠道手续费币种 → PHP菲律宾比索
                "channelId": 1200923079,    # 收款渠道ID → PesoPay - B2B本地化渠道
                "payeeAccountNo": "P900100110260",  # 本地收款账号（PesoPay分配）
                "payeeCcy": "PHP",          # 入账币种：PHP
                "payeeType": 3,             # 账号类型：3=B2B收款
                "remitCcy": "USD",          # 汇款币种：USD（跨境结算常用）
                "storeNo": 0,               # 非电商平台
                "remarks": "我的桐乡-uat--b2b收款账户"
            }
        }
    }
}

# 默认配置（用于简化调用）
DEFAULT_ENV = "uat"                       # 默认运行环境
DEFAULT_USERNO = 5181240702000026848       # 默认用户编号（桐乡主账号）
DEFAULT_ACCOUNT_KEY = "tx_shop"           # 默认账户标识（Adyen电商账户）


def get_test_data(env=None, userNo=None, account_key=None):
    """
    根据环境、用户编号、账户标识 获取测试数据
    :param env: 环境名，如 "fat", "uat"。若未传入，则使用 DEFAULT_ENV
    :param userNo: 用户编号（int 或 str 均可）。若未传入，则使用 DEFAULT_USERNO
    :param account_key: 账户标识，如 "yiyi_shop", "bank_pln" 等。若未传入，则使用 DEFAULT_ACCOUNT_KEY
    :return: dict 测试数据 or None（查找失败时打印错误信息）
    """
    env = env or DEFAULT_ENV
    userNo = userNo or DEFAULT_USERNO
    account_key = account_key or DEFAULT_ACCOUNT_KEY

    # 尝试逐层查找
    env_data = TEST_DATA_POOL.get(env)
    if not env_data:
        print(f"[ERROR] 未找到环境: '{env}'")
        return None

    user_data = env_data.get(userNo)
    if not user_data:
        print(f"[ERROR] 环境='{env}' 中未找到 userNo={userNo}")
        return None

    data = user_data.get(account_key)
    if data is None:
        print(f"[ERROR] userNo={userNo} 下未找到 account_key='{account_key}' 的数据")
        return None

    return data


# -----------------------------
# 可选：辅助函数（方便调试）
# -----------------------------

def list_all_accounts(env=None, userNo=None):
    """
    列出指定环境或用户的可用 account_key
    :param env: 环境名，如 "fat", "uat"
    :param userNo: 用户编号（可选），指定则只列出该用户下的账户
    """
    env = env or DEFAULT_ENV
    if env not in TEST_DATA_POOL:
        print(f"[INFO] 无可用环境: {env}")
        return

    env_data = TEST_DATA_POOL[env]
    if userNo:
        if userNo in env_data:
            accounts = list(env_data[userNo].keys())
            print(f"[INFO] userNo={userNo} 在 '{env}' 环境下可用账户: {accounts}")
        else:
            print(f"[INFO] userNo={userNo} 在 '{env}' 环境下无数据")
    else:
        print(f"[INFO] 环境 '{env}' 中的所有用户及账户:")
        for uid, accounts in env_data.items():
            print(f"  userNo={uid} → 账户列表: {list(accounts.keys())}")


# # 示例用法（调试时可取消注释）
# if __name__ == '__main__':
#     # 示例1：获取 uat 环境下 userNo 的 tx_shop 数据
#     data = get_test_data(env="uat", userNo=5181240702000026848, account_key="tx_shop")
#     print("示例1结果:", data)
#
#     # 示例2：使用默认值
#     data = get_test_data()
#     print("示例2（默认）:", data)
#
#     # 示例3：列出 uat 环境所有账户
#     list_all_accounts(env="uat")
#
#     # 示例4：查找特定 userNo 的所有账户
#     list_all_accounts(env="fat", userNo=5181240628000024148)