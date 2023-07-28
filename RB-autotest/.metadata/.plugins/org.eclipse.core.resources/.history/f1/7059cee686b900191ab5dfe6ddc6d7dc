"""
Created on 2019/7/25
"""
import pytest
from Demoproject.home import HomePage
from time import sleep
from business import login
from _socket import timeout

@pytest.mark.pre_b2cpc_0
def test_login_search(selenium):
    '''demo测试'''
    h = HomePage(selenium)
    h.go_to_homepage() #打开润吧首页
    sleep(5)
    findBusness = h.driver.find_element_by_css_selector('#businessInvitation > a > span')
    assert findBusness.text == '我要找商机','点击我要招商机类目'
    findBusness.click()
    h.driver.find_element_by_class_name('link-quickview').click()
    loginText = h.driver.find_element_by_css_selector('.login_title > p')
    assert loginText.text == '用户登录','未弹出用户登录页面'
    sleep(2)
    
@pytest.mark.prd_pc_0
def test_01_login(selenium):
    '''登录'''
    l=login.Login(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'

@pytest.mark.prd_pc_0
def test_02_change_role(selenium):
    '''切换到园区角色'''
    l=login.Login(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(2)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'
    
@pytest.mark.prd_pc_0
def test_03_change_role(selenium):
    '''切换企业身份'''
    h = HomePage(selenium)
    h.go_to_homepage() #打开润吧首页    
    l=login.Login(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selectRole = selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(1)>a')
    selectRoleText = selectRole.text
    print("被选择的企业角色：",selectRoleText)
    selectRole.click() #选择企业，点击切换
    sleep(4)
#     h.wait_until_display(By.ID, 10)
    headcurrentRole = selenium.find_element_by_id('headcurrentrole').text
    print("首页显示角色：",headcurrentRole)
    assert selectRoleText == headcurrentRole,'选择服务商，首页显示不是被选择企业'
    

@pytest.mark.prd_pc_0
def test_04_enter_manageUserCenter(selenium):
    '''润吧云首页-进入云管理中心'''
    h = HomePage(selenium)
    h.go_to_homepage() #打开润吧首页    
    l=login.Login(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    selenium.find_element_by_link_text('进入云管理中心').click()
    sleep(2)
    headerTitle = selenium.find_element_by_css_selector('.header > div > div > div > a').text.strip()
    print("云管理中心页面Title:",headerTitle)
    assert '企业管理控制台' in headerTitle,'未进入云管理中心'
    username = selenium.find_element_by_class_name('home-blue').text
    assert '纪金辉' == username,'元管理中心账户名称不是当前用户名或者账户名有变化'
    
@pytest.mark.prd_pc_0
def test_05_businessMemberList(selenium):
    '''基础信息-企业档案-企业档案列表'''
    l=login.Login(selenium)
    h = HomePage(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(2)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'
    h.go_to_homepage(url='http://codemaster.runbaba.com/Business/Member/index')
    business_text = selenium.find_element_by_css_selector('.rightbox > div > div > div:nth-child(1) > div > h5')
    assert '企业档案' == business_text.text.strip(),'未进入企业档案页面'
    members = selenium.find_elements_by_css_selector('.text-gray>a')
    assert len(members)> 8,'企业档案列表。数据量不足8条'
    
    
@pytest.mark.prd_pc_0
def test_06_business_search_companyInfo(selenium):
    '''基础信息-企业档案-查询企业信息'''
    l=login.Login(selenium)
    h = HomePage(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(2)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'
    h.go_to_homepage(url='http://codemaster.runbaba.com/Business/Member/index')
    business_text = selenium.find_element_by_css_selector('.rightbox > div > div > div:nth-child(1) > div > h5')
    assert '企业档案' == business_text.text.strip(),'未进入企业档案页面'
    
    h.searchCompany_info(companyname="上海宝信软件股份有限公司")
    members = selenium.find_elements_by_css_selector('.text-gray>a')
    assert members[0].text == '上海宝信软件股份有限公司','搜索道德企业名称不一样'
    
    
@pytest.mark.prd_pc_0
def test_07_business_addPage(selenium):
    '''基础信息-企业档案-新增页面'''
    l=login.Login(selenium)
    h = HomePage(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(2)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'
    h.go_to_homepage(url='http://codemaster.runbaba.com/Business/Member/index')
    business_text = selenium.find_element_by_css_selector('.rightbox > div > div > div:nth-child(1) > div > h5')
    assert '企业档案' == business_text.text.strip(),'未进入企业档案页面'
    addtext = selenium.find_elements_by_css_selector('.console-title>a')[0]
    if addtext.text !='新增':
        raise("点击入口非新增入口")
    addtext.click()
    sleep(1)
    pagetitle = selenium.find_element_by_class_name('ng-isolate-scope').text.strip()
    assert pagetitle =='企业档案>企业档案新增','新增页面title非预期名称'
    # 新增页面信息字段显示
    addinfos = selenium.find_elements_by_class_name('text-muted')
    assert len(addinfos)>4,'页面显示新增字段缺失'
    assert '会员等级' in addinfos[0].text,'页面未显示会员等级信息'

@pytest.mark.prd_pc_0
def test_08_business_importPage(selenium):
    '''基础信息-企业档案-导入页面'''
    l=login.Login(selenium)
    h = HomePage(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(2)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'
    h.go_to_homepage(url='http://codemaster.runbaba.com/Business/Member/index')
    business_text = selenium.find_element_by_css_selector('.rightbox > div > div > div:nth-child(1) > div > h5')
    assert '企业档案' == business_text.text.strip(),'未进入企业档案页面'
    addtext = selenium.find_elements_by_css_selector('.console-title>a')[1]
    if addtext.text !='导入':
        raise("非导入入口")
    addtext.click()
    sleep(1)
    pagetitle = selenium.find_element_by_class_name('ng-isolate-scope').text.strip()
    assert '会员管理模版下载' in pagetitle,'未显示“会员管理模版下载”'

@pytest.mark.prd_pc_0
def test_09_business_detail(selenium):
    '''基础信息-企业档案-企业信息详情'''
    l=login.Login(selenium)
    h = HomePage(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(2)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'
    h.go_to_homepage(url='http://codemaster.runbaba.com/Business/Member/index')
    business_text = selenium.find_element_by_css_selector('.rightbox > div > div > div:nth-child(1) > div > h5')
    assert '企业档案' == business_text.text.strip(),'未进入企业档案页面'
#     h.searchCompany_info(companyname="上海宝信软件股份有限公司")
    members = selenium.find_elements_by_css_selector('.text-gray>a')
    print("点击查看的企业名称：", members[0].text) 
    checkoutBtns = selenium.find_elements_by_css_selector('.nowrap>a')
    companyName = members[0].text
    if checkoutBtns[0].text != '查看':
        raise("点击的不是查看btn")
    checkoutBtns[0].click()
    currentCompanyName = selenium.find_element_by_css_selector('.row > div > div > h5:nth-child(2)').text
    print("查看企业详情页面：",currentCompanyName)
    assert (companyName in currentCompanyName),'点击查看的企业与企业详情页企业名称不一致，请核查'

@pytest.mark.prd_pc_0
def test_10_business_record_export(selenium):
    '''基础信息-企业档案-企业档案导出列表'''
    l=login.Login(selenium)
    h = HomePage(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(2)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'
    h.go_to_homepage(url='http://codemaster.runbaba.com/Business/Member/index')
    business_text = selenium.find_element_by_css_selector('.rightbox > div > div > div:nth-child(1) > div > h5')
    assert '企业档案' == business_text.text.strip(),'未进入企业档案页面'
    addtext = selenium.find_elements_by_css_selector('.console-title>a')[6]
    if addtext.text !='企业档案导出':
        raise("非企业档案导出入口")
    addtext.click()
    sleep(2)
    pagetitle = selenium.find_element_by_class_name('console-title').text
    assert '企业档案导出' in pagetitle,'未打开企业档案导出页面'

@pytest.mark.prd_pc_0
def test_11_business_search_othercompanyInfo(selenium):
    '''基础信息-企业档案-查询企业信息'''
    l=login.Login(selenium)
    h = HomePage(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(2)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'
    h.go_to_homepage(url='http://codemaster.runbaba.com/Business/Member/index')
    business_text = selenium.find_element_by_css_selector('.rightbox > div > div > div:nth-child(1) > div > h5')
    assert '企业档案' == business_text.text.strip(),'未进入企业档案页面'
    
    h.searchCompany_info(companyname="上海安乐达电器科")
    members = selenium.find_elements_by_css_selector('.text-gray>a')
    assert '上海安乐达电器科' in members[0].text,'搜索到的企业名称不包含搜素信息'

@pytest.mark.prd_pc_0
def test_12_business_InvestigateCompany_list(selenium):
    '''基础信息-企业监管-企业监管列表'''
    l=login.Login(selenium)
    h = HomePage(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(2)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'
    h.go_to_homepage(url='http://codemaster.runbaba.com/Business/InvestigateCompany/index')
    sleep(1)
    business_text = selenium.find_element_by_css_selector('.rightbox > div > div > div:nth-child(1) > div > h5')
    assert '排查企业管理列表' == business_text.text.strip(),'企业监管页面未正确打开'

@pytest.mark.prd_pc_0
def test_13_business_InvestigateCompany_search(selenium):
    '''基础信息-企业监管-查询企业信息'''
    l=login.Login(selenium)
    h = HomePage(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(2)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'
    h.go_to_homepage(url='http://codemaster.runbaba.com/Business/InvestigateCompany/index')
    sleep(1)
    business_text = selenium.find_element_by_css_selector('.rightbox > div > div > div:nth-child(1) > div > h5')
    assert '排查企业管理列表' == business_text.text.strip(),'企业监管页面未正确打开'
    companyname = h.InvestigateCompany_search(companyname='魔都振基资产管理有限公司')
    selenium.find_element_by_name('btn_search').click()
    sleep(1)
    get_result = selenium.find_elements_by_css_selector('.text-gray>a')[0].text
    assert companyname == get_result.strip(),'搜索到企业名称不对'

@pytest.mark.prd_pc_0
def test_14_business_InvestigateCompany_feed_Page(selenium):
    '''基础信息-企业监管-跟踪反馈页面'''
    l=login.Login(selenium)
    h = HomePage(selenium)
    l.login_with_the_user(usernmae='13900000000', password='b12345678')
    searchbar=selenium.find_elements_by_class_name('input-serach')
    assert len(searchbar) > 0,'登录成功到首页显示搜索框'
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('当前角色',role)
    selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
    sleep(1)
    selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
    sleep(2)
    role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
    print('切换后角色',role)
    assert '园区' in role,'切换到园区成功'
    h.go_to_homepage(url='http://codemaster.runbaba.com/Business/InvestigateCompany/index')
    sleep(1)
    business_text = selenium.find_element_by_css_selector('.rightbox > div > div > div:nth-child(1) > div > h5')
    assert '排查企业管理列表' == business_text.text.strip(),'企业监管页面未正确打开'
    h.InvestigateCompany_search(companyname='魔都振基资产管理有限公司')
    selenium.find_element_by_name('btn_search').click()
    sleep(1)
    click_control = selenium.find_elements_by_css_selector('.text-gray>a')[1]
    
    assert click_control.text.strip() in '跟踪反馈 ','定位到的tab不是“跟踪反馈”'
    click_control.click()
    result_info = selenium.find_element_by_class_name('table-viewer-topbar-title').text
    assert '跟踪反馈信息' == result_info,'未跳转到跟踪反馈页面'

# @pytest.mark.prd_pc_0
# def test_15open_business_archives(selenium):
#     '''基础信息-打开企业档案页面'''
#     l=login.Login(selenium)
#     l.login_with_the_user(usernmae='13900000000', password='b12345678')
#     role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
#     print('当前角色',role)
#     selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)>a>.caret').click()
#     sleep(1)
#     selenium.find_element_by_css_selector('#choiceIdentity>li:nth-child(2)>a').click()
#     sleep(3)
#     role = selenium.find_element_by_css_selector('.pull-right>span:nth-child(2)').text.strip()
#     print('切换后角色',role)
#     assert '园区' in role,'切换到园区成功'
#     selenium.get('http://codemaster.runbaba.com/Business/Member/index')
#     selenium.find_element_by_css_selector('#sidemenu0>li>.collapse>li>a').click() #点击企业档案
#     c_search=selenium.find_elements_by_css_selector('.pull-left>.form-control')
#     assert len(c_search)>0,'企业档案页面未打开成功'
    
@pytest.mark.prd_pc_0
def test_15open_owner_file(selenium):
    '''基础信息-打开业主档案页面'''
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
    selenium.get('http://codemaster.runbaba.com/Business/OwnerManagement/index')
    ower_file_search=selenium.find_elements_by_css_selector('.form-group .pull-left>.form-control')
    assert len(ower_file_search)>0,'业主档案页面未打开成功'
#     selenium.find_element_by_css_selector('#sidemenu0>li>a>.arrow').click() #点击基础信息

@pytest.mark.prd_pc_0
def test_16owner_file_search(selenium):
    '''基础信息-打开业主档案页面搜索'''
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
    selenium.get('http://codemaster.runbaba.com/Business/OwnerManagement/index')
    ower_file_search=selenium.find_elements_by_css_selector('.form-group .pull-left>.form-control')
    assert len(ower_file_search)>0,'业主档案页面未打开成功'
    s=selenium.find_element_by_css_selector('.form-group .pull-left>.form-control')
    s.click()
    s.clear()
    s.send_keys('上海市南供电公司')
    sleep(1)
    selenium.find_element_by_id('generalSubmit').click()
    sleep(3)
    s_relust=selenium.find_element_by_css_selector('.table>tbody>tr').text
    print('搜索业主结果',s_relust)
    assert '上海市南供电公司' in s_relust,'成功搜索到结果'
    
@pytest.mark.prd_pc_0
def test_17owner_info_add_page(selenium):
    '''基础信息-打开新增业主企业信息页面'''
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
    selenium.get('http://codemaster.runbaba.com/Business/OwnerManagement/add') #打开新增页面
    new_sign=selenium.find_elements_by_class_name('console-title')
    assert len(new_sign)>0,'新增页面打开成功'
 
@pytest.mark.prd_pc_0
def test_18owner_info_import_page(selenium):
    '''基础信息-打开业主企业信息导入页面'''
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
    selenium.get('http://codemaster.runbaba.com/Business/OwnerManagement/import')
    upload=selenium.find_elements_by_id('asyncTd')
    assert len(upload)>0,'打开导入页面成功'   

@pytest.mark.prd_pc_0
def test_19check_owner_info(selenium):
    '''基础信息-查看业主档案详情信息'''
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
    selenium.get('http://codemaster.runbaba.com/Business/OwnerManagement/index')
    ower_file_search=selenium.find_elements_by_css_selector('.form-group .pull-left>.form-control')
    assert len(ower_file_search)>0,'业主档案页面未打开成功'
    s=selenium.find_element_by_css_selector('.form-group .pull-left>.form-control')
    s.click()
    s.clear()
    s.send_keys('上海市南供电公司')
    sleep(1)
    selenium.find_element_by_id('generalSubmit').click()
    sleep(3)
    s_relust=selenium.find_element_by_css_selector('.table>tbody>tr').text
    print('搜索业主结果',s_relust)
    assert '上海市南供电公司' in s_relust,'成功搜索到结果'
    selenium.find_element_by_css_selector('.nowrap>a').click() #点击查看
    sleep(2)
    info=selenium.find_elements_by_class_name('rowbox')
    assert len(info)>0,'查看具体业主信息页面打开成功'
    
@pytest.mark.prd_pc_0
def test_20garden_inside_file(selenium):
    '''基础信息-打开园中园档案页面'''
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
    selenium.get('http://codemaster.runbaba.com/Business/AgencyManagement/index')
    search_btn=selenium.find_elements_by_css_selector('.pull-left>.form-control') #搜索框
    assert len(search_btn)>0,'打开园中园档案页面成功'
  
@pytest.mark.prd_pc_0
def test_21garden_inside_file_search(selenium):
    '''基础信息-打开园中园档案页面,通过名称筛选具体结果'''
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
    selenium.get('http://codemaster.runbaba.com/Business/AgencyManagement/index')
    search_btn=selenium.find_element_by_css_selector('.pull-left>.form-control') #搜索框
    search_btn.click()
    search_btn.clear()
    search_btn.send_keys('上海润蓝企业管理咨询有限公司')
    selenium.find_element_by_id('generalSubmit').click()
    sleep(3)
    reslut=selenium.find_element_by_css_selector('.table>tbody').text
    print('搜索结果',reslut)
    assert '上海润蓝企业管理咨询有限公司' in reslut,'成功显示搜索 结果'

@pytest.mark.prd_pc_0
def test_22check_garden_inside_file(selenium):
    '''基础信息-打开园中园档案页面,通过名称筛选具体结果,查看企业信息详情'''
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
    selenium.get('http://codemaster.runbaba.com/Business/AgencyManagement/index')
    search_btn=selenium.find_element_by_css_selector('.pull-left>.form-control') #搜索框
    search_btn.click()
    search_btn.clear()
    search_btn.send_keys('上海润蓝企业管理咨询有限公司')
    selenium.find_element_by_id('generalSubmit').click()
    sleep(3)
    reslut=selenium.find_element_by_css_selector('.table>tbody').text
    print('搜索结果',reslut)
    assert '上海润蓝企业管理咨询有限公司' in reslut,'成功显示搜索 结果' 
    selenium.find_element_by_css_selector('.nowrap>a').click()
    sleep(3)
    num=selenium.find_element_by_class_name('simple-table-row').text
    print('园中园编号',num)
    assert '园中园编号' in num,'查看企业信息详情页面未正常显示'



    

if __name__ == '__main__':
    from function import system
    import os
    system.runtc(os.path.basename(__file__),'prd_pc_0',driver='Chrome',
                 options=[]) #Firefox锛孋hrome