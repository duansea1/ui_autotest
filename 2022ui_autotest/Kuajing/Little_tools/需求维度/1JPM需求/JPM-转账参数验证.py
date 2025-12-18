"""
@Author    : duansea
@Date      : 2025/7/9 10:12
@Description: [文件功能的简要描述]
"""


def print_transaction_details(transaction_data):
    # 获取PmtInf列表中的第一个元素（假设只有一个支付信息）
    pmt_inf = transaction_data['Document']['CstmrCdtTrfInitn']['PmtInf'][0]

    # 获取出款账户信息
    dbtr_acct_id = pmt_inf['DbtrAcct']['Id']['Othr']['Id']

    # 获取入账账户信息
    cdtr_acct_id = pmt_inf['CdtTrfTxInf'][0]['CdtrAcct']['Id']['Othr']['Id']

    # 获取金额和币种信息
    amount_details = pmt_inf['CdtTrfTxInf'][0]['Amt']['InstdAmt']
    amount = amount_details['Amount']
    currency = amount_details['Ccy']

    # 打印所需的信息
    print(f"出款账户{dbtr_acct_id}，出款金额{amount}，出款币种{currency}")
    print(f"入账账户{cdtr_acct_id}，金额{amount}，币种{currency}")


# 示例调用
transaction_data = {
    "Document": {
        "CstmrCdtTrfInitn": {
            "GrpHdr": {
                "CreDtTm": "2025-07-09T10:02:07.938Z",
                "MsgId": "2507091002682414407"
            },
            "PmtInf": [
                {
                    "CdtTrfTxInf": [
                        {
                            "Amt": {
                                "InstdAmt": {
                                    "Amount": 0.01,
                                    "Ccy": "USD"
                                }
                            },
                            "CdtrAcct": {
                                "Id": {
                                    "Othr": {
                                        "Id": "1314000010"
                                    }
                                }
                            },
                            "CdtrAgt": {
                                "FinInstnId": {
                                    "BICFI": "CHASHKHH"
                                }
                            },
                            "PmtId": {
                                "EndToEndId": "2507091002682414407"
                            },
                            "RmtInf": {
                                "Ustrd": ["Withdraw Transaction"]
                            }
                        }
                    ],
                    "DbtrAcct": {
                        "Id": {
                            "Othr": {
                                "Id": "3140000011"
                            }
                        }
                    },
                    "DbtrAgt": {
                        "FinInstnId": {
                            "BICFI": "CHASUS33MCY"
                        }
                    },
                    "ReqdExctnDt": "2025-07-09"
                }
            ]
        }
    }
}

print_transaction_details(transaction_data)