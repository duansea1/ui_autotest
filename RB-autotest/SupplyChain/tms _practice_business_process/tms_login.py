#coding=utf-8
from selenium import webdriver
from time import sleep

def login():
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
# browser = webdriver.Chrome()
# browser.maximize_window()
# url='http://tms2.111.com.cn/home'
# browser.get (url)
# browser = webdriver.Chrome()
# browser.maximize_window() #最大化浏览器
# url='http://tms2.111.com.cn/home'
#进入TMS


