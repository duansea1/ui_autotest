# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-11-23 16:39
# ---
import os

from Common.RSAUtil import *
from Common import enviromments as enc
from icecream import ic
from datetime import datetime, timedelta
from logging import getLogger, basicConfig, INFO
import json
import requests

from read_files import get_files


def jsonString(data):
    """
    转换 Swift 字典为 JSON 字符串
    data_value = {"email": "121@111.com"}
    """
    return json.dumps(data, separators=(',', ':'))

def send_request(rsa_utils, url, dataMap, **kwargs):
    """Send request"""
    request_params = {
        'url': url,
        'data': dataMap,
        'verify': False  # 不推荐在生产环境中使用
    }

    # Update with any additional keyword arguments
    request_params.update(kwargs)

    # Remove None values to avoid passing them to requests.post
    request_params = {k: v for k, v in request_params.items() if v is not None}

    response = requests.post(**request_params)

    if response.status_code == 200:
        try:
            response_data = response.json()  # 解析JSON响应
            if response_data.get('result'):
                result = response_data.get('result')  # 提取result字段
                logger.info(f"{url}未解密前的响应结果：{response_data}")
                result = rsa_utils.pub_decrypt(result)  # RSA解密
                with open('跨境接口调用成功返回记录表.txt', "a") as f:
                    f.write(f"\n {url}调用成功返回结果：\n {result}")
                logger.info(f"{url}解密结果：{result}")
                ic(result)
                return json.loads(result)
            else:
                logger.info(f"{url}解密result失败结果：{response_data}")
                return None
        except json.JSONDecodeError as e:
            logger.info(f"{url}解析JSON失败：{e}")
            return None
    else:
        logger.info(f"{url}请求失败：{response.text}")
        return None


def rsa_generate(data, env):
    """RAS加密
    @param data: json
    @param env: 环境
    @return rsa_utils: RSA 工具类
    @return dataContent: 加密后的数据
    """
    data_env = enc.get_envs(env)
    rsa_utils = RSAUtil(pfx_path=data_env.get('pfx_path'), pfxpass=data_env.get('pfx_pass'),
                        cer_path=data_env.get('cer_path'))
    dataContent = rsa_utils.pri_encrypt(json.dumps(data))  # RSA加密
    return rsa_utils, dataContent


def data_Map(data_env, dataContent, apiType=None):
    """
    构建数据Map
    @param data_env: 环境变量
    @param dataContent: 加密后的数据
    @param apiType: 1-代理商  2-商户  3-代理商和商户
    @return dataMap: 构建的数据Map
    """
    dataMap = {
        "version": "1.0.0",
        "certificateId": data_env.get('certificateId'),
        "dataType": "JSON",
        "dataContent": dataContent,
        # "userNo": data_env.get('userNo'),
        # "agentNo": data_env.get('agentNo'),
        # "apiType": 1  # 1-代理商  2-商户

    }
    api_type_mapping = {
        1: {'apiType': 1, 'agentNo': data_env.get('agentNo')},
        2: {'apiType': 2, 'userNo': data_env.get('userNo')},
        3: {'apiType': 1, 'userNo': data_env.get('userNo'), 'agentNo': data_env.get('agentNo')}
    }
    if apiType in api_type_mapping:
        dataMap.update(api_type_mapping[apiType])
    return dataMap


def generate_dates(day_offset=0):
    """
    根据传入的 day_offset 参数，生成当天、明天或后天的日期，格式为 YYYY-MM-DD。

    :param day_offset: 整数，表示相对于今天的偏移量。0 表示今天，1 表示明天，2 表示后天，依此类推。
    :return: 字符串，格式为 YYYY-MM-DD
    """
    # 获取当前日期
    today = datetime.now().date()

    # 根据偏移量计算目标日期
    target_date = today + timedelta(days=day_offset)

    # 返回格式化后的日期字符串
    return target_date.strftime('%Y-%m-%d')


def rsa_and_send_request(data, env, url, apiType=3, **kwargs):
    """
    获取加密数据、加密+发送请求+解密
    :param data:
    :param env:
    :param url:
    :param apiType:3 -默认代理商和商户号全传
    :param **kwargs: request.post的动态参数
    :return:
    """
    # 获取代理商or商家的配置信息
    data_env = enc.get_envs(env)

    rsa_utils, dataContent = rsa_generate(data, env)

    # 构建请求数据
    dataMap = data_Map(data_env, dataContent, apiType)
    logger.info(f"请求数据参数：{dataMap}\n")

    # 发送请求
    result = send_request(rsa_utils, url, dataMap, **kwargs)

    return result


def calculate_md5(file_path, chunk_size=8192):
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                md5.update(chunk)

        # Convert each byte to a two-character hex string, similar to Java's String.format("%02x", b & 0xff)
        hex_string = ''.join(f'{byte:02x}' for byte in md5.digest())
        ic(hex_string)
        return hex_string
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

def get_file_info(filename):
    """返回文件名称和md5加密数据"""
    file_path = get_files("OtherFiles", filename)
    logger.info(f"文件地址{file_path}")
    file_name = os.path.basename(file_path)
    md5_encryption = calculate_md5(file_path)
    return file_name, file_path, md5_encryption

if __name__ == '__main__':
    pass
    # calculate_md5(r"C:\Users\段海洋\BF_javafiles\kuajing_javas\baofu-test-core\file\fileUpload\wePay.png")
