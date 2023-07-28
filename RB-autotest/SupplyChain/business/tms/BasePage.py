#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/13
# @Author  : zhangqinqin

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import NoSuchElementException
import re


class Base(object):
    def __init__(self, driver):
        self.driver = driver

    def get_page_source(self):
        """
        获取当前页面源码
        :return:
        """
        page_source = self.driver.page_source
        print(page_source)
        return page_source

    def assert_source(self, text):
        """
        断言当前页面源码是否包含字段
        :param text:
        :return:
        """
        src = self.get_page_source()
        text_found = re.search(text, src)
        assert (text_found is not None)



    # 重新封装单个元素定位方法
    def find_element(self, loc):
        """
        单个元素定位方法
        :param loc:
        :return:
        """
        try:
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except NoSuchElementException:
            print(u"%s 页面中未能找到 %s 元素" % (self, loc))
            return None

    # 重新封装一组元素定位方法
    def find_elements(self, loc):
        """
        一组元素定位方法
        :param loc:
        :return:
        """
        try:
            if len(self.driver.find_elements(*loc)):
                return self.driver.find_elements(*loc)
        except NoSuchElementException:
            print(u"%s 页面中未能找到 %s 元素" % (self, loc))

    # 重新封装输入方法
    def send_keys(self, loc, value, clear_first=True, click_first=True):
        """
        输入方法，默认清空输入框，并点击，再输入
        :param loc: 传递的loc必须为R对象中的tuple，而不是WebElement对象
        :param value:
        :param clear_first:
        :param click_first:
        :return:
        """
        try:
            if click_first:
                self.find_element(loc).click()
            if clear_first:
                self.find_element(loc).clear()
            self.find_element(loc).send_keys(value)
        except AttributeError:
            print(u"%s 页面未能找到 %s 元素" % (self, loc))

    # 重新封装按钮点击方法
    def click(self, loc, find_first=True):
        """
        按钮点击
        :param loc: 传递的loc必须为R对象中的tuple，而不是WebElement对象
        :param find_first:
        :return:
        """
        try:
            if find_first:
                self.find_element(loc)
            self.find_element(loc).click()
        except AttributeError:
            print(u"%s 页面未能找到 %s 按钮" % (self, loc))

    def switch_to_latest_windows(self):
        """
        浏览器多窗口，切换到最新窗口
        :return:
        """
        handles = self.driver.window_handles  # 获取所有窗口句柄
        self.driver.switch_to.window(handles[-1])  # 切换到最新窗口

    def get_last_window_title(self):
        """
        浏览器多窗口，获取最新窗口标题
        :return:
        """
        handles = self.driver.window_handles  # 获取所有窗口句柄
        current_handle = self.driver.current_window_handle  # 保存当前窗口句柄
        self.driver.switch_to.window(handles[-1])  # 切换到弹出窗口
        title = self.driver.title  # 获取标题
        self.driver.switch_to.window(current_handle)  # 切换回原窗口
        return title

    def close_latest_window(self):
        """
        浏览器多窗口，关闭最后一个窗口
        :return:
        """
        handles = self.driver.window_handles  # 获取所有窗口句柄
        self.driver.switch_to.window(handles[-1])  # 切换到弹出窗口
        self.driver.close  # 关闭
        self.driver.switch_to.window(handles[-2])  # 切换回上一个窗口
