# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-11-21 19:38
# ---
# from read_files import *
from Kuajing.Common.read_files import *
def get_envs(env):
    if env == 'fat-sea-agent-hzl':  # 海之蓝代理商
        base_env = {
            "pfx_path": get_files("FatAgentFiles", "key_5182240909000002158@@2409101910000000504.pfx"),
            "cer_path": get_files("FatAgentFiles", "key_5182240909000002158@@2409101910000000504.cer"),
            "pfx_pass": "5182240909000002158_882745",
            "userNo": "5181240821000008798",  # 香港五五企业公司
            "agentNo": "5182240909000002158",
            "certificateId": "2409101910000000504",
            # "certificateId": "2408281533000001302",   # 海之蓝的
            "url": "http://10.254.95.181:8061"
        }
        return base_env
    elif env == 'fat-sea-wu':  # 香港五五
        base_env = {
            "pfx_path": get_files("FatTenantFiles", "key_5181240821000008798@@2408281533000001302.pfx"),
            "cer_path": get_files("FatTenantFiles", "key_5181240821000008798@@2408281533000001302.cer"),
            "pfx_pass": "5181240821000008798_774480",
            "agentNo": "5182240909000002158",  # 海之蓝代理商
            "userNo": "5181240821000008798",  # 香港五五企业公司
            "certificateId": "2408281533000001302",
            "url": "http://10.254.95.181:8061"
        }
        return base_env
    elif env == 'fat-sea-tx':  # 桐乡
        base_env = {
            "pfx_path": get_files("FatTenantFiles", "key_5181240628000024148@@2412041416000002198.pfx"),
            "cer_path": get_files("FatTenantFiles", "key_5181240628000024148@@2412041416000002198.cer"),
            "pfx_pass": "5181240628000024148_658379",
            # "agentNo": "5182240909000002158",  # 无代理商
            "userNo": "5181240628000024148",  # 桐乡
            "certificateId": "2412041416000002198",
            "url": "http://10.254.95.181:8061"
        }
        return base_env
    elif env == 'uat-sea-ss':  # 其他企业丝丝
        base_env = {
            "pfx_path": get_files("UatTenantFiles", "key_5181240829000137108@@2408291525000006449.pfx"),
            "cer_path": get_files("UatTenantFiles", "key_5181240829000137108@@2408291525000006449.cer"),
            "pfx_pass": "5181240829000137108_417161",
            # "agentNo": "5182240808000102058",  # uat海之蓝金牌销售
            "userNo": "5181240829000137108",  # 丝丝
            "certificateId": "2408291525000006449",
            "url": "http://10.254.154.99:8061"
        }
        return base_env
    else:
        return None


if __name__ == '__main__':
    get_envs = get_envs('fat-sea-agent-hzl')
    print(get_envs)
