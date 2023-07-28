#coding=utf-8
from selenium import webdriver
from time import sleep
import os
import openpyxl
import random
import mysql.connector
'''返款数据汇总校验'''
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
# title=browser.title
# print("页面标题为："+title)
# url=browser.current_url
# print("当前网址为："+url)
# sleep(3)
farther=browser.find_elements_by_css_selector("ul.layui-layout-left>li>a")
son=browser.find_elements_by_css_selector("li.layui-nav-item>dl>dd>a")
sleep(2)
first='费用结算'
second='COD汇总对账'
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
browser.find_element_by_id("btn-submit").click()#点击查询
sleep(2)
DO=browser.find_elements_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[3]/div')
order_amount=browser.find_elements_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[11]/div')
fright_fee=browser.find_elements_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[13]/div')
to_collect_amount=browser.find_elements_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[14]/div')
Refund_amount=browser.find_elements_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[15]/div')
'''DO'''
print ('   DO   ：' , end="")
for do in DO:
    print(do.text, end=" ")
print('\n')

'''订单金额'''
print ('订单金额：' , end="")
order_amount_Sum1=0
for a in order_amount:
    order_amount_Sum1+=int(a.text)
    print(a.text, end="  ， ")
print('订单总金额：',order_amount_Sum1)

'''运费'''
print ('运    费：', end="")
fright_fee_Sum1=0
for b in fright_fee:
    fright_fee_Sum1+=int(b.text)
    print(b.text, end="  ， ")
print('运费总金额：',fright_fee_Sum1)

'''应收金额'''
print ('应收金额：', end="")
to_collect_amount_Sum1=0
for c in to_collect_amount:
    to_collect_amount_Sum1+=int(c.text)
    print(c.text, end="  ， ")
print('应收总金额：',to_collect_amount_Sum1)

'''返款金额'''
print ('返款金额：', end="")
Refund_amount_Sum1=0
i=''
for d in Refund_amount:
    if d.text ==i:
        m=0
    else:
        m=d.text
    Refund_amount_Sum1+=int(m)
    print(m, end="  ， ")
print('返款总金额：',Refund_amount_Sum1)
sleep(2)
order_amount_Sum2=int(browser.find_element_by_xpath('//*[@id="layui-laypage-2"]/span[6]').text)
fright_fee_Sum2=int(browser.find_element_by_xpath('//*[@id="layui-laypage-2"]/span[9]').text)
to_collect_amount_Sum2=int(browser.find_element_by_xpath('//*[@id="layui-laypage-2"]/span[12]').text)
Refund_amount_Sum2=int(browser.find_element_by_xpath('//*[@id="layui-laypage-2"]/span[15]').text)
if order_amount_Sum1==order_amount_Sum2 \
        and fright_fee_Sum1==fright_fee_Sum2\
        and to_collect_amount_Sum1==to_collect_amount_Sum2\
        and Refund_amount_Sum1==Refund_amount_Sum2:
    print (order_amount_Sum2, fright_fee_Sum2, to_collect_amount_Sum2, Refund_amount_Sum2)
    print("汇总金额相等，测试通过")
else:
    print("汇总金额不相等，测试不通过")
sleep(1)
browser.quit()
