'''
Created on 2022年6月30日

@author: 段海洋
'''

from selenium import webdriver
import time

# 通过executable_path 获取firefox的驱动
driver = webdriver.Firefox(executable_path="C:\\files_sea\\exe\\geckodriver")

# 打开搜狗软件
driver.get("http://www.sogou.com")

#获取输入框的元素
input_text = driver.find_element_by_id('query')
input_text.clear()
input_text.send_keys("光荣之路自动化")

search_btn = driver.find_element_by_id('stb')

search_btn.click()
time.sleep(3)
driver.quit()



