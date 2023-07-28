# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年9月月13日 20:49
# ---

from API.commons.yaml_util import YamlUtil
import os
file = os.getcwd() + "\pr_yaml.yaml"
print(file)
res = YamlUtil().read_apiCommon_yaml(yaml_path="\pr_yaml.yaml")

print(res)
