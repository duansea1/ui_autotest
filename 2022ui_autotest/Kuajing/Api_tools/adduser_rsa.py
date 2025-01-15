# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-08-22 10:22
# ---

from Common import publicTools as p
from Common import enviromments as enc
from icecream import ic


# ic.configureOutput(prefix='DEBUG: ')
ic.configureOutput(includeContext=True)


def add_user(env, email):
    """新增代理商关联的商户"""
    # 获取秘钥相关信息
    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/user/createUser"

    data = {
        "email": email
    }
    ic(data)
    p.rsa_and_send_request(data, env, url, apiType=1)

if __name__ == '__main__':
    fat_env = "fat-sea-agent-hzl"
    uat_env = "uat-sea-agent-hzl"
    email = "121@111.com"
    """新增商户"""
    add_user(fat_env, email)
