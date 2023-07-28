# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年9月月04日 16:57
# ---
import os
import yaml

#读  写、 清空


class YamlUtil():
    # 读
    def read_yaml(self, key=None):
        with open(os.getcwd()+"\extract.yaml", encoding="utf-8") as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            if key:
                yaml.safe_load()
                print(value[key])
            else:
                print(value)
            return value

    def write_yaml(self, data):
        """写入"""
        with open(os.getcwd()+"\extract.yaml", encoding="utf-8", mode="a") as f:
            yaml.dump(data, stream=f)

    def clean_yaml(self):
        """清空"""
        with open(os.getcwd()+"\extract.yaml", encoding="utf-8", mode="w") as f:
            f.truncate()

    def read_apiCommon_yaml(self, yaml_path):
        with open(os.getcwd() + yaml_path, encoding="gbk") as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            # print(value)
            return value


if __name__ == "__main__":

    dic = {"key":"yaoshi"}
    YamlUtil().write_yaml(dic)
    YamlUtil().read_yaml()