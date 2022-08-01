# -- coding: utf-8 --
# @time :
# @author : xxxx
# @file : .py
# @desp : 全局夹具；不需要导入调用该默认文件
import logging

from selenium import webdriver
from time import sleep
import pytest


@pytest.fixture(scope="module")
def driver():
    # 启动谷歌浏览器
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture()
def user_driver():
    "已登录的浏览器"
    driver = webdriver.Chrome()
    driver.maximize_window()
    print("假装-打开浏览器-已登录成功")
    yield driver
    driver.quit()


@pytest.fixture()
def clear_favor(user_driver):
    "夹具：假设是取消收藏；已登录->跳转到个人中心--》对页面商品进行清除"
    print("一个case可使用多个夹具")
    pass


#创建logger


logger = logging.getLogger(__name__)


def pytest_runtest_setup(item):
    logger.info(f"开始执行：{item.nodeid}".center(60, "-"))


def pytest_runtest_teardown(item):
    logger.info(f"执行结束：{item.nodeid}".center(60, "-"))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    "钩子函数：框架执行过程中，根据执行结果执行"
    outcome = yield
    report = outcome.get_result

    if report.when == "call":

        o = report.outcome
        s = f"用例执行结果：【{report.outcome}】"
        path = "images/{time.time()}.png"
        if o == "failed":
            logger.error(s)
        elif o == "skip":
            logger.warning(s)
        else:
            logger.info(s)
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            driver.get_screenshot_as_file(path)
            logger.info(f"页面截图：{path}")









