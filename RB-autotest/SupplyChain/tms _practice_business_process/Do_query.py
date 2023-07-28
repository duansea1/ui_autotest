#coding=utf-8
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.common.exceptions import NoSuchElementException
import time;
from tms.tms_login import login

browser = webdriver.Chrome()
browser.maximize_window() #最大化浏览器
url='http://tms2.111.com.cn/home'
print ("进入%s"%(url))#进入TMS
browser.get(url)
# login()
print("输入用户名")
browser.find_element_by_name("username").send_keys("chenpeng")
print("输入密码")
browser.find_element_by_name("password").send_keys("Cp,147258")
print("点击登录")
browser.find_element_by_css_selector("#login-from > span").click()
sleep(3)
title=browser.title
print("页面标题为："+title)
url=browser.current_url
print("当前网址为："+url)
sleep(3)
farther=browser.find_elements_by_css_selector("ul.layui-layout-left>li>a")
son=browser.find_elements_by_css_selector("li.layui-nav-item>dl>dd>a")
sleep(2)
first='订单管理'
second='DO管理'
for i in farther:
    if i.text.strip() ==first:
        print("点击一级菜单："+first)
        i.click()
        sleep(1)
        for a in son:
            if a.text.strip()==second:
                print("点击二级菜单："+second)
                a.click()
                sleep(1)
frame=browser.find_element_by_css_selector("body > div > div.layui-body > div > div > div > div > iframe")
print("切换frame")
browser.switch_to.frame(frame)
print("点击查询")
browser.find_element_by_id("address_query_btn").click()
time_from="2019-03-01"
time_to="2019-03-01"
do="7033048299"
print("输入出库时间from："+time_from)
browser.find_element_by_xpath("//input[@id='leaveDcTimeStart']").clear()
browser.find_element_by_xpath("//input[@id='leaveDcTimeStart']").send_keys(time_from)
sleep(1)
print("输入出库时间to："+time_to)
browser.find_element_by_xpath("//input[@id='leaveDcTimeEnd']").clear()
browser.find_element_by_xpath("//input[@id='leaveDcTimeEnd']").send_keys(time_to)
sleep(1)
print("输入DO单号："+do)
browser.find_element_by_xpath("//input[@name='code']").click()
sleep(1)
browser.find_element_by_xpath("//input[@name='code']").clear()
browser.find_element_by_xpath("//input[@name='code']").send_keys(do)
print("点击查询")
browser.find_element_by_id("address_query_btn").click()
sleep(1)
# null= browser.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/div[2]/div").text
# print(null)
try:
    if do == browser.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[3]/div").text:#DO单号
        print("测试通过")
    else :
        print ("查询结果不正确，测试不通过")
except NoSuchElementException:
    if "无数据" == browser.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/div[2]/div").text:
        print("DO号输入错误，查无数据")

sleep(2)
browser.quit()

