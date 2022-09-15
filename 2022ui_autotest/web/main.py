# -- coding: utf-8 --
# @time :
# @author : xxxx
# @file : .py
# @desp : xxxx
import pytest
import os
import allure_pytest
# 安装allure相关信息 配置环境变量

# pytest.main()
pytest.main(["-vrA", "-s", "-m excel"])
# pytest 允许完毕后，自动生成报告
#===手动执行
# os.system("allure serve .allure_results")
## 自动探测
os.system("allure generate ./allure_results -o ./reports_new --clean")