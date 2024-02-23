# -*- coding: utf-8 -*-
# ---
# @Author: https://blog.csdn.net/weixin_53846408/article/details/127954250
# @Time: 2024-02-21 14:51

# ---
import requests
import json
import urllib3
import sys
import re
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class InformRobot:
    def __init__(self):
        self.sess = requests.session()
        self.test_case_passing_rate = ""
        self.test_case_fail_rate = ""
        self.avg_api_response_rate = ""
        self.test_case_untested_rate = ""
        self.test_case_quantity_rate = ""

    def markdown_robot(
            self, webhook_url, report_url, principal, job_name, test_environment, STATUS
    ):
        """
        实现企业微信通知
        :param webhook_url: 企业微信token
        :param report_url: 报告地址
        :param principal: 负责人名称
        :param job_name: 项目名称
        :param test_environment:环境名称
        :return:
        """
        data = {

            "msgtype": "markdown",  # 消息类型，此时固定为markdown

            "markdown": {
                "content": f"### 提醒! <font color=\"info\"> {job_name} </font> 接口自动化测试反馈  \n "
                           f">项目名称：{test_environment} \n" +
                           f">测试用例结果：<font color=\"info\"> {STATUS} </font> \n" +
                           f">测试用例（接口）总数：<font color=\"info\"> {self.test_case_quantity_rate} </font> \n" +
                           f">平均接口请求耗时：<font color=\"info\"> {self.avg_api_response_rate} </font> \n" +
                           f">测试用例通过率：<font color=\"info\"> {self.test_case_passing_rate} </font> \n" +
                           f">测试用例失败率：<font color=\"#FF0000\"> {self.test_case_fail_rate} </font> \n" +
                           f">测试用例未测率：<font color=\"#FFCC33\"> {self.test_case_untested_rate} </font> \n" +
                           f">测试报告链接：[点击查看报告详情]({report_url}) \n" +
                           f">测试负责人：{principal}"
            }
        }
        re_post = self.sess.post(webhook_url, data=json.dumps(data), verify=False)
        print('打印请求的数据：：', re_post.content, data)
        return re_post

    def result_pass_rate(self, html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            report = f.read()

        pass_rate = re.search('<div class="col-md-4 text-label">通过率</div>\n\ +<div class="col-md-8">(.*?)</div>',
                              report)

        fail_rate = re.search('<div class="col-md-4 text-label">失败率</div>\n\ +<div class="col-md-8">(.*?)</div>',
                              report)
        avg_api_response_time = re.search(
            '<div class="col-md-4 text-label">平均接口请求耗时</div>\n\ +<div class="col-md-8">(.*?)</div>',
            report)

        case_untested_rate = re.search(
            '<div class="col-md-4 text-label">未测率</div>\n\ +<div class="col-md-8">(.*?)</div>', report)
        case_quantity_rate = re.search(
            '<div class="col-md-4 text-label">HTTP 接口请求数</div>\n\ +<div class="col-md-4">(.*?)</div>', report)

        self.test_case_fail_rate = fail_rate.group(1)  # 用例失败率
        self.test_case_passing_rate = pass_rate.group(1)  # 用例通过率
        self.avg_api_response_rate = avg_api_response_time.group(1)  # 平均接口请求耗时
        self.test_case_untested_rate = case_untested_rate.group(1)  # 用例未测率
        self.test_case_quantity_rate = case_quantity_rate.group(1)  # 用例数量(应该是循环数，改为了接口数量)


if __name__ == '__main__':
    print('sysargv:', sys.argv)
    # for key, value in os.environ.items():
    #   print(f"{key}: {value}")
    print("testtestosenviron", os.environ.get('webhook_url'))
    job_name = os.environ.get('JOB_NAME')
    test_environment = os.environ.get('ENV_TEST')
    STATUS = sys.argv[6]
    build_number = os.environ.get('BUILD_NUMBER')
    print('构建ID：', build_number)
    webhook_url = os.environ.get('webhook_url')
    report_url = os.environ.get('WORKSPACE')
    principal = sys.argv[3]
    r_url = "\\apifox-reports\\" + str(job_name) + str(build_number) + ".html"
    print(r_url)
    report_url += r_url  # 拼接测试报告
    print(report_url)

    # webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a5168c15-720b-4aed-9bfa-2eb1897b8a86"
    # report_url = "url_report"
    # principal = "# 测试"
    # job_name = "job名字"
    # test_environment = "测试"
    # STATUS = "成功"
    # build_number = 222

    # path = "/var/jenkins_home/workspace/{}/apifox-reports/test-dsp-apifox_{}.html".format(job_name, build_number)
    # path = "C:/ProgramData/Jenkins/.jenkins/workspace/SCRM_API_cases/apifox-reports/a-test.html"
    path = f"C:/ProgramData/Jenkins/.jenkins/workspace/{job_name}/apifox-reports/{job_name}{build_number}.html"

    info_robot = InformRobot()
    info_robot.result_pass_rate(path)
    info_robot_res = info_robot.markdown_robot(webhook_url, report_url, principal, job_name, test_environment, STATUS)
    print("info_robot_res:", info_robot_res)

    info_robot.sess.close()