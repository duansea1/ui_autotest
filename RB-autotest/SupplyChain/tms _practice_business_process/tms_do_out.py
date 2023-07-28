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
        sleep(3)
        for a in son:
            if a.text.strip()==second:
                print("点击二级菜单："+second)
                a.click()
                sleep(3)
frame=browser.find_element_by_css_selector("body > div > div.layui-body > div > div > div > div > iframe")
print("切换frame")
browser.switch_to_frame(frame)
print("点击查询")
browser.find_element_by_id("address_query_btn").click()
print("获取DO列表_第一列数据")
sleep(3)
do=browser.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[3]/div").text#DO单号
sleep(2)
carrier=browser.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[8]/div").text#承运商
sleep(3)
leave_time=browser.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[5]/div").text#出库时间
current_time=time.time()
print("DO单号为："+do)
print ("当前时间为："+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(current_time)))
print("出库时间为："+leave_time)
print("承运商为："+carrier)
c=time.mktime(time.strptime(leave_time,"%Y-%m-%d %H:%M:%S"))#字符串转换为时间戳
a=time.strftime("%Y-%m-%d %H",time.localtime(current_time))#当前时间-时间戳转换为年-月-日-时
d=time.strftime("%Y-%m-%d %H",time.localtime(c))#出库时间-时间戳转换为年-月-日-时
if a==d:
    print("----------当前为线上环境-------------")
else:
    print("-------当前为测试环境------------")
sleep(3)
browser.quit()

