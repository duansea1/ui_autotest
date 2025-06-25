import requests



cookie = 'agent-control-core-token=eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDI0MDYyNzEwMTIwNTAwNTgiLCJpYXQiOjE3NDI1MzU5NTR9.MIR0KMWnr4P7jaECXW_4VQ5E-59pO32cfVL-cYfXRAMpUG4Nsrpky-bbN6ebbpSNB425nX-BELaxKC_NeyR6Ug'

def run_timed_job(job_no):
    """
    执行定时任务的函数--【测试环境】

    参数:
    job_no (int): 任务编号
    """
    url = 'https://fat-global-ad.baofu.com/ams-api/timedJob/run'
    headers = {

        'Content-Type': 'application/json',

        'Cookie': cookie
    }
    data = {
        "jobNo": job_no,
        "operationBy": "段海洋"
    }

    # 移除 compress=True 参数
    response = requests.post(url, headers=headers, json=data, verify=False)
    return response.text


# 示例调用

result = run_timed_job(67)  # 汇兑订单交割定时任务
# result = run_timed_job(249)  # 手动交割的汇兑交割提醒
# result = run_timed_job(204)  # 	渠道汇兑订单自动交割
# result = run_timed_job(198)  # 	货币兑换API自动策略下单定时任务
# result = run_timed_job(71)  # 	海外换汇官方汇率查询定时任务
print(result)