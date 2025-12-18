"""
@Author    : duansea
@Date      : 2025/7/25 16:31
@Description: [文件功能的简要描述]
"""
from Common import publicTools as p
from Common import enviromments as enc
from icecream import ic
import time
from threading import Thread
from datetime import datetime


# ic.configureOutput(prefix='DEBUG: ')
ic.configureOutput(includeContext=True)


def query_rate(env):
    """查询汇率-默认查的是biz_type=1的"""
    # 获取秘钥相关信息

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/rate/query-rate"

    data = {
        "userNo": data_env.get('userNo'),
        "originalCcy": "CNH",  # 买入
        "targetCcy": "USD",  # 卖出币种
        "closingDate": p.generate_dates()
    }
    # ic(data)
    p.rsa_and_send_request(data, env, url, apiType=3)



def b2b_query_rate(env):
    """此汇率查询接口是按照固定币种对方向返回汇率，币种对方向一致时返回卖出价，币种对方向相反则返回买入价。
            业务类型暂支持取值：
        6：B2B结汇付款汇率，
        7：B2B国际分发汇率
        8：B2B兑换汇率
        示例：如币种对 USD/CNH

        卖出USD->买入CNH，则返回7.231900,表示：卖出1 USD可以换7.231900 CNH
        卖出CNH->买入USD，则返回7.260700,表示：买入1 USD需要7.260700 CNH"""
    # 获取秘钥相关信息

    data_env = enc.get_envs(env)
    url = f"{data_env.get('url')}/api/agent/rate/query-rate"

    data = {
          "bizType":"8",
          "closingType":"SPOT",
          "originalCcy":"CNH",
          "targetCcy":"USD"
    }
    # ic(data)
    p.rsa_and_send_request(data, env, url, apiType=3)





def run_query(method_name, env, time_seconds=1, number=1):
    """
    动态调用指定接口，在指定时间内发送指定次数请求
    :param method_name: 要调用的方法名（"query_rate" 或 "b2b_query_rate"）
    :param env: 环境参数，如 "fat", "uat"
    :param time_seconds: 请求周期（秒）
    :param number: 请求次数
    :return:
    """
    # 根据方法名选择实际调用的函数
    if method_name == "query_rate":
        method = query_rate
    elif method_name == "b2b_query_rate":
        method = b2b_query_rate
    else:
        raise ValueError(f"不支持的方法名: {method_name}")

    print(f"[{datetime.now()}] 开始执行任务，接口: {method_name}，环境: {env}")
    print(f"在 {time_seconds}s 内发送 {number} 次请求")

    interval = time_seconds / number  # 每次请求间隔时间

    for i in range(1, number + 1):
        def task(i):
            print(f"[{datetime.now()}] 第 {i} 次请求开始")
            method(env=env)
            print(f"[{datetime.now()}] 第 {i} 次请求结束")

        Thread(target=task, args=(i,)).start()
        time.sleep(interval)

    print(f"[{datetime.now()}] 请求任务结束，共发送 {number} 次请求")

if __name__ == "__main__":
    # 示例：在 1s 内发送 10 次 query_rate 请求
    fat_env = "uat-sea-agent-hzl"
    run_query(method_name="query_rate", env=fat_env, time_seconds=20, number=103)

    # 示例：在 60s 内发送 60 次 b2b_query_rate 请求
    # run_query(method_name="b2b_query_rate", env="fat", time_seconds=60, number=60)
