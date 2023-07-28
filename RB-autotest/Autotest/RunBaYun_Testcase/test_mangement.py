'''
Created on 2019年8月4日

@author: Administrator
'''
"""
Created on 2019/7/25
"""
import pytest
from Demoproject.home import HomePage
from time import sleep
from business.login import login
from _socket import timeout
  
@pytest.mark.prd_pc_0
def test_01open_find_company(selenium):
    '''招商管理-打开找企业页面'''
    l=login.Login(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(3)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'   
    selenium.get('http://codemaster.runbaba.com/Business/FindCompany/index')
    s=selenium.find_elements_by_css_selector('.pull-left>.form-control') #搜索框
    assert len(s)>0,'打开找企业页面未展示搜索框' 

@pytest.mark.prd_pc_0
def test_02find_company_search(selenium):
    '''招商管理-打开找企业页面,搜索企业名称展示对应搜索结果'''
    l=login.Login(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(3)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'   
    selenium.get('http://codemaster.runbaba.com/Business/FindCompany/index')
    s=selenium.find_element_by_css_selector('.pull-left>.form-control') #搜索框
    s.click()
    s.clear()
    s.send_keys('上海润蓝企业管理咨询有限公司')
    selenium.find_element_by_id('submit_btn').click()
    sleep(2)
    info=selenium.find_element_by_css_selector('.table>tbody>tr').text.strip()
    print('搜索结果',info)
    assert '上海润蓝企业管理咨询有限公司' in info ,'搜索结果未正常显示'

if __name__ == '__main__':
    from function import system
    import os
    system.runtc(os.path.basename(__file__),'prd_pc_0',driver='Chrome',
                 options=[]) #Firefox  hrome