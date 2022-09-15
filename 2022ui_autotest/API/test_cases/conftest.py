# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年9月月04日 16:41
# ---
import pytest
import os
from API.commons.yaml_util import YamlUtil


@pytest.fixture(scope="module", autouse=False)
def excute_sqlw():
    print("--sql****--------------------执行sql查询")
    YamlUtil().clean_yaml()
    yield
    print("--1111111111----关闭数据库连接-清空yaml")
    # clean_yaml()

