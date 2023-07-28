#coding=utf-8
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.common.exceptions import NoSuchElementException
import time;

browser = webdriver.Chrome()
browser.maximize_window() #最大化浏览器
url='http://tms2.111.com.cn/home'
print ("进入%s"%(url))#进入TMS
browser.get(url)
# login()
print("输入用户名")
browser.find_element_by_name("username").send_keys("chenpeng")
print("输入密码")
browser.find_element_by_name("password").send_keys("Cp,456789")
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
first='费用结算'
second='COD订单管理'
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
sleep(1)
browser.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/div/input').click()
sleep(1)
print('选择全部')
browser.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/dl/dd[1]').click()
# print('选择未导入订单')
# browser.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/dl/dd[2]').click()
sleep(1)
print("输入出库时间")
browser.find_element_by_id('leaveDcTimeStart').clear()
browser.find_element_by_id('leaveDcTimeStart').send_keys('2017-04-01 00:00:00')
print("点击查询")
browser.find_element_by_id("btn-submit").click()
sleep(3)
a=browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[4]/div').text
sleep(1)
b=browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[17]/div').text
print('do单号：'+a)
print('返款状态：'+b)
print('勾选订单')
browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td/div/div/i').click()
sleep(1)
print('点击返款')
browser.find_element_by_id('confirm').click()
sleep(2)
browser.find_element_by_name("code").send_keys(a)
sleep(1)
browser.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/div/input').click()
sleep(1)
browser.find_element_by_name("code").click()

# print('选择全部')
# browser.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/dl/dd[1]').click()
# sleep(1)
print("点击查询")
browser.find_element_by_id("btn-submit").click()
sleep(3)
status=browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[17]/div').text
if status == '异常':
    print('BEGIN_STATUS：'+b,"END_STATUS："+status)
    print('---------测试通过---------')
elif status == b:
    print('BEGIN_STATUS：'+b,"END_STATUS："+status)
    print('---------测试通过---------')
else:
    print('BEGIN_STATUS：'+b,"END_STATUS："+status)
    print('---------测试不通过---------')
