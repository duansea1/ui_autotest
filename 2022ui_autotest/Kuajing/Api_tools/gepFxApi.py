# -*- coding: utf-8 -*-
# ---
# GEP-FX相关接口
# @Time: 2024-12-03 19:35
# ---
from commons.RSAUtil import *
from Kuajing.Common import publicTools
from Kuajing.Common import enviromments as enc
from icecream import ic

# ic.configureOutput(prefix='DEBUG: ')
ic.configureOutput(includeContext=True)


def gep_apply_payment(env):
    """ GEP汇款申请(对应业务：GEP付款-旧版)"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)

    data = {
        "userNo": data_env.get('userNo'),  # 商户号 - 必填
        "certificateId": data_env.get('certificateId'),  # 证书编号 - 必填
        "userReqNo": "sea202412060010",  # 汇款申请单号 - 必填, 字符串长度不超过32
        "paymentMode": "SWIFT",  # 付款模式 - 必填, SWIFT、 LOCAL、 BILLPAY、 BPAY 为空则默认SWIFT，此值需要与添加银行账号选择的付款方式要一致
        "paymentCcy": "USD",  # 付款币种 - 必填 商户开通的出款币种
        "paymentAmount": 1,  # 实际付款的资金，当付款币种和收款币种不一致时，并且固定模式为1时，此字段必须大于0，固定模式为2时此字段填写0
        "payeeCcy": "CNH",  # 实际境外收款的币种
        "payeeAmount": 0,  # 实际境外收款的资金，当付款币种和收款币种不一致时，并且固定模式为1时，此字段必须为0，固定模式为2时此字段必须大于0
        "fixedModel": 1,  # 固定模式：1-固定付款金额，2-固定收款金额
        "paymentPurpose": 13,  # 付款用途：12-供货商 13-物流服务 14-分销推广 15-广告宣传 16-技术服务 17-留学 18-其他
        "paymentReference": 'sea-remarks-b2b',  # 汇款附言，只能是英文付款模式是BPAY的场景时,付款附言必填
        "costBorne": "SHA",  # 费用承担方式：SHA-非全额到账、OUR-全额到账、BEN-收款人承担
        "paymentMaterial": 13469798,  # 通过文件上传接口上传成功之后返回的文件编号
        "cardNo": "622878876256535",  # 已经在GEP平台绑定的帐号--通过接口获取
        "accountName": "CNH acount name",  # 已经在GEP平台绑定的账户名称，其中银行帐号 + 账户名 + 收款到账币种确认一个收款人帐号信息
        "businessNo": "2411181141000000415",  # 收款方主体编号,在添加收款方主体时返回的编号
        "paymentFeeCcy": "CNH",  # 只能是商户开通的账户币种，出款的手续费币种
        "callBackUrl": "121-sea",  # 通知地址 - 必填
        "payerUserNo": 5181240821000008798,  # 出款的商户号，该商户号和代理商号需要在运营平台配置才能传该值T_USER_AGENT_PAYMENT
        "poboPayment": None,  # (是否已用户名义出款，收到入账时付款人名字是商户号对应的名称该字段取值：1-是0-否默认都是否)
        "poboRecordId": None  # 如果poboPayment为1，则需要填写pobo付款人记录编号(新增pobo付款人接口返回的记录编号),不填则为同名POBO付款，默认为当前付款用户号
    }

    ic(data)

    # 开始加密操作
    rsa_utils, dataContent = publicTools.rsa_generate(data, env)

    url = f"{data_env.get('url')}/api/payment/applyPayment"

    # 请求数据
    dataMap = {
        "version": "1.0.0",
        "certificateId": data_env.get('certificateId'),
        "userNo": data_env.get('userNo'),
        "dataType": "JSON",
        "dataContent": dataContent,
        "agentNo": data_env.get('agentNo'),
        "apiType": 1      # 1-代理商  2-商户
    }
    ic(dataMap)

    # 发送请求
    publicTools.send_request(rsa_utils, url, dataMap)

def platform_apply_payment(env):
    """
    GEP电商平台付款API测试（对应业务：gep-提现付款管理-发起付款-选择电商）
    数据从https://fat-member.gepholding.com/api/user/payee-account/queryUserPayeeAccount/6接口获取
    """
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/payment/platform-apply-payment"
    data = {
        "userNo": data_env.get('userNo'),
        "certificateId": data_env.get('certificateId'),
        "userReqNo": "sea202412070009",
        "paymentCcy": "USD",
        "paymentAmount": 1,
        "payeeCcy": "HKD",  # 收款账户币种
        "paymentPurpose": 10,
        "paymentReference": "TRADE TEST",
        "costBorne": "OUR",

        "cardNo": "566978098342",
        "accountName": "HKONG WUWU NET Company .LIT",
        "businessNo": "2412091404000034329",

        "callBackUrl": "m071102",
        "paymentMaterial": 13477752,
        "paymentMaterialName": "wePay.png",
        "paymentStoreList": [
            {
                "paymentAmt": 1,
                "storeNo": 2409061133000000417,
            }
        ],
        "industryType": "01",  # TODO 没有这个参数 UserPaymentOrderServiceImpl|selectAvailableAmtStore
        }

    # 提示：在实际使用时，请确保所有必填项都有提供具体值。
    ic(data)

    # 开始加密操作
    rsa_utils, dataContent = publicTools.rsa_generate(data, env)

    # 构建请求数据
    dataMap = {
        "version": "1.0.0",
        "certificateId": data_env.get('certificateId'),
        "userNo": data_env.get('userNo'),
        "dataType": "JSON",
        "dataContent": dataContent,
        # "agentNo": data_env.get('agentNo'),
        # "apiType": 1    # 1-代理商  2-商户

    }
    ic(dataMap)

    # 发送请求
    publicTools.send_request(rsa_utils, url, dataMap)

def gep_apply_settle(env):
    """
    GEP结汇申请（对应业务：gep-境内结汇申请-选择汇兑账户）"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    data = {
            "userNo": data_env.get('userNo'),
            "certificateId": data_env.get('certificateId'),
            "userReqNo": "sea202412070006",
            "paymentCcy": "EUR",
            "paymentAmount": 1,
            "paymentPurpose": 13,
            # "industryType": 01,
            "paymentFeeCcy": "EUR",  # 只能是商户开通的账户币种，出款的手续费币种
            "paymentMaterial": 13470161,
            "paymentMaterialName": "fat-GEP-结汇货物贸易明细（付款至境内-结汇申请）.xlsx",
            "callBackUrl": "m071102",
            }

    # 提示：在实际使用时，请确保所有必填项都有提供具体值。
    ic(data)

    # 开始加密操作
    rsa_utils, dataContent = publicTools.rsa_generate(data, env)

    url = f"{data_env.get('url')}/api/settle/apply-settle"

    # 构建请求数据
    dataMap = {
        "version": "1.0.0",
        "certificateId": data_env.get('certificateId'),
        "userNo": data_env.get('userNo'),
        "dataType": "JSON",
        "dataContent": dataContent,
        "agentNo": data_env.get('agentNo'),
        "apiType": 1    # 1-代理商  2-商户

    }
    ic(dataMap)

    # 发送请求
    publicTools.send_request(rsa_utils, url, dataMap)

def platform_apply_settle(env):
    """
    6-收款账户结汇（GEP结汇申请-选择收款账户）"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/settle/platform-apply-settle"
    data = {
            "userNo": data_env.get('userNo'),
            "certificateId": data_env.get('certificateId'),
            "userReqNo": "sea-p202412070001",
            "paymentStoreList": [
                {"paymentAmt": "1", "storeNo": "2409061133000000417"}
            ],
            "paymentCcy": "USD",
            "paymentAmount": 1,
            "paymentPurpose": 13,
            "industryType": "01",
            "paymentFeeCcy": "USD",  # 只能是商户开通的账户币种，出款的手续费币种
            "paymentMaterial": 13477959,
            "paymentMaterialName": "fat-GEP-结汇货物贸易明细（付款至境内-结汇申请）.xlsx",
            "callBackUrl": "m071102",
            }

    # 提示：在实际使用时，请确保所有必填项都有提供具体值。
    ic(data)

    # 开始加密操作
    rsa_utils, dataContent = publicTools.rsa_generate(data, env)

    # 构建请求数据
    dataMap = {
        "version": "1.0.0",
        "certificateId": data_env.get('certificateId'),
        "userNo": data_env.get('userNo'),
        "dataType": "JSON",
        "dataContent": dataContent,
        # "agentNo": data_env.get('agentNo'),
        "apiType": 2    # 1-代理商  2-商户

    }
    ic(dataMap)

    # 发送请求
    publicTools.send_request(rsa_utils, url, dataMap)

def apply_unify_settle(env):
    # 商户端看不到，GEP-付款审核可以看到
    """GEP结汇申请"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/settle/apply-unify-settle"

    data = {
        "userNo": data_env.get('userNo'),

        "certificateId": data_env.get('certificateId'),
        "userReqNo": "sea-gep202412070004",
        "payeeType": 1,
        "clearingCode": "308584000013",

        "paymentAmount": 10,
        "cardNo": "6321908192",
        "accountName": "李勇",
        "paymentCcy": "USD",
        "industryType": 12,
        "paymentMaterialName": "GEP-GG-test.xls",
        "paymentPurpose": 10,
        "payeeIdNo": "140221199501117114",
        "paymentFeeCcy": "USD",
        "paymentMaterial": 13478738,
        "callBackUrl": "http://X:8080/notify/receiveNotify/5181240821000008798/2408281533000001302/结汇一体化API",

        "provinceCode": "340000",
        "cityCode": "340500",
        }

    # 提示：在实际使用时，请确保所有必填项都有提供具体值。
    ic(data)
    # 开始加密操作
    rsa_utils, dataContent = publicTools.rsa_generate(data, env)

    # 构建请求数据
    dataMap = {
        "version": "1.0.0",
        "certificateId": data_env.get('certificateId'),
        "userNo": data_env.get('userNo'),
        "dataType": "JSON",
        "dataContent": dataContent,
        # "agentNo": data_env.get('agentNo'),
        "apiType": 2    # 1-代理商  2-商户

    }
    ic(dataMap)

    # 发送请求
    publicTools.send_request(rsa_utils, url, dataMap)

def gep_apply_withdrawal(env):
    """
    GEP提现申请（提现付款管理-发起提现-选择汇兑）
    注意该接口只能体现到用户的同名账户，需要付款到非同名账户时请使用付款申请接口。"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/withdrawal/apply-withdrawal"
    data = {
            "userNo": data_env.get('userNo'),
            "certificateId": data_env.get('certificateId'),
            "userReqNo": "sea-with202412070005",
            "paymentCcy": "EUR",  # 付款币种 - 必填 商户开通的出款币种
            "paymentAmount": 1,  # 实际付款的资金，当付款币种和收款币种不一致时，并且固定模式为1时，此字段必须大于0，固定模式为2时此字段填写0
            "payeeCcy": "CNH",  # 实际境外收款的币种
            "payeeAmount": 0,  # 实际境外收款的资金，当付款币种和收款币种不一致时，并且固定模式为1时，此字段必须为0，固定模式为2时此字段必须大于0
            "fixedModel": 1,  # 固定模式：1-固定付款金额，2-固定收款金额
            "paymentPurpose": 13,  # 付款用途：12-供货商 13-物流服务 14-分销推广 15-广告宣传 16-技术服务 17-留学 18-其他
            "paymentReference": 'sea-remarks-b2b',  # 汇款附言，只能是英文付款模式是BPAY的场景时,付款附言必填
            "costBorne": "SHA",  # 费用承担方式：SHA-非全额到账、OUR-全额到账、BEN-收款人承担

            "cardNo": "5686798743",  # 已经在GEP平台绑定的帐号--通过接口获取 5686798743-fat
            "accountName": "HKONG WUWU NET Company .LIT",  # 已经在GEP平台绑定的账户名称，其中银行帐号 + 账户名 + 收款到账币种确认一个收款人帐号信息
            # "businessNo": "2411181141000000415",  # 收款方主体编号,在添加收款方主体时返回的编号
            "paymentFeeCcy": "CNH",  # 只能是商户开通的账户币种，出款的手续费币种
            "callBackUrl": "121-sea",  # 通知地址 - 必填
            "payerUserNo": data_env.get('userNo')

            }

    # 提示：在实际使用时，请确保所有必填项都有提供具体值。
    ic(data)

    # 开始加密操作
    rsa_utils, dataContent = publicTools.rsa_generate(data, env)

    # 构建请求数据
    dataMap = publicTools.data_Map(data_env, dataContent, apiType=1)

    ic(dataMap)

    # 发送请求
    publicTools.send_request(rsa_utils, url, dataMap)

def gep_platform_apply_withdrawal(env):
    """
    3.8 电商平台提现申请（提现付款管理-发起提现-选择电商）
    商户在文件上传成功之后，可通过此接口进行汇款，在汇款时需把GEP返回的文件批次号上传给GEP系统。"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/withdrawal/platform-apply-withdrawal"
    data = {
            "userNo": data_env.get('userNo'),
            "certificateId": data_env.get('certificateId'),
            "userReqNo": "sea-plat202412070005",
            "paymentCcy": "USD",  # 付款币种 - 必填 商户开通的出款币种
            "paymentAmount": 1,  # 实际付款的资金，当付款币种和收款币种不一致时，并且固定模式为1时，此字段必须大于0，固定模式为2时此字段填写0
            "payeeCcy": "CNH",  # 实际境外收款的币种
            "paymentPurpose": 10,  # 1-往来结算款、2-贷款、3-差旅费
            "paymentReference": 'sea-remarks-b2b',  # 汇款附言，只能是英文付款模式是BPAY的场景时,付款附言必填
            "costBorne": "SHA",  # 费用承担方式：SHA-非全额到账、OUR-全额到账、BEN-收款人承担

            "cardNo": "5686798743",  # 已经在GEP平台绑定的帐号--通过接口获取
            "accountName": "HKONG WUWU NET Company .LIT",  # 已经在GEP平台绑定的账户名称，其中银行帐号 + 账户名 + 收款到账币种确认一个收款人帐号信息

            "callBackUrl": "121-sea",  # 通知地址 - 必填
            "paymentStoreList": [
                {"paymentAmt": 1, "storeNo": 2409061133000000417},
            ],
            "industryType": "01",  # 没有这个参数 UserPaymentOrderServiceImpl|selectAvailableAmtStore


            }

    ic(data)

    # 开始加密操作
    rsa_utils, dataContent = publicTools.rsa_generate(data, env)

    # 构建请求数据
    dataMap = publicTools.data_Map(data_env, dataContent, apiType=None)
    ic(dataMap)

    # 发送请求
    publicTools.send_request(rsa_utils, url, dataMap)


if __name__ == '__main__':

    # B2b 海外付款审核接口-done
    # gep_apply_payment(env="fat-sea-wu")
    # gep_apply_payment(env="fat-sea-agent-hzl")

    # 电商平台付款申请 -done
    # platform_apply_payment(env="fat-sea-wu")

    # GEP结汇申请 -done
    # gep_apply_settle(env="fat-sea-agent-hzl")

    # 6-收款账户结汇 -done
    # platform_apply_settle(env="fat-sea-wu")

    # GEP提现申请 -done
    gep_apply_withdrawal(env="uat-sea-agent-hzl")

    # 4-收款账户用户提现 -done
    # gep_platform_apply_withdrawal(env="fat-sea-wu")

    # GEP结汇申请api -done
    # apply_unify_settle(env="fat-sea-wu")




