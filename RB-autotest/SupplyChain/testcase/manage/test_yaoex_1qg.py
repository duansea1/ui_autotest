'''
Created on 2018年11月15日

@author: zengkai
'''
from business.manage.yaoex_manage import Yaoex
import pytest
from business.manage.manage_home import ManageSystem
from time import sleep

@pytest.fixture
def selenium(selenium):
    print('脚本运行的浏览器：',selenium.name)
#     if selenium.name!='internet explorer':
#         selenium.implicitly_wait(40)
#     print('浏览器版本：',selenium.capabilities['version'])
    selenium.maximize_window()
    return selenium

@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--ignore-certificate-errors')
    prefs= {
        "profile.managed_default_content_settings.images":1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player":1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player":1,
        "credentials_enable_service":False,
        "profile.password_manager_enabled":False
        }
    chrome_options.add_experimental_option('prefs', prefs)
    return chrome_options


@pytest.mark.for_skip
def test_1qg_list(selenium):
    ''''''
    manage=ManageSystem(selenium)
    manage.login("qa_manage", "YW_manage")
    manage.chose_platform()
    manage.toggle_workplat()
    manage.chose_subsystem("1药城运营后台")
    manage.switch_to_latest_windows()
    print(manage.driver.title)
    sleep(3)
    print("进入: 1药城运营后台")
    yaoex=Yaoex(selenium)
    yaoex.click_frist_level("平台活动")
    yaoex.click_child_level("一起购活动")
    sleep(3)
    #yaoex.search_1qg_multiquery(aid="255",display="all", suppler="all")
    sleep(3)

@pytest.mark.for_pytest
def test_create_1qg(selenium):
    ''''''
    manage=ManageSystem(selenium)
    manage.login("qa_manage", "YW_manage")
    manage.chose_platform()
    manage.chose_subsystem("1药城运营后台")
    yaoex=Yaoex(selenium)
    yaoex.click_frist_level("平台活动")
    yaoex.click_child_level("一起购活动")
    sleep(3)
    yaoex.create_1qg_activitie()
    sleep(3)
 
    
if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'for_pytest',driver='Chrome')