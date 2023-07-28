#coding=utf-8
from selenium import webdriver
from time import sleep
import os
import openpyxl
import random
import mysql.connector
import time
'''COD订单批量备注'''
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
sleep(1)
print("输入出库时间")
browser.find_element_by_id('leaveDcTimeStart').clear()
sleep(1)
browser.find_element_by_id('leaveDcTimeStart').send_keys('2017-04-01 00:00:00')
browser.find_element_by_id("btn-submit").click()#点击查询
sleep(2)
first_remark = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[24]/div/a').text
print(first_remark)
print('点击批备')
browser.find_element_by_id("remarks").click()
sleep(1)
tips=browser.find_element_by_xpath('//*[@id="layui-layer1"]/div[2]').text
print(tips)
print('点击确定')
browser.find_element_by_xpath('//*[@id="layui-layer1"]/span[1]/a').click()
sleep(1)
print('全选')
browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[3]/div[1]/table/thead/tr/th/div/div/i').click()
sleep(1)
print('点击批备')
browser.find_element_by_id("remarks").click()
sleep(1)
print('切换到备注弹窗frame')
browser.switch_to_frame(browser.find_element_by_id('layui-layer-iframe2'))
sleep(1)
print('输入备注信息')
time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
remark_text="自动化测试 "+time
browser.find_element_by_name('remark').send_keys(remark_text)
sleep(1)
print('点击保存')
browser.find_element_by_id('btn-submit').click()
sleep(2)
print("切换到主界面frame")
browser.switch_to.frame(frame)
sleep(1)
second_remark = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[24]/div/a').text
print('备注信息为：'+second_remark)
if remark_text==second_remark:
    print('批量备注成功，测试通过')
else:
    print('批量备注失败，测试不通过')
sleep(2)
browser.quit()

