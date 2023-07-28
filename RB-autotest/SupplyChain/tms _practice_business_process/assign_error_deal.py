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
second='配送异常'
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
print("清空出库时间")
browser.find_element_by_id('leaveDcTimeStart').clear()
browser.find_element_by_id('leaveDcTimeEnd').clear()
print("点击查询")
browser.find_element_by_id("btn-submit").click()
# print('滑至页面底部')
# js="var q=document.documentElement.scrollTop=100000"
# browser.execute_script(js)
sleep(5)
print('点击处理')
browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[2]/div/a[1]').click()
sleep(1)
print('切换到弹窗iframe')
browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="layui-layer-iframe1"]'))
print('选择处理原因')
browser.find_element_by_xpath('//*[@id="ex_order_form"]/div/div[6]/div/div/div/div/input').click()
sleep(1)
browser.find_element_by_xpath('//*[@id="ex_order_form"]/div/div[6]/div/div/div/dl/dd[2]').click()
print('输入备注')
browser.find_element_by_id('exRemark').send_keys('测试')
print('保存')
browser.find_element_by_xpath('//*[@id="ex_order_form"]/div/div[8]/div/button').click()
sleep(2)
browser.switch_to_default_content()
sleep(1)
print("切换主界面frame")
browser.switch_to.frame(frame)
sleep(2)
print("点击查询")
browser.find_element_by_id("btn-submit").click()
sleep(2)
print('查看日志详情')
browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[2]/div/a[2]').click()
sleep(2)
print('切换到日志详情弹窗')
browser.switch_to.frame(browser.find_element_by_xpath('//*[@id="layui-layer-iframe2"]'))
# reason=browser.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[2]/div').text
# date=browser.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[3]/div').text
# operator=browser.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[4]/div').text
# remark=browser.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[5]/div').text
# print('日志详情')
# print("处理原因："+reason)
# print("日    期："+date)
# print("处 理 人："+operator)
# print("备    注："+remark)
number=browser.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[3]/div[2]/table/tbody/tr/td/div')#第一列序号
reason=browser.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[2]/div')#第2列处理原因
date=browser.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[3]/div')#第3列处理时间
operator=browser.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[4]/div')#第4列处理人
remark=browser.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[5]/div')#第5列备注
list1=[]
list2=[]
list3=[]
list4=[]
list5=[]
for i in number:
    m='第' + i.text + '条日志详情：'
    list1.append(m)
    # print ('第' + i.text + '条日志详情：')
for a in reason:
    n='处理原因：'+a.text
    list2.append(n)
for b in date:
    o='处理时间：'+b.text
    list3.append(o)
for c in operator:
    p='处理人：'+c.text
    list4.append(p)
for d in remark:
    q="备注："+d.text
    list5.append(q)
log_list = map(list,zip(list1,list2,list3,list4,list5))
for j in log_list:
    print(j)
sleep(2)
browser.quit()

'''列表合并函数
# list1 = [1, 2, 3, 4, 5]
# list2 = [1, 2, 3, 4, 5]
# list3 = [1, 2, 3, 4, 5]
# multi_list = map(list, zip(list1, list2, list3))
# for i in mulit_list:
# print(i)
'''

