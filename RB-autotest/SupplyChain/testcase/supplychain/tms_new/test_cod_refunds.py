'''
# -*- coding: utf-8 -*-
#开发人员:   
#开发日期:   
#文件项目:   
#文件名称:   
 '''

from business.tms.MenuPage import Menu
from business.tms.login import Login
from time import sleep
from business.tms.COD_refunds_upload import Cod_refunds
import pytest
import time



@pytest.mark.Cod_manage
def test_CodRefunds_upload_firsttime(selenium):
    '''未导入订单导入返款数据,并确认返款'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('费用结算', 'COD订单管理')
    upload=Cod_refunds(selenium)
    print('选择未导入订单')
    query_result1=upload.query_order('未导入','')
    do=query_result1[0]
    carrier=query_result1[1]
    refunds1=query_result1[2]
    status1=query_result1[3]
    carrier_code=upload.query_carriercode_by_carriername(carrier)
    print ('当前返款金额：' + refunds1,'\n',
           '当前返款状态：' + status1, sep='')
    excel_path=upload.query_file_path()[0]
    exe_path=upload.query_file_path()[1]
    print ('修改Excel返款金额')
    upload.excel_edit(do,carrier_code,excel_path)
    print ('点击上传返款数据')
    upload.upload_excel_normal(exe_path,excel_path)
    upload.driver.switch_to.default_content()
    upload.query_order('请选择',do)
    print('导入订单确认返款')
    upload_result=upload.Refunds_confirm()
    print('查询导入订单状态')
    refunds2=upload_result[0]
    status2=upload_result[1]
    collect_amout=upload_result[2]
    print ('应收金额：' + collect_amout,'\n',
           '导入返款金额：' + refunds2,'\n',
           '导入返款状态：' + status2,sep='')
    if collect_amout == refunds2 and refunds1 !=refunds2 :
        assert status2 == "已返款"
        print ('返款成功，测试通过')
    elif collect_amout != refunds2 and refunds1 !=refunds2 :
        assert status2 == '异常'
        print ('返款金额与应收金额不一致，返款异常，测试通过')
    else :
        assert status2 == '未导入'
        print ('返款失败，测试不通过')

@pytest.mark.Cod_manage
def test_CodRefunds_upload_doing(selenium):
    '''处理中订单导入返款数据'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('费用结算', 'COD订单管理')
    upload = Cod_refunds (selenium)
    #先导入测试数据----------------
    data=upload.Upload_Refunds_firsttime('未导入')
    do=data
    upload.driver.switch_to.default_content()
    #------------------------------------
    print ('选择处理中订单')
    query_result2 = upload.query_order ('处理中', do)
    carrier=query_result2[1]
    refunds1 = query_result2[2]
    status1 = query_result2[3]
    carrier_code=upload.query_carriercode_by_carriername(carrier)
    print ('当前返款金额：' + refunds1, '\n',
           '当前返款状态：' + status1, sep='')
    excel_path = upload.query_file_path ()[0]
    exe_path = upload.query_file_path ()[1]
    print ('修改Excel返款金额')
    upload.excel_edit (do, carrier_code, excel_path)
    print ('点击上传返款数据')
    upload.upload_excel_normal (exe_path, excel_path)
    upload.driver.switch_to.default_content ()
    upload.query_order ('请选择', do)
    print ('导入订单确认返款')
    upload_result = upload.Refunds_confirm ()
    print ('查询导入订单状态')
    refunds2 = upload_result[0]
    status2 = upload_result[1]
    collect_amout = upload_result[2]
    print ('应收金额：' + collect_amout, '\n',
           '第二次导入后返款金额：' + refunds2, '\n',
           '第二次导入后返款状态：' + status2, sep='')
    #处理中订单导入返款数据，返款金额不会改变
    if  refunds1 == collect_amout  :
        assert refunds1==refunds2 and status2 == "已返款"
        print ('返款成功，测试通过')
    elif collect_amout != refunds1 :
        assert refunds1==refunds2 and status2 == '异常'
        print ('返款金额与应收金额不一致，返款异常，测试通过')
    else :
        assert refunds1!=refunds2 and status2 == '处理中'
        print ('返款失败，测试不通过')
            
@pytest.mark.Cod_manage
def test_CodRefunds_upload_done(selenium):
    '''已返款订单导入返款数据'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('费用结算', 'COD订单管理')
    upload = Cod_refunds (selenium)
    print ('选择已返款订单')
    query_result1 = upload.query_order ('已返款', '')
    do = query_result1[0]
    carrier = query_result1[1]
    refunds1 = query_result1[2]
    status1 = query_result1[3]
    carrier_code = upload.query_carriercode_by_carriername (carrier)
    print ( '当前返款金额：' + refunds1, '\n',
           '当前返款状态：' + status1, sep='')
    excel_path = upload.query_file_path ()[0]
    exe_path = upload.query_file_path ()[1]
    print ('修改Excel返款金额')
    upload.excel_edit (do, carrier_code, excel_path)
    print ('点击上传返款数据')
    upload.upload_excel_normal (exe_path, excel_path)
    upload.driver.switch_to.default_content ()
    upload.query_order ('请选择', do)
    print ('导入订单确认返款')
    upload_result = upload.Refunds_confirm ()
    print ('查询导入订单状态')
    refunds2 = upload_result[0]
    status2 = upload_result[1]
    collect_amout = upload_result[2]
    print ('应收金额：' + collect_amout, '\n',
           '导入返款金额：' + refunds2, '\n',
           '导入返款状态：' + status2, sep='')
    # 已返款订单导入返款数据，返款金额不会改变
    if refunds1 == collect_amout :
        assert refunds1 == refunds2 and status2 == "已返款"
        print ('返款成功，测试通过')
    elif collect_amout != refunds1 :
        assert refunds1 == refunds2 and status2 == '异常'
        print ('返款金额与应收金额不一致，返款异常，测试通过')
    else :
        assert refunds1 != refunds2 and status2 == '处理中'
        print ('返款失败，测试不通过')

@pytest.mark.Cod_manage
def test_CodRefunds_upload_error(selenium):
    '''异常订单通过异常导入功能导入返款数据'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('费用结算', 'COD订单管理')
    upload = Cod_refunds (selenium)
    print ('选择异常订单')
    query_result1 = upload.query_order ('异常', '')
    do = query_result1[0]
    carrier = query_result1[1]
    refunds1 = query_result1[2]
    status1 = query_result1[3]
    carrier_code = upload.query_carriercode_by_carriername (carrier)
    print ('当前返款金额：' + refunds1, '\n',
           '当前返款状态：' + status1, sep='')
    excel_path = upload.query_file_path ()[0]
    exe_path = upload.query_file_path ()[1]
    print ('修改Excel返款金额')
    upload.excel_edit (do, carrier_code, excel_path)
    print ('点击上传返款数据')
    upload.upload_excel_unusual (exe_path, excel_path)
    upload.driver.switch_to.default_content ()
    upload.query_order ('请选择', do)
    print ('导入订单确认返款')
    upload_result = upload.Refunds_confirm ()
    print ('查询导入订单状态')
    refunds2 = upload_result[0]
    status2 = upload_result[1]
    collect_amout = upload_result[2]
    print ('应收金额：' + collect_amout, '\n',
           '导入返款金额：' + refunds2, '\n',
           '导入返款状态：' + status2, sep='')
    #异常订单导入返款数据会更新返款金额
    if refunds1 != refunds2 and collect_amout == refunds2 :
        assert status2 == "已返款"
        print ('返款成功，测试通过')
    elif refunds1 != refunds2 and collect_amout != refunds2:
        assert status2 == '异常'
        print ('返款金额与应收金额不一致，返款异常，测试通过')
    else :
        assert refunds1 == refunds2
        print ('返款失败，测试不通过')

@pytest.mark.Cod_manage
def test_Cod_batchremarks(selenium):
    '''COD订单批量备注'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('费用结算', 'COD订单管理')
    frame = selenium.find_element_by_css_selector ("body > div > div.layui-body > div > div > div > div > iframe")
    print ("切换frame")
    selenium.switch_to.frame (frame)
    sleep (1)
    selenium.find_element_by_xpath ('//*[@id="ra"]/div[2]/div/div/div/input').click ()
    sleep (1)
    print ('选择全部')
    selenium.find_element_by_xpath ('//*[@id="ra"]/div[2]/div/div/dl/dd[1]').click ()
    sleep (1)
    print ("输入出库时间")
    selenium.find_element_by_id ('leaveDcTimeStart').clear ()
    sleep (1)
    selenium.find_element_by_id ('leaveDcTimeStart').send_keys ('2017-04-01 00:00:00')
    selenium.find_element_by_id ("btn-submit").click ()  # 点击查询
    sleep (2)
    first_remark = selenium.find_element_by_xpath (
        '/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[24]/div/a').text
    print (first_remark)
    print ('点击批备')
    selenium.find_element_by_id ("remarks").click ()
    sleep (1)
    tips = selenium.find_element_by_xpath ('//*[@id="layui-layer1"]/div[2]').text
    print (tips)
    print ('点击确定')
    selenium.find_element_by_xpath ('//*[@id="layui-layer1"]/span[1]/a').click ()
    sleep (1)
    print ('全选')
    selenium.find_element_by_xpath (
        '/html/body/div[1]/div/div/div[8]/div[1]/div[3]/div[1]/table/thead/tr/th/div/div/i').click ()
    sleep (1)
    print ('点击批备')
    selenium.find_element_by_id ("remarks").click ()
    sleep (1)
    print ('切换到备注弹窗frame')
    selenium.switch_to_frame (selenium.find_element_by_id ('layui-layer-iframe2'))
    sleep (1)
    print ('输入备注信息')
    now_time = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))
    remark_text = "自动化测试 " + now_time
    selenium.find_element_by_name ('remark').send_keys (remark_text)
    sleep (1)
    print ('点击保存')
    selenium.find_element_by_id ('btn-submit').click ()
    sleep (2)
    print ("切换到主界面frame")
    selenium.switch_to.frame (frame)
    sleep (1)
    second_remark = selenium.find_element_by_xpath (
        '/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[24]/div/a').text
    print ('备注信息为：' + second_remark)
    assert remark_text == second_remark 
    print ('批量备注成功，测试通过')
    
@pytest.mark.Cod_manage_1
def test_Cod_Refunds_onekey(selenium):
    '''COD一键返款'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('费用结算', 'COD订单管理')
    upload=Cod_refunds(selenium)
    #先导入测试数据----------------
    upload.Upload_Refunds_firsttime('未导入')
    upload.driver.switch_to.default_content()
    #------------------------------------
    data=upload.query_order('处理中','')
    do=data[0]
    status1=data[3]
    batch_no=data[5]
    print ('订单DO：' + do)
    print ('批次号：' + batch_no)
    print ('返款状态：' + status1)
    sleep (1)
    upload.refunds_onekey()
    upload.driver.switch_to.default_content()
    result=upload.query_order('请选择','')
    status2=result[3]
    print ('初始返款状态：' + status1)
    print ('一键返款状态：' + status2)
    assert status2 == '异常' or status2 == '已返款'
    print ('一键返款成功，测试通过')

@pytest.mark.Cod_manage
def test_Cod_Refunds_confirm(selenium):
    '''COD确认返款，校验返款状态'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('费用结算', 'COD订单管理')
    frame = selenium.find_element_by_css_selector ("body > div > div.layui-body > div > div > div > div > iframe")
    print ("切换frame")
    selenium.switch_to.frame (frame)
    sleep (1)
    selenium.find_element_by_xpath ('//*[@id="ra"]/div[2]/div/div/div/input').click ()
    sleep (1)
    print ('选择全部')
    selenium.find_element_by_xpath ('//*[@id="ra"]/div[2]/div/div/dl/dd[1]').click ()
    # print('选择未导入订单')
    # selenium.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/dl/dd[2]').click()
    sleep (1)
    print ("输入出库时间")
    selenium.find_element_by_id ('leaveDcTimeStart').clear ()
    selenium.find_element_by_id ('leaveDcTimeStart').send_keys ('2017-04-01 00:00:00')
    print ("点击查询")
    selenium.find_element_by_id ("btn-submit").click ()
    sleep (3)
    a = selenium.find_element_by_xpath ('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[4]/div').text
    sleep (1)
    b = selenium.find_element_by_xpath ('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[17]/div').text
    print ('do单号：' + a)
    print ('返款状态：' + b)
    print ('勾选订单')
    selenium.find_element_by_xpath (
        '/html/body/div[1]/div/div/div[8]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td/div/div/i').click ()
    sleep (1)
    print ('点击返款')
    selenium.find_element_by_id ('confirm').click ()
    sleep (2)
    selenium.find_element_by_name ("code").send_keys (a)
    sleep (1)
    selenium.find_element_by_xpath ('//*[@id="ra"]/div[2]/div/div/div/input').click ()
    sleep (1)
    selenium.find_element_by_name ("code").click ()

    # print('选择全部')
    # selenium.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/dl/dd[1]').click()
    # sleep(1)
    print ("点击查询")
    selenium.find_element_by_id ("btn-submit").click ()
    sleep (3)
    status = selenium.find_element_by_xpath (
        '/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[17]/div').text
    if b == '异常' or b == '未导入' or b == '已返款' :
        assert status == b
        print ('BEGIN_STATUS：' + b, "END_STATUS：" + status)
        print ('---------测试通过---------')
    else:
        assert status== '已返款' or status =='异常'
        print ('BEGIN_STATUS：' + b, "END_STATUS：" + status)
        print ('---------测试通过---------')
        
@pytest.mark.Cod_manage
def test_Cod_Remarks_Edit(selenium):
    '''COD订单编辑备注'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('费用结算', 'COD订单管理')
    frame = selenium.find_element_by_css_selector ("body > div > div.layui-body > div > div > div > div > iframe")
    print ("切换frame")
    selenium.switch_to.frame (frame)
    sleep (1)
    selenium.find_element_by_xpath ('//*[@id="ra"]/div[2]/div/div/div/input').click ()
    sleep (1)
    print ('选择全部')
    selenium.find_element_by_xpath ('//*[@id="ra"]/div[2]/div/div/dl/dd[1]').click ()
    sleep (1)
    print ("输入出库时间")
    selenium.find_element_by_id ('leaveDcTimeStart').clear ()
    sleep (1)
    selenium.find_element_by_id ('leaveDcTimeStart').send_keys ('2017-04-01 00:00:00')
    selenium.find_element_by_id ("btn-submit").click ()  # 点击查询
    sleep (2)
    print ('点击备注')
    do = selenium.find_element_by_xpath (
        '/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr[1]/td[4]/div').text
    first_remark = selenium.find_element_by_xpath (
        '/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[24]/div/a')
    print (do)
    print (first_remark.text)
    first_remark.click ()
    sleep (2)
    print ('切换到备注弹窗frame')
    selenium.switch_to_frame (selenium.find_element_by_id ('layui-layer-iframe1'))
    sleep (1)
    print ('输入备注信息')
    now_time = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))
    remark_text = "自动化测试编辑备注 " + now_time
    # selenium.find_element_by_name('remark').send_keys(Keys.ENTER)
    selenium.find_element_by_name ('remark').clear ()
    selenium.find_element_by_name ('remark').send_keys (remark_text)
    sleep (1)
    print ('点击保存')
    selenium.find_element_by_id ('btn-submit').click ()
    sleep (2)
    print ("切换到主界面frame")
    selenium.switch_to.frame (frame)
    sleep (1)
    selenium.find_element_by_name ('code').send_keys (do)
    sleep (1)
    selenium.find_element_by_id ("btn-submit").click ()  # 点击查询
    sleep (2)
    second_remark = selenium.find_element_by_xpath (
        '/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[24]/div/a').text
    print ('备注信息为：' + second_remark)
    assert remark_text == second_remark
    print ('编辑备注成功，测试通过')


@pytest.mark.Cod_manage
def test_Cod_Refunds_Sum(selenium):
    '''返款数据汇总校验'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('费用结算', 'COD汇总对账')
    frame = selenium.find_element_by_css_selector ("body > div > div.layui-body > div > div > div > div > iframe")
    print ("切换frame")
    selenium.switch_to.frame (frame)
    sleep (1)
    selenium.find_element_by_id ("btn-submit").click ()  # 点击查询
    sleep (2)
    DO = selenium.find_elements_by_xpath ('/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[3]/div')
    order_amount = selenium.find_elements_by_xpath (
        '/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[11]/div')
    fright_fee = selenium.find_elements_by_xpath ('/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[13]/div')
    to_collect_amount = selenium.find_elements_by_xpath (
        '/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[14]/div')
    Refund_amount = selenium.find_elements_by_xpath (
        '/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[15]/div')
    '''DO'''
    print ('   DO   ：', end="")
    for do in DO :
        print (do.text, end=" ")
    print ('\n')

    '''订单金额'''
    print ('订单金额：', end="")
    order_amount_Sum1 = 0
    for a in order_amount :
        order_amount_Sum1 += int (a.text)
        print (a.text, end="  ， ")
    print ('订单总金额：', order_amount_Sum1)

    '''运费'''
    print ('运    费：', end="")
    fright_fee_Sum1 = 0
    for b in fright_fee :
        fright_fee_Sum1 += int (b.text)
        print (b.text, end="  ， ")
    print ('运费总金额：', fright_fee_Sum1)

    '''应收金额'''
    print ('应收金额：', end="")
    to_collect_amount_Sum1 = 0
    for c in to_collect_amount :
        to_collect_amount_Sum1 += int (c.text)
        print (c.text, end="  ， ")
    print ('应收总金额：', to_collect_amount_Sum1)

    '''返款金额'''
    print ('返款金额：', end="")
    Refund_amount_Sum1 = 0
    i = ''
    for d in Refund_amount :
        if d.text == i :
            m = 0
        else :
            m = d.text
        Refund_amount_Sum1 += int (m)
        print (m, end="  ， ")
    print ('返款总金额：', Refund_amount_Sum1)
    sleep (2)
    order_amount_Sum2 = int (selenium.find_element_by_xpath ('//*[@id="layui-laypage-2"]/span[6]').text)
    fright_fee_Sum2 = int (selenium.find_element_by_xpath ('//*[@id="layui-laypage-2"]/span[9]').text)
    to_collect_amount_Sum2 = int (selenium.find_element_by_xpath ('//*[@id="layui-laypage-2"]/span[12]').text)
    Refund_amount_Sum2 = int (selenium.find_element_by_xpath ('//*[@id="layui-laypage-2"]/span[15]').text)
    assert order_amount_Sum1 == order_amount_Sum2 \
            and fright_fee_Sum1 == fright_fee_Sum2 \
            and to_collect_amount_Sum1 == to_collect_amount_Sum2 \
            and Refund_amount_Sum1 == Refund_amount_Sum2 
    print (order_amount_Sum2, fright_fee_Sum2, to_collect_amount_Sum2, Refund_amount_Sum2)
    print ("汇总金额相等，测试通过")



if __name__ == '__main__':
    from public import test
    test.runtc(__file__,  tclevel='Cod_manage_1', driver='Chrome')  # Firefox，Chrome

