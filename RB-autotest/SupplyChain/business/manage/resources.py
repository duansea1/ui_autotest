#-*- coding: utf-8 -*-
'''
Created on 2018年9月14日

@author: geqiuli
'''

from selenium.webdriver.common.by import By

class Managehome:
    login_button = (By.CLASS_NAME, 'login_btn', '登录按钮')
    
    platform_selector = (By.ID,'business_type', '选择平台')
    platform_submit_btn = (By.CSS_SELECTOR, '.submit_btn>button', '选择平台确定按钮')
    
    current_work_plat = (By.CSS_SELECTOR, '.header-tab>li.active')
    work_plat = (By.CSS_SELECTOR, '.header-tab>li', '工作台')
    more_system = (By.CSS_SELECTOR,'.title-more > .more', '我的系统-更多')
    
    sub_system = (By.CSS_SELECTOR, 'a>div', '子系统') 
    sub_system_image = (By.CLASS_NAME, 'manager_img', '子系统图片')
    child_system = (By.CSS_SELECTOR, '#container_body > div > div > a > div > p', '子系统图片') 
    
    my_systems = (By.CSS_SELECTOR,'.dialog-content-main > ul > li > a','我的系统-更多中的子系统')

class YaoexManage:
    yaoex_first_level = (By.CSS_SELECTOR,'div.leftsidebar_box > div > dl > dt','一级菜单')
    yaoex_all_level= (By.CSS_SELECTOR,'div.leftsidebar_box > div > dl > ul.lev-1 > li> a','二级菜单容器')
    spu_code = (By.ID,'spuCode')
    active_id = (By.ID,'buyId')
    query = (By.ID,"query")
    select_option = (By.ID,'pcShow','查询页面频道展示下拉框')
    select_shop = (By.ID,'sellerShow','查询页面活动商家下拉框')
    shop_select_all = (By.ID,'.checkAll','活动商家选择所有')
    save_active = (By.ID,'saveBuyActivity','一起购保存活动')
    create_btn = (By.ID,'add','创建一起购活动按钮')
    product_code = (By.ID,'product_code','商品编码')
    
    upload_button =By.CSS_SELECTOR, 'button[onclick^="uploadLoad"]', '上传按钮'
    upload_pop_addimg = By.CSS_SELECTOR, 'object.swfupload', '上传图片弹框中添加图片按钮'
    upload_pop_confirm = By.CSS_SELECTOR, '#insertAll', '上传图片弹框中确定按钮'
    upload_pop_upload = By.CSS_SELECTOR, '#btnUpload', '上传图片弹框中上传按钮'
    
class ErpSystem:
    menu_first_level = (By.CSS_SELECTOR, '#page_accordion>.l-accordion-header>.l-accordion-header-inner>p', '一级菜单')
    menubtn_first_level = (By.CSS_SELECTOR, '#page_accordion>.l-accordion-header>.l-accordion-toggle', '一级菜单展开按钮')
    
    menu_second_container = (By.CSS_SELECTOR, '#page_accordion>.l-accordion-content', '二级菜单容器')
    menu_second_level = (By.CSS_SELECTOR, '#page_accordion>.l-accordion-content')
    
    current_tab = (By.CSS_SELECTOR, '#framecenter>div>ul>li.l-selected', '当前tab页')
    
    
class Yaoex_sp_manage:
    father_menu = (By.CSS_SELECTOR, '#menuInit > li > a', '药城自营后台-一级菜单')
    child_menu = (By.CSS_SELECTOR, '#menuInit > li > ul.sub > li > a', '药城自营后台-二级菜单')
    
    merchants_id = (By.ID, 'merchants','选择自营公司id')
    
    promotion_tab = (By.CSS_SELECTOR, '#myTab > li > a', '促销活动tab')
    
    creat_promotin = (By.ID, 'addPromotion','新增活动按钮')
    title = (By.CSS_SELECTOR,'.breadcrumb > li.active ','活动标题')
    promotion_Name = (By.ID, 'promotionName','活动名称')
    beginTime = (By.ID, 'beginTime','点击活动开始时间')
    endTime = (By.ID, 'endTime','点击活动结束时间')
    
    time_iframe = (By.CSS_SELECTOR, 'body > div:nth-child(3) > iframe', '时间控件iframe')
    time_dptoday = (By.ID, 'dpTodayInput', '今天按钮')
    time_dpok = (By.ID, 'dpOkInput', '确定按钮')
    time_year = (By.CSS_SELECTOR,'#dpTitle > div:nth-child(4) > input', '输入框-年')
    time_month = (By.CSS_SELECTOR, '#dpTitle > div:nth-child(3) > input', '输入框-月')
    
    chose_customer_group = (By.CSS_SELECTOR,'.form-group > .col-xs-5 > .chose','选择客户组按钮')
    input_group = (By.ID, 'groupname', '输入客户组')
    search_btn = (By.ID, 'search', '搜素按钮')
    customer_group = (By.CSS_SELECTOR,'.table-box >tbody >tr > td:nth-child(1)','选中客户组')
    submit_btn =(By.ID,'submitBtn','确定按钮')
    
    upload =(By.CSS_SELECTOR,'.form-group > .col-xs-3 > button','上传按钮')
    priceVisible = (By.ID, 'priceVisible', '价格对未登录客户展示')
    createPromotion_btn = (By.CSS_SELECTOR, '.padding-t-10 > #createPromotion','创建活动按钮')
    
    editor_promotion = (By.CSS_SELECTOR, '#promotionBody > tr > td > a','编辑促销活动')
    editor_merchant = (By.CSS_SELECTOR,'#promotionBody > tr > td > button','编辑商品')
    
    productCode = (By.ID,'productCodeCompany','本公司商品编码')
    search_tab1 = (By.ID,'search_tab1','search_tab1','添加商品的搜索按钮')
    all_check_tab1 = (By.ID,'all_check_tab1','全选中-复选框')
    add_btn = (By.CSS_SELECTOR, '#tab1_tbody > tr > td:nth-child > a', '单个商品的添加按钮')
    all_add_btn = (By.ID,'batchAddProductBtn','全部添加按钮')
    confirm = (By.CSS_SELECTOR,'.alertm1 > p > button','弹框确认按钮')
    
    already_add_tab = (By.CSS_SELECTOR,"a[href='#tab2']",'已添加的商品tab')
    
class cms_activity:
    #cms活动
    cms_name = By.ID, 'names', '活动名称'
    cms_begintime = By.ID, 'dueBegintime', '活动开始时间'
    cms_endtime = By.ID, 'dueEndtime', '活动结束时间'
    time_dpok = By.ID, 'dpOkInput', '确定按钮'
    time_year = By.CSS_SELECTOR, '#dpTitle > div:nth-child(4) > input', '输入框-年'
    time_month = By.CSS_SELECTOR, '#dpTitle > div:nth-child(3) > input', '输入框-月'

    activity_system = By.ID, 'zhengshiStyle1','普通系统'
    activity_manual = By.ID, 'zhengshiStyle2','普通手动'

    save_btn = By.ID, 'save', '保存按钮'
    confirm = By.CSS_SELECTOR, '.alertm >p > #confirm','弹框确认按钮'


