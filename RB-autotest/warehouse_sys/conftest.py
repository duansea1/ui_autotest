'''
Created on 2017年7月27日

@author: geqiuli
'''
import pytest
from py.xml import html #此处html的错误提示请忽略
import os
#import sys
# from function.io_ import read_json
import json
#from business.interface import promotions

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
DesiredCapabilities.INTERNETEXPLORER['ignoreProtectedModeSettings'] = True

projname='warehouse_sys'
root_dir=os.path.abspath('conftest.py').split(projname)[0]+projname+os.sep
print(root_dir)

def read_json(file_name, source='pc'):
    fpath=root_dir + os.sep+'file'+ os.sep + source + os.sep + file_name + ".json"
    with open(fpath, 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    return listCookies

@pytest.fixture
def selenium(selenium):
    print('脚本运行的浏览器：',selenium.name)
    if selenium.name!='internet explorer':
        selenium.implicitly_wait(40)
    #print('浏览器版本：',selenium.capabilities['version'])
    selenium.maximize_window()
    return selenium

@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('--start-maximized')
    prefs= {
        "profile.managed_default_content_settings.images":1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player":1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player":1,
        "credentials_enable_service":False,
        "profile.password_manager_enabled":False
        }
    chrome_options.add_experimental_option('prefs', prefs)
    return chrome_options

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    
    if hasattr(report,"description"):
        des=report.description
    else:
        des="无"
    cells.insert(2, html.td(des))
    cells.pop()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)

def pytest_addoption(parser):
    '''命令行参数'''
    parser.addoption("--warehouse_info", action="store", default='13_广州药业仓库（新）',
        help="wms平台的仓库：13_广州药业仓库（新）,15_昆山药网仓库,233951_广州药网仓库,20_重庆药业仓 等等，以_分割")
    parser.addoption("--warehouse_id", action="store", default='13',
        help="wms平台的仓库id：13,15,233951,20")
    parser.addoption("--do_num", action="store", 
        help="do_num: do号")
    parser.addoption("--is_yc_order", action="store", 
        help="is_yc_order：是否B端订单")
    parser.addoption("--ordertype", action="store", 
        help="order type")
    parser.addoption("--asn_num", action="store", 
        help="ASN_num号")
    parser.addoption("--outbound_type", action="store", default='1',
        help="发货单类型: 1-正常出库，2-调拨出库,3-RTV出库")


@pytest.fixture
def warehouse_id(request):
    '''参数 warehouse'''
    warehouse_str=request.config.getoption("--warehouse_info")
    return warehouse_str.split('_')[0]
 
@pytest.fixture
def do_num(request):
    '''参数 do_num'''
    return request.config.getoption("--do_num")    

@pytest.fixture
def is_yc_order(request):
    '''是否药城订单'''
    return request.config.getoption("--is_yc_order")  

@pytest.fixture
def asn_num(request):
    '''参数 asn_num'''
    return request.config.getoption("--asn_num")

@pytest.fixture
def outbound_type(request):
    '''参数 outbound_type'''
    #return request.config.getoption("--outbound_type")
    outbound=request.config.getoption("--outbound_type")
    return outbound.split('_')[0]