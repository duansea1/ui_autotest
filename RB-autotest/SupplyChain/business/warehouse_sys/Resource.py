
from selenium.webdriver.common.by import By

username = 'admin'
password = 'admin123'
    
class Login:
    username = By.ID, "loginForm:userName", "用户名"
    password = By.ID, "loginForm:password", "用户密码"
    warehouse = By.ID, "loginForm:warehouse", "仓库选择框"
    login_button= By.ID, "loginForm:submitBtn", "登录按钮"
    
    login_info = By.ID, "topRightForm", "登录用户信息"
    
class Normal:
    message = By.CLASS_NAME, "rich-messages-label", "返回消息"
    
class DeliveryList:
    start_do_input = By.CSS_SELECTOR, "#searchForm>table>tr>td:nth-child(2)>input", "开始发货单号" #请不要更改为name定位，已知：name值经常改变
    end_do_input = By.CSS_SELECTOR, "#searchForm>table>tr>td:nth-child(4)>input", "开始发货单号" #请不要更改为name定位，已知：name值经常改变
    
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    result_items = By.CSS_SELECTOR, "#selectForm:resultTable:tb>tr","查询结果dom元素"
    
    status_head= By.CSS_SELECTOR, "rich-table-subheadercell:nth-child(4)", "发运订单状态-标题"
    status_content = By.CSS_SELECTOR, "#selectForm:resultTable:tb>tr>td:nth-child(4)", "发运订单状态-内容" #请不要更改为id定位，已知：id值经常改变
    
class DoAllocate:
    '''订单分配页'''
    start_do_input = By.CSS_SELECTOR, "#searchForm>table>tr>td:nth-child(2)>input", "开始发货单号" #请不要更改为name定位，已知：name值经常改变
    end_do_input = By.CSS_SELECTOR, "#searchForm>table>tr>td:nth-child(4)>input", "开始发货单号" #请不要更改为name定位，已知：name值经常改变
    
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    result_items = By.CSS_SELECTOR, "#selectForm:resultTable:tb>tr","查询结果dom元素"
    
    status_head= By.CSS_SELECTOR, "rich-table-subheadercell:nth-child(3)", "发运订单状态-标题"
    status_content = By.CSS_SELECTOR, "#selectForm:resultTable:tb>tr>td:nth-child(3)", "发运订单状态-内容" #请不要更改为id定位，已知：id值经常改变
    
    
class Recheck:
    recheck_record= By.ID, "reCheckRecords:0:j_id708", "核拣"
    
    

class DeliveryOrder:
    """发货单"""
    # start_do = By.CSS_SELECTOR, "#searchForm>table>tody>tr>td:nth-child(2)>input", "开始发货单号"
    # end_do = By.CSS_SELECTOR, "#searchForm>table>tody>tr>td:nth-child(4)>input", "结束发货单号"
    # isYCorder = By.CSS_SELECTOR, '#searchForm>table>tbody>tr:nth-child(3)>td:nth-child(11)>input', 'B端订单checkbox'
    start_do = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input", "开始发货单号"
    end_do = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[1]/td[4]/input", "结束发货单号"
    isYCorder = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[3]/td[11]/input", 'B端订单checkbox'
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    result = By.XPATH, "//tbody[@id='selectForm:resultTable:tb']/tr", "查询结果"
    do_status = By.XPATH, "//tbody[@id='selectForm:resultTable:tb']/tr/td[4]", 'DO状态'
    # 获取波次编号
    wave_id = By.XPATH, "//tbody[@id='selectForm:resultTable:tb']/tr/td[18]", "波次编号"


class OrderDistribution:
    """订单分配"""
    start_do = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input", "开始发货单号"
    end_do = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[1]/td[4]/input", "结束发货单号"
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    result = By.XPATH, "//tbody[@id='selectForm:resultTable:tb']/tr", "查询结果"
    all_selected = By.XPATH, "//tr[@class='rich-table-subheader']/th[1]/div/input", "全选"
    dispatch_button = By.ID, "buttonToolForm:btnQuery2", "分配按钮"


class WaveGeneration:
    """生成波次"""
    do_num = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input", "查找发货单号"
    isYCorder = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[5]/td[10]/input", 'B端订单checkbox'
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    result = By.XPATH, "//tbody[@id='selectForm:resultTable:tb']/tr", "查询结果"
    select_checkbox = By.XPATH, "//tr[@class='rich-table-row rich-table-firstrow listTableSingular']/td[1]/input", "checkbox"
    generate_button = By.ID, "buttonToolForm:btnQuery2", "勾选订单生成波次"


class WavePlan:
    """波次计划"""
    start_wave = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input", "开始波次编号"
    end_wave = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[1]/td[4]/input", "结束波次编号"
    isYCorder = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[4]/td[7]/input[2]", 'B端订单checkbox'
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    result = By.XPATH, "//tr[@class='rich-table-row rich-table-firstrow listTableSingular']", "查询结果"
    wave_link_1st = By.XPATH, "//tr[@class='rich-table-row rich-table-firstrow listTableSingular']/td[2]/a", "波次编号link 1st"
    wave_link_2nd = By.XPATH, "//div[@class='tableContainer']/table/tbody/tr[3]/td[2]/a", "波次编号link 2nd"
    pick_id = By.XPATH, "//div[@class='rich-panel-body ']/table/tbody/tr/td[2]/a", "拣货单号"


class PickConfirm:
    """拣货确认"""
    pick_id = By.ID, "dataForm:pickNoInput", "拣货单号"
    work_no = By.ID, "dataForm:pickInput", "工号"
    equipment_no = By.ID, "dataForm:facilityInput", "拣货设施"


class Sorting:
    """分拣"""
    wave_id = By.ID, "searchForm:waveNo", "波次号"
    sort_button = By.ID, "searchForm:btnSeed1", "按波次强制分拣"


class Encasement:
    """核拣装箱"""
    do_num = By.ID, "searchForm:orderNoInput", "发货单号"
    search_button = By.ID, "searchForm:doSearchBtn", "确定按钮"
    order_detail = By.CSS_SELECTOR, 'input[value="查看订单明细"]', "查看订单明细'"
    product_id = By.XPATH, "//table[@id='reCheckRecords']/tbody/tr[1]/td[6]", "获取产品条码"
    close_button = By.ID, "hidelink", "关闭窗口"
    select_checkbox = By.ID, "setScanMethodCB", "checkbox"
    product_input = By.ID, "newProductBarCode", "输入产品条码"
    carton_qty = By.ID, "confirmCartonQtyPanelSubview:cartonQtyInput", "箱数"
    confirm_encase = By.ID, "confirmCartonQtyPanelSubview:confirmPackedNumForm:doConfirmCartonQtyBtn", "确认装箱"
    result = By.XPATH, "//td[@id='resultForm:face_info']/table/tbody/tr/td/div/table/tbody/tr", "查询结果"
    carton_no = By.XPATH, "//td[@id='resultForm:face_info']/table/tbody/tr/td/div/table/tbody/tr[2]/td[3]/a", "箱号"
    # 获取箱号
    recheck_detail = By.ID, "'queryReCheckLink", "查询核拣记录"
    order_no = By.ID, "searchForm:orderNo", ""
    submit_button = By.ID, "submitBtn", ""


class Handover:
    """出库交接"""
    do_manual_handover = By.XPATH, "//form[@id='buttonToolForm']/span[10]/span/a", "DO人工交接"
    save_button = By.XPATH, "//form[@id='addForm']/table/tbody/tr[2]/td/div/input[1]", "保存按钮"
    carton_no = By.ID, "addDetailForm:carrierNo", "输入箱号"
    close_button = By.XPATH, "//form[@id='addForm']/table/tbody/tr[2]/td/div/input[4]", "关闭交接单"
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    handover_status = By.XPATH, "//div[@id='loadForm:dataDiv']/table/tbody/tr/td[4]", "交接状态"


