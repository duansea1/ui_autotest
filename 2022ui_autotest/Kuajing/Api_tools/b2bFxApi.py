# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-12-03 19:35
# ---
from commons.RSAUtil import *
import requests
import json
from Kuajing.Common import publicTools
from Kuajing.Common import enviromments as enc
from icecream import ic
# ic.configureOutput(prefix='DEBUG: ')
ic.configureOutput(includeContext=True)

def b2b_apply_payment(env):
    """ B2B汇款申请"""
    # 获取秘钥相关信息
    dataenv = enc.get_envs(env)
    pfxpath = dataenv.get('pfxpath')
    pfxpass = dataenv.get('pfx_pass')
    cerpath = dataenv.get('cerpath')
    agentNo = dataenv.get('agentNo')
    base_url = dataenv.get('url')
    certificateId = dataenv.get('certificateId')

    data = {
        "userNo": dataenv.get('userNo'),  # 商户号 - 必填
        "certificateId": None,  # 证书编号 - 必填
        "userReqNo": "",  # 汇款申请单号 - 必填, 字符串长度不超过32
        "paymentMode": "",  # 付款模式 - 必填, 字符串长度不超过32
        "paymentCcy": "",  # 付款币种 - 必填, 字符串长度为3
        "paymentAmount": None,  # 付款金额 - 必填
        "payeeCcy": "",  # 收款到账币种 - 必填, 字符串长度为3
        "payeeAmount": None,  # 收款到账金额 - 必填
        "fixedModel": None,  # 固定模式 - 必填
        "paymentPurpose": None,  # 付款用途 - 必填
        "paymentReference": None,  # 付款附言 - 可选, 字符串长度不超过128
        "costBorne": "",  # 费用承担方式 - 必填, 字符串长度为3
        "paymentMaterial": None,  # 付款材料文件ID - 必填
        "cardNo": "",  # 银行账号 - 必填, 字符串长度不超过128
        "accountName": "",  # 账户名称 - 必填, 字符串长度不超过128
        "businessNo": "",  # 收款方主体编号 - 必填, 字符串长度为19
        "paymentFeeCcy": "",  # 付款手续费币种 - 必填, 字符串长度为3
        "callBackUrl": "",  # 通知地址 - 必填
        "poboPayment": None,  # 是否以用户名义出款 - 可选
        "poboRecordId": None  # pobo的记录编号 - 可选
    }

    # 提示：在实际使用时，请确保所有必填项都有提供具体值。
    ic(data)
    # 开始加密操作
    json_str = publicTools.jsonString(data)  # JSON 格式的字符串
    rsa_util = RSAUtil(pfx_path=pfxpath, pfxpass=pfxpass, cer_path=cerpath)
    dataContent = rsa_util.pri_encrypt(json_str)  # RSA加密

    url = f"{base_url}/api/payment/b2b/apply-payment"

    # 构建请求数据
    dataMap = {
        "version": "1.0.0",
        "certificateId": certificateId,
        "userNo": dataenv.get('userNo'),
        "dataType": "JSON",
        "dataContent": dataContent,
        # "agentNo": agentNo,
        "apiType": 2       #
        # 1-代理商  2-商户
    }
    ic(dataMap)
    # 定义请求头
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # 发送HTTP POST请求
    response = requests.post(url=url, data=dataMap, headers=headers, verify=False)

    if response.status_code == 200:
        try:
            response_data = response.json()  # 解析JSON响应
            if response_data.get('result'):
                result = response_data.get('result')  # 提取result字段
                print("响应结果：", response_data)
                # print("提取的result字段：", result)
                result = rsa_util.pub_decrypt(result)  # RSA加密
                ic(result)
                return result
            else:
                ic(response_data)
                return response_data
        except json.JSONDecodeError as e:
            print(f"解析JSON失败：{e}")
            return None
    else:
        print(f"请求失败：{response.text}")
        return None
