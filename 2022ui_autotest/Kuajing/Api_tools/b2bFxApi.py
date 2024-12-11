# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-12-03 19:35
# ---
from commons.RSAUtil import *
from Kuajing.Common import publicTools
from Kuajing.Common import enviromments as enc
from icecream import ic
import requests
import json
# ic.configureOutput(prefix='DEBUG: ')
ic.configureOutput(includeContext=True)


def b2b_apply_payment(env):
    """ B2B汇款申请(海外付款)"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)

    data = {
        "userNo": data_env.get('userNo'),  # 商户号 - 必填
        "certificateId": data_env.get('certificateId'),  # 证书编号 - 必填
        "userReqNo": "sea202412060005",  # 汇款申请单号 - 必填, 字符串长度不超过32
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
        "cardNo": "465876536475",  # 已经在GEP平台绑定的帐号
        "accountName": "chins_sea",  # 已经在GEP平台绑定的账户名称，其中银行帐号 + 账户名 + 收款到账币种确认一个收款人帐号信息
        "businessNo": "2410162050000001016",  # 收款方主体编号,在添加收款方主体时返回的编号
        "paymentFeeCcy": "CNH",  # 只能是商户开通的账户币种，出款的手续费币种
        "callBackUrl": "121-sea",  # 通知地址 - 必填
        "poboPayment": None,  # (是否已用户名义出款，收到入账时付款人名字是商户号对应的名称该字段取值：1-是0-否默认都是否)
        "poboRecordId": None  # 如果poboPayment为1，则需要填写pobo付款人记录编号(新增pobo付款人接口返回的记录编号),不填则为同名POBO付款，默认为当前付款用户号
    }

    # 提示：在实际使用时，请确保所有必填项都有提供具体值。
    ic(data)

    # 开始加密操作
    rsa_utils, dataContent = publicTools.rsa_generate(data, env)

    url = f"{data_env.get('url')}/api/payment/b2b/apply-payment"

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

def b2b_apply_payment2(env,userReqNo):
    """ B2B汇款申请(海外付款)"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/payment/b2b/apply-payment"

    data = {
        "userNo": data_env.get('userNo'),  # 商户号 - 必填
        "certificateId": data_env.get('certificateId'),  # 证书编号 - 必填
        "userReqNo": userReqNo,  # 汇款申请单号 - 必填, 字符串长度不超过32
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
        "cardNo": "35759780",  # 已经在GEP平台绑定的帐号
        "accountName": "sisi",  # 已经在GEP平台绑定的账户名称，其中银行帐号 + 账户名 + 收款到账币种确认一个收款人帐号信息
        "businessNo": "2411051800002003919",  # 收款方主体编号,在添加收款方主体时返回的编号
        "paymentFeeCcy": "CNH",  # 只能是商户开通的账户币种，出款的手续费币种
        "callBackUrl": "121-sea",  # 通知地址 - 必填
        "poboPayment": None,  # (是否已用户名义出款，收到入账时付款人名字是商户号对应的名称该字段取值：1-是0-否默认都是否)
        "poboRecordId": None  # 如果poboPayment为1，则需要填写pobo付款人记录编号(新增pobo付款人接口返回的记录编号),不填则为同名POBO付款，默认为当前付款用户号
    }
    ic(data)

    # 开始加密操作
    rsa_utils, dataContent = publicTools.rsa_generate(data, env)

    # 构建请求数据
    dataMap = publicTools.data_Map(data_env, dataContent, apiType=3)
    ic(dataMap)

    # 发送请求
    publicTools.send_request(rsa_utils, url, dataMap)

if __name__ == '__main__':
    # B2b 海外付款审核接口
    userReqNo = "sea20241210001"
    # b2b_apply_payment(env="fat-sea-wu")

    # uat-环境的数据
    b2b_apply_payment2(env="uat-sea-agent-hzl", userReqNo=userReqNo)
