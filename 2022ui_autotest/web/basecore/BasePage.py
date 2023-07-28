# -- coding: utf-8 --
# @time :
# @author : xxxx
# @file : .py
# @desp : driver的基础封装、元素定位


from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import NoSuchElementException
import re
import os
import base64
import hashlib
from selenium.common.exceptions import TimeoutException
from PIL import Image
# from localplugins.PredictCaptcha import predict_captcha

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('BASE_DIR: ', BASE_DIR)


class Base:
    '''driver的一些基础封装-web'''

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, ele_loc, timeout=30):
        '''查找元素
        @param ele_loc: 元素定位方法，类似： (By.ID, "bu", "元素描述语")
        '''
        try:
            self.wait_until_display(ele_loc, timeout)
            ele = self.driver.find_element(*ele_loc[:2])
            return ele
        except NoSuchElementException:
            msg = '查找元素超时：' + str(ele_loc)
            print(msg)
            raise Exception(msg)
        except TimeoutException:
            msg = '查找元素超时：' + str(ele_loc)
            print(msg)
            raise Exception(msg)
        except Exception as e:
            print('查找元素，其他异常')
            raise Exception(e)

