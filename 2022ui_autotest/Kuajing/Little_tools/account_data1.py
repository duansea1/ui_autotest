"""
@Author    : duansea
@Date      : 2025/7/31 10:30
@Description: [文件功能的简要描述]
"""
# config/testdata.py

from datetime import datetime



# 示例：多个测试数据配置
fat_yiyi_shop_data = {
    "bankPayeeFeeCcy": "USD",   # 渠道手续费金额 ---- 币种
    "channelId": 1200923023,    # DBS-收款渠道
    "payeeAccountNo": "7990024100002962",  # 收款方账号
    "payeeCcy": "USD",  # 渠道入账币种
    "payeeType": 1,     # 账号类型 1-gep电商  3-B2B收款  2-gep收款  4-服贸交易
    "remitCcy": "USD",      # 入账币种
    "storeNo": 2502191503307939572,     # 店铺号  没有则为0
    "userNo": 5181240823000000178,     # 商户号
    "remarks":"fat环境-上海一一网络科技有限公司-自动化--gep-电商收款账户"
}

# 来自 data1 (CurrencyCloud - 电商平台, VND币种)
fat_cc_vnd_data = {
    "bankPayeeFeeCcy": "VND",   # 渠道手续费金额 ---
    "channelId": 1200923050,    # ---------------CurrencyCloud - 电商平台
    "payeeAccountNo": "GB85TCCL12345669644978",  # --------------------------收款方账号
    "payeeCcy": "VND",          # 渠道入账币种
    "payeeType": 3,             # 账号类型  3-B2B收款
    "remitCcy": "VND",          # 渠道汇款币种   对应 CHANNEL_REMITTANCE_CCY
    "storeNo": 0,               # 店铺号
    "userNo": 5181240628000024148,  # 桐乡市高桥旭木汽车咨询服务部
    "remarks": "fat:的B2B入账-CurrencyCloud - 电商平台"
}

# 来自 data1: CurrencyCloud - 电商平台, storeNo=2507111628006204734 → 推断为 ebay-usd站点
fat_ebay_usd_data = {
    "bankPayeeFeeCcy": "PHP",   # 渠道手续费金额 ---
    "channelId": 1200923050,    # ---------------------------CurrencyCloud - 电商平台
    "payeeAccountNo": "0333597819",  # --------------------------收款方账号
    "payeeCcy": "PHP",          # 渠道入账币种
    "payeeType": 1,             # 账号类型 1-gep电商  3-B2B收款
    "remitCcy": "PHP",          # 渠道汇款币种   对应 CHANNEL_REMITTANCE_CCY
    "storeNo": 2507111628006204734,  # 店铺号
    "userNo": 5181240628000024148,  # 桐乡市高桥旭木汽车咨询服务部
    "remarks": "我的桐乡-fat-CurrencyCloud - 电商平台"
}

uat_tx_shop_data = {
    "bankPayeeFeeCcy": "EUR",   # 渠道手续费金额 ---- 币种
    "channelId": 1108701001,    # Banking Circle S.A.
    "payeeAccountNo": "DK20240183",  # 收款方账号
    "payeeCcy": "EUR",  # 渠道入账币种
    "payeeType": 1,     # 账号类型 1-gep电商  3-B2B收款  2-gep收款  4-服贸交易
    "remitCcy": "EUR",      # 入账币种
    "storeNo": 2407221607000032510,     # 店铺店铺名称：shopiftgeq
    "userNo": 5181240702000026848,     # 商户号
    "remarks":"uat环境-桐乡--gep-电商收款账户"
}



# 来自 data2: 银行渠道, storeNo=0, userNo=5181240702000026848 → uat环境
uat_bank_pln_data = {
    "bankPayeeFeeCcy": "PLN",   # 渠道手续费金额 ---
    "channelId": 1200923053,    # ---Banking Circle S.A. - E贸汇
    "payeeAccountNo": "79900202404773",  # ----------收款方账号
    "payeeCcy": "PLN",          # 渠道入账币种
    "payeeType": 3,             # 账号类型 1-gep电商  3-B2B收款
    "remitCcy": "PLN",          # 渠道汇款币种   对应 CHANNEL_REMITTANCE_CCY
    "storeNo": 0,               # 店铺号
    "userNo": 5181240702000026848,  # UAT桐乡市高桥旭木汽车咨询服务部
    "remarks": "我的桐乡-uat-B2B收款账户"
}

# 来自 data: 银行渠道, remitCcy=USD → 可能是美元账户, storeNo=0
uat_bank_php_data = {
    "bankPayeeFeeCcy": "PHP",   # 渠道手续费金额 ---
    "channelId": 1200923079,    # ---------------------------Payso-电商收款-API
    "payeeAccountNo": "P900100110260",  # --------------------------收款方账号
    "payeeCcy": "PHP",          # 渠道入账币种
    "payeeType": 3,             # 账号类型   3-B2B收款
    "remitCcy": "USD",          # 渠道汇款币种   对应 CHANNEL_REMITTANCE_CCY
    "storeNo": 0,               # 店铺号
    "userNo": 5181240702000026848,  # UAT桐乡市高桥旭木汽车咨询服务部
    "remarks": "我的桐乡-uat--b2b收款账户"
}





# 可选：默认配置
DEFAULT_DATA = uat_tx_shop_data