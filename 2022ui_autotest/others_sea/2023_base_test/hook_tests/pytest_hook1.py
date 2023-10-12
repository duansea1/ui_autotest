# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月12日 9:28
# ---
import smtplib

import pytest

"""
如果想在一个类中使用，那么@pytest.fixture(scope="class")；

如果想在全部会话中使用，那么@pytest.fixture(scope="session"）。
也就是优先级从大到小：session-->module–->class–->function
"""
@pytest.fixture(scope="module")
def stmp_connection():
    import smtplib
    return smtplib.SMTP("smtp.gmai.com", 587, timeout=5)

def test_ehlo(smtp_connection):
    response, msg = smtp_connection.ehlo()
    assert response == 250
    assert 0  # 强制断言失败

def test_noop(smtp_connection):
    response, msg = smtp_connection.ehlo()
    assert response == 250
    assert 0  # 强制断言失败

@pytest.fixture(scope="function")
def smtp():
    smtp = smtplib.SMTP("smtpgmail.com")
    yield smtp
    print("teardown smtp")
    smtp.close()

"""
6. fixture中的参数 autouse

关于autouse，默认是False, 如果不加scope='session'，的使用autouse，只在当前module下有效。

① 如果你想一个module下的都用上，那就打开改成True, 如下，这样就不需要往每个函数里传入fixture，例如：
"""


