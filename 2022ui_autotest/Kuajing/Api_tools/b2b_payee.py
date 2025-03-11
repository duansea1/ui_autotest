# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2025-2-26 10:00
# ---

from Common import publicTools as p
from Common import enviromments as enc
from icecream import ic

from Api_tools import uploadFile


def b2b_apply_payment(env):
    """B2B汇款申请
    [业务场景：：：B2b海外付款订单]
    """
    # 获取秘钥相关信息

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/payment/b2b/apply-payment"


    # fat环境 五五商户的海外付款账户
    account_data ={
        "accType": 2,
        "accountCcy": "CNH",
        "accountName": "chins_sea",
        "bankCode": "",
        "bankName": "中国银行",
        "businessNo": "2410162050000001016",
        "cardNo": "465876536475",
        "countryCode": "CHN",
        "middleSwiftCode": "",
        "payeeAddress": "shanghai",
        "paymentChannelType": "SWIFT",
        "paymentDesc": "SWIFT",
        "recordNo": "2410162050000007725",
        "swiftCode": "BKCHCNBJ",
        "userNo": "5181240821000008798"
    }

    data = {
        "userNo": data_env.get('userNo'),  # 商户在GEP系统开通的唯一商户编号
        "certificateId": data_env.get('certificateId'),  # GEP提供给商户的证书编号
        "userReqNo": "2025020136-0005",  # 商户请求GEP系统的申请订单号，保证此单号唯一
        "paymentMode": "SWIFT",  # 付款模式，默认为SWIFT，可选值：SWIFT、LOCAL、BILLPAY、BPAY
        "paymentCcy": "EUR",  # 示例：商户开通的出款币种
        "paymentAmount": 2,  # 示例：实际付款的资金
        "payeeCcy": account_data.get("accountCcy"),  # 示例：实际境外收款的币种
        "fixedModel": 1,  # 固定模式：1-固定付款金额，2-固定收款金额
        "paymentPurpose": 12,  # 示例：付款用途，12-供货商
        "costBorne": "SHA",  # 示例：费用承担方式，SHA-非全额到账
        "paymentMaterial": 13614407,  # 示例：通过文件上传接口返回的文件编号
        "cardNo": account_data.get("cardNo"),  # 示例：已经在GEP平台绑定的帐号
        "accountName": account_data.get("accountName"),  # 示例：已经在GEP平台绑定的账户名称
        "businessNo": account_data.get("businessNo"),  # 示例：收款方主体编号
        "paymentFeeCcy": "CNH",  # 示例：只能是商户开通的账户币种
        # "callBackUrl": "https://example.com/callback",  # 示例：商户侧的请求地址
        # "poboPayment": 0,  # 示例：是否以用户名义出款，0-否
        # "poboRecordId": None  # 示例：如果poboPayment为1，则需要填写pobo付款人记录编号
    }
    ic(data)
    p.rsa_and_send_request(data, env, url, apiType=3)


def b2bSettleApply(env):
    """2.3.17 结汇付款申请"""
    # 获取秘钥相关信息

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/settle/b2bSettleApply"

    data = {
        "userNo": data_env.get('userNo'),  # 商户在GEP系统开通的唯一商户编号
        "userReqNo": "2025020136-0002",  # 商户请求GEP系统的申请订单号，保证此单号唯一
        "paymentCcy": "USD",  # 付款币种，详见附件币种列表（必填）
        "payeeCcy": "CNY",  # 收款币种，默认为CNY（必填）
        "fixedModel": 1,  # 固定模式：1-固定付款金额，2-固定收款金额（必填）
        "tradeAmount": 5.0,  # 交易金额，不能小于等于0（必填）
        "autoPayment": 1,  # 是否出款，默认1-自动出款（必填）
        "payeeAccountId": "2412101410000001246",  # 收款人银行账户编号，通过收款人查询接口获取（必填）  # 2410162100000007727---五五公司的 2407032010000002676-桐乡  2412101410000001246-丝丝uat
        "transferRemarks": "",  # 交易附言，最多64个字符（可选）
        # "callBackUrl": "",  # 处理结果回调地址，最多100个字符（可选）
        "fastPayment": 1  # 极速付款标识：1-普通付款，2-极速出款，默认为普通付款（可选）
    }
    ic(data)
    p.rsa_and_send_request(data, env, url, apiType=1)


def b2b_submit_Order(env):
    """2.3.12 结汇订单文件提交"""
    # 获取秘钥相关信息

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/declarationOrder/submitOrder"

    # updload_data = uploadFile.upload_file(env, filename='B2B收款材料上传明细模板-未发货.xls')
    data = {
        "userNo": data_env.get('userNo'),  # 商户在GEP系统开通的唯一商户编号
        "userReqNo": "20250226000019",  # 用户请求单号，保证此单号唯一（必填）
        "fileId": 13614494,  # 订单文件ID，上传文件接口返回的id，fileType为STORE_ORDER_FILE（必填）
        "fileName": "B2B收款材料上传明细模板-未发货.xls",  # 上传文件的名称，包含后缀，最多64个字符（必填）
        "voucherFileId": "13614450",  # 证明文件ID，上传文件接口返回的id，fileType为B2B_OPEN_ACC_FILE（必填）
        "fileType": 2,  # 文件类型，默认为2（必填）
        # "callBackUrl": "",  # 处理结果回调地址，最多100个字符（可选）
        "buyerName": "sea-wuwu"  # 买家名称，最多30个字符（必填）
    }
    ic(data)
    p.rsa_and_send_request(data, env, url, apiType=1)


def b2b_addPayee(env):
    """2.3.9 新增结汇收款人"""
    # 获取秘钥相关信息

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/payee/addPayee"



    data = {
        "userNo": data_env.get('userNo'),  # 用户编号，GEP分配的用户号（必填）
        "partnerType": 2,  # 合作收款人类型，2-本企业，5-第三方个人，6-第三方企业（必填）
        "nameType": "3",  # 干系人类型，当收款人类型为本企业时，必填；1-本企业，2-本企业的法人，3-本企业的受益人（条件必填）
        "name": "香港企业李勇",  # 收款人名称，结汇出款到银行账户或卡号的名称（必填）
        "orgCode": "",  # 组织机构号，当收款人类型为第三方企业时，必填（条件必填）
        "industryId": "",  # 行业属性，当收款人类型为第三方企业时，必填（条件必填）
        "economyId": "",  # 经济属性，当收款人类型为第三方企业时，必填（条件必填）
        "taxfreeCode": "",  # 经济特区，当收款人类型为第三方企业且是特殊经济区时，必填（条件必填）
        "linkMan": "",  # 联系人，当收款人类型为第三方企业时，必填（条件必填）
        "linkMobile": "",  # 联系人电话，当收款人类型为第三方企业时，必填（条件必填）
        "postCode": "",  # 邮编，当收款人类型为第三方企业时，必填（条件必填）
        "legalName": "",  # 法人名称，当收款人类型为第三方企业时，必填（条件必填）
        "legalIdNo": "140221199501117122",  # 证件号码，第三方个人时为收款人的身份证号码，第三方企业时为法人的身份证号码（条件必填）
        "province": "",  # 省份代码，当收款人类型为第三方企业时，必填（条件必填），格式：code_name 如：210000_辽宁省
        "city": "",  # 城市代码，当收款人类型为第三方企业时，必填（条件必填），格式：code_name 如：210200_大连市
        "area": "",  # 区县代码，当收款人类型为第三方企业时，必填（条件必填），格式：code_name 如：210202_中山区
        "address": "",  # 详细地址，当收款人类型为第三方企业时，必填（条件必填）
        "bankName": "招商永隆银行有限公司深圳分行",  # 结汇出款到账的银行名称（必填）
        "cardNo": "1325455765",  # 结汇出款到账的境内银行账号（对公）或卡号（对私）（必填）
        "bankBranchName": "招商永分行",  # 收款人开户行的支行名称（必填）
        "bankProvince": "210000_辽宁省",  # 收款人开户行的省份，格式：code_name 如：210000_辽宁省（必填）
        "bankCity": "210200_大连市",  # 收款人开户行的城市，格式：code_name 如：210200_大连市（必填）
        "bankAddress": "上海市浦东新区",  # 收款人开户行的详细地址（必填）
        "bankNameOfLegal": "",  # 添加法人到账银行名称，当收款人类型为第三方企业时可为空（条件选填）
        "cardNoOfLegal": "",  # 添加法人境内到账银行卡号，当收款人类型为第三方企业时可为空（条件选填）
        "bankLegalProvince": "",  # 法人到账银行的省份，当法人到账银行名称不为空时必填，格式：code_name 如：210000_辽宁省（条件必填）
        "bankLegalCity": "",  # 法人到账银行的城市，当法人到账银行名称不为空时必填，格式：code_name 如：210200_大连市（条件必填）
        "accountDocument": 0,  # 证明文件id，当收款人类型为第三方企业、第三方个人时，必填（条件必填）
        "callBackUrl": "",  # 处理结果回调地址（可选）
        "userReqNo": "346567685555"  # 用户请求单号，如为空则GEP自动赋值UUID（可选）
    }

    ic(data)
    p.rsa_and_send_request(data, env, url, apiType=1)

def b2b_applySubAcc(env):
    """2.3.7 子账户开户【B2b收款账户开通】"""
    # 获取秘钥相关信息

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/subAcc/applySubAcc"

    data = {
        "userNo": data_env.get('userNo'),  # 用户编号，GEP分配的用户号（必填）
        "accountPayeeType": 2,  # 账户收款类型：1-全球收款，2-本地收款，不传默认为1（必填）
        "country": "IDN",  # 账号区域，accountPayeeType为1时账户区域为HKG、SGP；accountPayeeType为2时账户区域为NZL, CAN, USA等，不传默认HKG（必填）
        "bankCode": 32,
        # 账户开户行，accountPayeeType为1时必填：1-DBS Bank (Hong Kong) Limited，2-J.P.morgan等，不传默认为1（必填，条件依赖accountPayeeType）
        "bankAccName": "HKONG WUWU NET Company .LIT",  # 银行账户名称，当accountPayeeType为2且country为KOR时必填，字符最大长度为10个字符（条件必填）
        "webUrl": "api11.com",  # 用户使用平台网址（必填）
        "goodsType": "020",  # 贸易商品大类，详见附件（必填）
        "goodsArea": "ALB",  # 贸易国家或地区，详见附件（必填）
        "goodsTradeType": "1",  # 贸易类型，详见附件（必填）
        "goodsFileNo": 0,  # 商品大类资质文件id，当goodsType为016、018、019时必传（条件必填）
        # "callBackUrl": "",  # 处理结果回调地址（可选）
        "exceptYearSalesAmount": 1,  # 预计月销售额：1-月交易量10万美元以下；2-月交易量10万（含）-30万美元；3-月交易量30万（含）-50万美元；4-月交易量50万（含）美元以上（必填）
        "platformType": "Self built station"  # 经营平台，参见附录经营平台列表（必填）
    }
    ic(data)
    p.rsa_and_send_request(data, env, url, apiType=1)



if __name__ == '__main__':
    """
    fat:代理商 fat-sea-agent-hzl
    uat:代理商 uat-sea-agent-hzl
    prod: 代理商 prod-sea-agent-dhf

    """
    fat_env = "fat-sea-agent-hzl"
    uat_env = "uat-sea-agent-hzl"
    # prod_env = "prod-sea-agent-dhf"
    # 代理商
    # query_rate(env=fat_env)

    # 海外付款场景
    # b2b_apply_payment(env="fat-sea-agent-hzl")
    # 结汇付款
    b2bSettleApply(env=uat_env)
    # b2bSettleApply(env="fat-sea-tx")
    # b2b_submit_Order(env="fat-sea-agent-hzl")

    # 新增收款人
    # b2b_addPayee(env="fat-sea-agent-hzl")
    # b2b账户开通
    # b2b_applySubAcc(env="uat-sea-agent-hzl")