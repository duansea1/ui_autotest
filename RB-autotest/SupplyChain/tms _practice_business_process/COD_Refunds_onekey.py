#coding=utf-8
from selenium import webdriver
from time import sleep
import os
import openpyxl
import random
import mysql.connector
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
'''COD一键返款'''
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
print('选择处理中订单')
browser.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/dl/dd[3]').click()
sleep(1)
print("输入出库时间")
browser.find_element_by_id('leaveDcTimeStart').clear()
sleep(1)
browser.find_element_by_id('leaveDcTimeStart').send_keys('2017-04-01 00:00:00')
browser.find_element_by_id("btn-submit").click()#点击查询
sleep(2)
do=browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr[1]/td[4]/div').text
batch_no=browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[18]/div').text
status1=browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[17]/div').text
print('订单DO：'+do)
print('批次号：'+batch_no)
print('返款状态：'+status1)
sleep(1)
print('点击一键返款')
browser.find_element_by_id('oneKeyConfirmData').click()
sleep(1)
warning=browser.find_element_by_xpath('//*[@id="layui-layer1"]/div[2]').text
print(warning)
sleep(1)
browser.find_element_by_xpath('//*[@id="layui-layer1"]/div[3]/a').click()
sleep(1)
print('输入批次号')
browser.find_element_by_name('serialNum').send_keys(batch_no)
browser.find_element_by_id("btn-submit").click()#点击查询
sleep(1)
print('一键返款')
browser.find_element_by_id('oneKeyConfirmData').click()
sleep(1)
warning2=browser.find_element_by_xpath('//*[@id="layui-layer2"]/div[2]').text
print('点击确定')
browser.find_element_by_xpath('//*[@id="layui-layer2"]/div[3]/a[1]').click()
sleep(2)
browser.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/div/input').click()
sleep(1)
print('选择全部订单')
browser.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/dl/dd[1]').click()
browser.find_element_by_id("btn-submit").click()#点击查询
sleep(2)
status2=browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[17]/div').text
print('初始返款状态：'+status1)
print('一键返款状态：'+status2)
if status2=='异常' or status2=='已返款':
    print('一键返款成功，测试通过')
else:
    print('一键返款失败，测试不通过')
sleep(2)
browser.quit()
