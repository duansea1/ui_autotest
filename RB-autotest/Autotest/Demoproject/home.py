'''
Created on 2017年8月15日

@author: geqiuli
'''
from time import sleep
from Demoproject.BasePage import Base
from Demoproject.resources import Public as p
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import urllib.request
import re

class HomePage(Base):

 

    def go_to_homepage(self, url=p.home_url):  
        self.driver.get(url)
        sleep(2)
        print('进入页面：',self.driver.title)
        
    def demo_find_element(self):
        self.find_element()




if __name__ == '__main__':
    pass