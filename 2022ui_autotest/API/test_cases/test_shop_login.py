# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年9月月04日 13:35
# ---
# import pytest
import pytest
import requests
import json
from API.commons.request import RequestUtil
from API.commons.MyEncoder import MyEncoder
from API.commons.yaml_util import YamlUtil
import time


class TestApis():
    sessions = "sessionXXXXXXXCCCCCC"

    def setup(self):
        print("前置操作")
        print("前置操作第2步")

    def teardown(self):
        print("每个用例执行之后的操作")

    def setup_class(self):
        print("每个类----前置操作")
        print("每个类---前置操作第2步")

    def teardown_class(self):
        print("-之后--每个类---执行之后的操作")

    # @pytest.fixture(scope="function", autouse=False)
    # def excute_sql(self):
    #     print("---2222-------------------执行sql查询")


    @pytest.mark.smoke
    def test_keyia_login(self, mobile="13166210872", password="duan2324", *args):
        """商家后台登录"""
        url = "http://api-test.shop.keyid.cn/platform/auth/login"
        header = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Connection": "keep-alive"
        }
        parms = {
            "mobile": mobile,
            "password": password
        }
        # res = requests.post(url=url, json=parms, headers=header, verify=True)
        # print(res.json())

    @pytest.mark.smoke
    def test_login2(self, excute_sqlw,  mobile="13166210872", password="duan2324"):
        """商家后台登录"""
        print("传入的参数:%s" % excute_sqlw)
        url = "http://api-test.shop.keyid.cn/platform/auth/login"
        header = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Connection": "keep-alive"
        }
        parms = {
            "mobile": mobile,
            "password": password
        }
        # res = requests.post(url=url, json=parms, headers=header, verify=True)
        # print(res.json())
        print("第2条case")
        name_logo = "NBAqiaodan"+str(time.time())[-4:]
        dic = {"logo": name_logo}
        # YamlUtil().clean_yaml()
        YamlUtil().write_yaml(dic)
        print("------写入yaml完成")

    @pytest.mark.yaml
    @pytest.mark.parametrize("login_args", YamlUtil().read_apiCommon_yaml("\\get_api_common.yaml"))
    def test_login_from_yaml(self, excute_sqlw, login_args):
        """商家后台登录"""
        print("传入的参数:%s" % excute_sqlw)
        url = "http://api-test.shop.keyid.cn/platform/auth/login"
        header = login_args["request"]["headers"]
        parms = login_args["request"]["params"]
        url = login_args["request"]["url"]
        res = requests.post(url=url, json=parms, headers=header, verify=True)
        print(res.json())
        # name_logo = "NBAqiaodan" + str(time.time())[-4:]
        # dic = {"logo": name_logo}
        # # YamlUtil().clean_yaml()
        # YamlUtil().write_yaml(dic)
        # print("------写入yaml完成")

    @pytest.mark.smoke
    def test_read(self):
        print("读取yaml中的logo：::::" + str(YamlUtil().read_yaml('logo')))


if __name__ == "__main__":
    pytest.main(["-vs", "-m yaml"])

