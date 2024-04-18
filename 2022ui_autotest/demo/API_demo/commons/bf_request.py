# -- coding: utf-8 --
# @time :
# @author : xxxx
# @file : .py
# @desp : 统一封装、统计用例数、日志监控、发送请求的代码很相似

import requests
import urllib3
urllib3.disable_warnings()   # 解决请求提示InsecureRequestWarning（不安全请求警告）的log

def request_bf_del_account(loginNo, usertype):
    """
    调宝付接口，删除测试环境的宝户账号
    :param loginNo: 登录号
    :param usertype: MERCHANT -对公企业
    :return:{'msg': '企业二级账户不存', 'code': 500}
    {
    "msg": "删除成功",
    "code": 0,
    "UserInfo": {
        "customerNo": "5198000459301528",
        "customerType": "MERCHANT",
        "loginNo": "0TvaSAL4QmDX"
    }
}
    """
    bf_url = "https://sp.baofoo.com/support-admin/mer/follow/del/logino?logino="+loginNo + "&usertype=" + usertype
    get_re = requests.get(url=bf_url, verify=False)
    if get_re.json()['code'] == 0:
        return True  # 删除成功
    return False    # 删除失败

def request_bct_del_account(openNo):
    """
    调宝财通接口，删除测试环境的宝户账号

    """
    bcf_url = f"https://sp.baofoo.com/support-admin/tools/bct/del?contract_no={openNo}"
    get_re = requests.get(url=bcf_url, verify=False)
    if get_re.json()['code'] == 0:
        return True  # 删除成功
    return False    # 删除失败

class RequestUtil:
    sess = requests.session()

    @staticmethod
    def all_send_request(method, url, **kwargs):
        """封装接口请求方法"""
        print("----------------------------")
        res = RequestUtil.sess.request(method, url, **kwargs)
        return res


if __name__ == "__main__":
    bf = request_bf_del_account(loginNo='123',usertype='MERCHANT')
    print(bf)
