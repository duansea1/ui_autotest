'''
Created on 2018年9月10日

@author: geqiuli
'''

from selenium.webdriver.common.by import By

class Public:
    home_url = "http://www.runbayun.com/RegCompanyGuide/CompanyRegister"

    station = (By.ID,'usersProvince') #当前区域
    provices = (By.CSS_SELECTOR,'#headerAllProvince > li > a') #选择区域
    switch_provice = (By.CSS_SELECTOR,'.menu-hd.province_box') #切换省份的悬停
    
    

class Homepage:
    health_pop_up = (By.CSS_SELECTOR, '#healthpackageCon>.newuser_box>span.close_a')
    
    
    
    
    