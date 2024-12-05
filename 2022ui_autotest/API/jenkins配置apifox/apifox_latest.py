# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-02-23 15:42
# ---
import argparse
from logging import exception
import os
import sys
import re
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class ApifoxScript:
    # 删除指定文件夹和文件
    def delete_dirs(self, path, keep_files_num):
        # path:删除文件的路径
        # keep_files_num:路径下需要保存的文件数量
        print("开始执行删除")
        for root, dirs, files in os.walk(path):
            # root:当前文件夹地址
            # dirs:当前文件夹下的所有目录list
            # files:当前文件下的所有文件list
            print(files)
            # 遍历删除目录
            for name in dirs:
                dir_path = os.path.join(root, name)
                # print(dir_path)
                if os.path.exists(dir_path):
                    try:
                        os.rmdir(dir_path)
                    except exception as e:
                        print('删除文件夹失败' + e)

            path_time_list = []
            file_path = ''

            # 获取文件最后修改时间，保留最新的keep_files_num数量的文件，删除多余文件
            for file in files:
                file_path = os.path.join(root, file)
                path_time = os.path.getmtime(file_path)
                path_time_list.append(path_time)

            # 待删除的文件地址日期list
            del_path_time_list = sorted(path_time_list, reverse=True)[keep_files_num:]
            del_path_list = []
            # 根据del_path_time_list找到需要删除的文件地址del_path_list
            if len(del_path_time_list) > 0:
                for path_time in del_path_time_list:
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            if os.path.getmtime(file_path) == path_time:
                                del_path_list.append(file_path)
                        except exception as e:
                            print("读取文件目录错误" + e)
            else:
                print("文件未达到 " + str(keep_files_num) + " 份，无需删除")

            print(del_path_list)
            # 删除文件
            for del_path in del_path_list:
                try:
                    if os.path.exists(del_path):
                        os.remove(del_path)
                except exception as e:
                    print("删除文件出错" + e)

    # 指定本python文件通过bash或shell命令运行时外部传入的参数
    def parse_args(self):
        print(sys.argv)
        default_apifox_cli = (r"call apifox run https://api.apifox.cn/api/v1/projects/2871719/api-test/ci-config/407550/detail?token=x9kH9qSoPkqbNhez9WtOyC -r html,cli --out-file %JOB_NAME%%BUILD_NUMBER% exit 0")
        # database_json_path = '/var/jenkins_home/workspace/check-apifox/database-connections.json'
        parser = argparse.ArgumentParser()
        # Jenkins中job的名字
        parser.add_argument("--job-name", dest="job_name", type=str, action="store", default='SCRM_API_cases')
        # Jenkins中job的第n次构建
        parser.add_argument("--build-number", dest="build_number", type=int, action="store", default=160)
        # 需要保留的文件数量
        parser.add_argument("--set-num", dest="set_num", type=int, action="store", default=10)
        # apifox测试用例或测试套件命令
        parser.add_argument("--apifox-cli", dest="apifox_cli", type=str, action="store", default=default_apifox_cli)
        # 数据库配置
        # parser.add_argument("--database-json-path", dest="database_json_path", type=str, action="store",
        #                     default=database_json_path)

        args = parser.parse_args()
        return {"job_name": args.job_name, "build_number": args.build_number, "set_num": args.set_num,
                "apifox_cli": args.apifox_cli, "database_json_path": 'please check .py'}

    # 判断报告中是否存在失败的用例
    def html_result(self, html_path, status_path):
        # 定义报告的执行结果默认为True
        # html报告只有失败的时候会有‘失败情况’四个字，读取报告检索是否有这四个字即可知道
        #  测试用例的执行情况
        cases_result = True
        try:
            with open(html_path, "r", encoding='utf-8') as f:
                html = f.read()
                res_list = re.findall("失败情况", html)
                print(res_list)
                if len(res_list) != 0:
                    cases_result = False

            # 根据报告结果将结果写入txt中
            with open(status_path, "w", encoding="utf-8") as t:
                if cases_result:
                    t.write("STATUS=Passed")
                    os.environ['STATUS']='PASSED'
                    print("STATUS=All cases passed")
                else:
                    t.write("STATUS=Failed")
                    os.environ['STATUS']='FAILED'
                    print("STATUS=Some cases failed")
            f.close()
            t.close()
        except exception as e:
            print("读取报告html文件失败" + e)


if __name__ == '__main__':
    apifox = ApifoxScript()
    args_dict = apifox.parse_args()
    apifox_cli = args_dict.get("apifox_cli")
    # database_json_path = args_dict.get("database_json_path")
    job_name = args_dict.get("job_name")
    set_num = args_dict.get("set_num")
    build_number = args_dict.get("build_number")

    # print("database_json_path: " + database_json_path)
    #
    # if database_json_path:
    #     apifox_cli = apifox_cli + " --database-connection " + database_json_path
    #     print("apifox_cli: " + apifox_cli)

    base_path = r"C:\ProgramData\Jenkins\.jenkins\workspace"
    report_path = base_path + "/" + job_name + r"/apifox-reports"
    report_name = job_name + str(build_number)
    print("report_path： " + report_path)
    print("report_name： " + report_name)

    # 执行删除html报告
    apifox.delete_dirs(report_path, 10)
    print("删除完毕delete-over!!!")

    # 执行apifox命令
    apifox_full_cli = f"{apifox_cli}  --out-file {report_name} --out-dir {report_path}"
    print("apifox_full_cli: " + apifox_full_cli)

    msg = os.system(apifox_full_cli)
    print("运行apifoxbash结果")
    print(msg)

    # 判断用例执行结果，附加在推送邮件中
    html_report_path = report_path + "/" + report_name + ".html"
    print("html_report_path: " + html_report_path)
    status_path = base_path + "/" + job_name + r"/build_status.txt"
    print("用例执行的状态写入文件-status_path: " + status_path)
    apifox.html_result(html_report_path, status_path)