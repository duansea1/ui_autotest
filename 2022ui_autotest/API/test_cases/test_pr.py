# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年9月月04日 14:29
# ---
import pytest
# from API.test_cases.test_shop_login import TestApis
from API.commons.yaml_util import YamlUtil
class Testall():

    # 第一种数据驱动的形式
    @pytest.mark.parametrize("name", ["kobe", "kevin", "sea"])
    def test_api(self, name):
        print("第一条case-名字{0}".format(name))

    @pytest.mark.parametrize("name", YamlUtil().read_apiCommon_yaml("\\get_api_common.yaml"))
    def test_opt(self, name, age=None):
        print("{0}:::第1条opts".format(name))
        assert 1 == 1
        if name == "sea":
            assert age == 89, "断言年龄不符合预期"


if __name__ == "__main__":
    pytest.main(["-vs", "test_pr.py"])

