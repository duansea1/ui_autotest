# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-12-25 16:18
# ---
import json
import os

import requests
from loguru import logger

from Common import publicTools as p
from Common import enviromments as enc
from icecream import ic

from Common.read_files import *
# ic.configureOutput(prefix='DEBUG: ')
ic.configureOutput(includeContext=True)


def upload_file(env, name='wePay.png'):
    """HTTP文件上传接口"""
    # 获取秘钥相关信息
    filename = get_files("OtherFiles", name)
    ic(filename)
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/common/file/upload-file"
    file_name, file_path, md5_encryption = p.get_file_info(name)
    data = {
        "userNo": data_env.get('userNo'),
        "fileName": file_name,  # 文件名称
        "fileMd5encryption": md5_encryption,  # 文件Md5加密
        "fileType": "STORE_ORDER_FILE",  # 付款证明文件 B2B_OPEN_ACC_FILE  \STORE_ORDER_FILE--订单文件
    }
    ic(data)

    # # 开始加密操作
    # rsa_utils, dataContent = p.rsa_generate(data, env)
    #
    # # 构建请求数据
    # dataMap = p.data_Map(data_env, dataContent, apiType=3)

    file = {'file': (filename, open(file_path, 'rb'))}
    ic(file)
    result = p.rsa_and_send_request(data, env, url, apiType=3, files=file)
    if result:
        try:
            logger.info(f"上传成功的文件id：{result.get('fileId')}")
            return result.get('fileId')
        except json.JSONDecodeError:
            logger.info(f"JSON 解析出错: {result.text}")
            return None
    else:
        logger.info(f"HTTP 状态码: {result.status_code}, 错误信息: {result.text}")
        return None

if __name__ == '__main__':
    fat_env = "fat-sea-agent-hzl"
    uat_env = "uat-sea-agent-hzl"
    upload_file(fat_env, name='B2B收款材料上传明细模板-未发货.xls')
