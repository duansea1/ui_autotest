"""
Created on 2019/7/25
"""
import pytest
from Demoproject.home import HomePage
from time import sleep
@pytest.mark.pre_b2cpc_1
def test_login_search(selenium):
    '''demo'''
    h = HomePage(selenium)
    h.go_to_homepage() #打开首页
    sleep(5)
    findBusness = h.driver.find_element_by_css_selector('#businessInvitation > a > span')
    assert findBusness.text == '我要找商机'
    findBusness.click()
    h.driver.find_element_by_class_name('link-quickview').click()
    loginText = h.driver.find_element_by_css_selector('.login_title > p')
    assert loginText.text == '用户登录'
    sleep(2)
    



if __name__ == '__main__':
    from function import system
    import os
    system.runtc(os.path.basename(__file__),'pre_b2cpc_1',driver='Chrome',
                 options=[]) #Firefox，Chrome