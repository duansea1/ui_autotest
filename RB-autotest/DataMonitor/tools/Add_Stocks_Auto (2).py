'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-06-17
#文件项目:   自动添加库存
#文件名称:   实时监测药城药网使用评率最高商品，自动添加库存
 '''

import pymysql
import time
import cx_Oracle as oracle
from public.mysql_opr import query_mysql


warehouse_list = ('10', '13', '15', '20', '30')
yc_order_dbinfo = {"host" : "10.6.168.14","user" : "yc_order","password" : "d41d8cd98f00b204","port" : 3306,"data" : "yc_order"}
yw_order_dbinfo = {"host" : "10.6.168.13","user" : "order5","password" : "d41d8cd98f00b204","port" : 3306,"data" : "kubaorder"}
pms_dbinfo = {"host" : "mysql.test.yiyaowang.com","user" : "yao","password" : "d41d8cd98f00b204","port" : 3306,"data" : "yao"}
gss_dbinfo = {"host" : "10.6.168.13","user" : "store","password" : "d41d8cd98f00b204","port" : 3306,"data" : "store"}




def query_hotsell_product():
    '''查询药城药网使用评率最高的商品编码'''
    Item_no1=[]
    date_now=time.strftime ('%Y-%m-%d', time.localtime ())
    now = time.time ()  # 当前时间戳
    twl = now - 30 * 24 * 60 * 60  # 30天前的时间戳
    year = str (time.localtime (twl)[0])  # 从30天前时间结构体中提取年
    mon = str (time.localtime (twl)[1])  # 从30天前时间结构体中提取月
    day = str (time.localtime (twl)[2])  # 从30天前时间结构体中提取日
    date_month_ago = year + '-' + mon + '-' + day
    #---------------------------------YC-----------------------------------
    cust_name='%'+'测试终端自动化'+'%'
    supply_id=('8353','125476','134428')
    args = ','.join (supply_id)
    yc_sql = "select a.product_id,a.product_code,a.product_name,a.short_name," \
          "sum(case when b.cust_name like '%s'  then 1 else 0 end) as '自动化下单次数'," \
          "sum(case when b.cust_name not like '%s'  then 1 else 0 end) as '非自动化下单次数' " \
          "from t_order_detail a " \
          "INNER JOIN t_order b on a.order_id = b.order_id " \
          "WHERE (b.create_time BETWEEN '%s' and '%s') " \
          "AND b.supply_id in (%s) " \
          "GROUP BY a.product_id " \
          "ORDER BY count(a.product_id) desc limit 50 "%(cust_name,cust_name,date_month_ago,date_now,args)
    result1 = query_mysql (yc_order_dbinfo['host'], yc_order_dbinfo['user'], yc_order_dbinfo['password'], yc_order_dbinfo['port'], yc_order_dbinfo['data'],sql=yc_sql)
    for i in range(0,len(result1['data'])):
        Item_no1.append((result1['data'][i])[1])
    print('药城热销商品编码Item_no1：','\n',Item_no1)
    print('药城热销商品个数：',len(Item_no1))

    #---------------------------------YW-----------------------------------
    Item_no2=[]
    yw_sql = "SELECT a.GOODS_NAME,a.PRODUCT_NO,COUNT(*) from sd_sales_list a " \
          "INNER JOIN sd_sales_order b on a.SALES_ORDER_ID = b.SD_SALES_ORDER_ID " \
          "WHERE (a.UPDATE_TIME BETWEEN '%s' and '%s' ) " \
          "and b.ORDER_SOURCE_TYPE ='A3A' " \
          "group by a.GOODS_NAME,a.PRODUCT_NO " \
          "ORDER BY count(*) desc limit 30"%(date_month_ago,date_now)
    result2 = query_mysql (yw_order_dbinfo['host'], yw_order_dbinfo['user'], yw_order_dbinfo['password'], yw_order_dbinfo['port'], yw_order_dbinfo['data'],sql=yw_sql)
    for i in range(0,len(result2['data'])):
        Item_no2.append((result2['data'][i])[1])
    print('药网热销商品编码Item_no2：','\n',Item_no2)
    print('药网热销商品个数：',len(Item_no2))
    set1 = set (Item_no1)#将列表转换为集合
    set2 = set (Item_no2)
    same_item=set1&set2#找出相同的商品编码
    print('相同的商品编码为：','\n',same_item)
    Item_list=list(set(Item_no1+Item_no2))
    print('合并后的商品编码Item_no：','\n',Item_list,'\n','合并后商品编码个数：',len(Item_list))
    return Item_list

def query_ItemNo_BY_SkuNo(item_no):
    '''根据商品编码查询产品编码'''
    #item_list=query_hotsell_product()
    item_list=tuple(item_no)
    #print('商品编码',item_no)
    #print(len(item_no))
    args = ','.join (item_list)
    select_sku_no="SELECT item_no,product_code from pms_merchant_product where item_no in (%s) group by item_no,product_code"%(args)
    result = query_mysql (pms_dbinfo['host'], pms_dbinfo['user'], pms_dbinfo['password'], pms_dbinfo['port'], pms_dbinfo['data'],sql=select_sku_no)
    sku_no=[]
    item_valid=[]
    for i in range(0,len(result['data'])):
        sku_no.append((result['data'][i])[1])
        item_valid.append((result['data'][i])[0])
    print('WMS产品编码:','\n',sku_no,'\n','产品编码个数',len(sku_no))
    set1 = set (item_no)  # 将列表转换成集合
    set2 = set (item_valid)
    invalid_item=set1 ^ set2
    print ('后台无效的商品编码:','\n',invalid_item,'\n','无效的商品编码个数：','\n',len(invalid_item))  # 不同元素
    return sku_no


#def Add_stocks_auto():
def Not_enough_stock_frontend(item_list,warehouse_list,min_stocks):
    '''查询前端库存不足的品'''
    #item_list = query_hotsell_product()
    item_no=tuple(item_list)
    args_1 = ','.join (item_no)
    args_2 = ','.join (warehouse_list)
    select = "select product_no,available_qty,freeze_qty,storage from store_product_stock " \
             "where product_no in (%s) and storage in (%s) " \
             "group by product_no,storage" % (args_1, args_2)
    result = query_mysql (gss_dbinfo['host'], gss_dbinfo['user'], gss_dbinfo['password'], gss_dbinfo['port'], gss_dbinfo['data'],sql=select)

    Not_enough_stock_item_no = []
    Not_enough_stock_warehouse_id = []
    Not_enough_stock=[]
    data=[]
    for i in range(0,len(result['data'])):
        available_qty=(result['data'][i])[1]
        freeze_qty = (result['data'][i])[2]
        if available_qty-freeze_qty <=min_stocks:
            #print (available_qty - freeze_qty)
            Not_enough_stock_item_no.append((result['data'][i])[0])
            Not_enough_stock_warehouse_id.append ((result['data'][i])[3])
            Not_enough_stock.append(str(available_qty-freeze_qty))
    #print(Not_enough_stock_sku_id,'\n',Not_enough_stock_warehouse_id,'\n',Not_enough_stock)
    for j in range(0,len(Not_enough_stock_item_no)):
        stocks_detail=(Not_enough_stock_item_no[j],Not_enough_stock_warehouse_id[j],Not_enough_stock[j])
        data.append(stocks_detail)
    #data = dict (zip (Not_enough_stock_sku_id, Not_enough_stock_warehouse_id))
    poor_stocks_item_qty=len (Not_enough_stock_item_no)
    return data,poor_stocks_item_qty


def Not_enough_stock_backend(item_list,warehouse_list,min_stocks):
    '''查询WMS库存不足的品'''
    #item_no=['0009713513', '0009714754']
    #item_list = query_hotsell_product()
    #item_no=tuple(item_list)
    sku_no=query_ItemNo_BY_SkuNo(item_list)
    args_1 = ','.join (warehouse_list)
    args_2 = ','.join (sku_no)
    wms_oracle = oracle.connect ('WMS_SH_YW', 'WMS_SH_YW', '10.6.84.20:1521/WMSOracle')
    # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
    print ('WMS-Oracle数据库:连接成功')
    cursor = wms_oracle.cursor ()  # 使用cursor()方法获取操作游标
    '''查询SKU_ID'''
    select_sku_id = 'SELECT id from MD_SKU where product_code in (%s) order by id desc' % (args_2)
    cursor.execute (select_sku_id)
    result2 = cursor.fetchall ()
    sku_list=[]
    all_stocks_list=[]
    for m in range(0,len(result2)):
        sku1=str((result2[m])[0])
        sku_list.append(sku1)
        for warehouse_id in warehouse_list:
            all_stocks_tuple=(sku1,warehouse_id)
            all_stocks_list.append(all_stocks_tuple)
    #sku_id = (result2[0])[0]
    #print('SKU_id:',sku_list)
    #print('SKUid个数',len(sku_list))
    #print('SKUID——list',sku_list)
    #print(2,all_stocks_list)
    #print(1,len(all_stocks_list))

    sku_id=tuple(sku_list)
    #print(sku_id)
    args_3 = ','.join (sku_id)
    select_store_now=\
        'SELECT sku_id,sum(qty_available),warehouse_id from STK_BATCH_LOC_LPN where sku_id in (%s) and warehouse_id in (%s) group by sku_id,warehouse_id order by sku_id desc'%(args_3,args_1)
    cursor.execute (select_store_now)
    result3 = cursor.fetchall ()
    #print ('库存信息',result3)
    #print(len(result3))
    print('查询仓库没有库存信息的品')
    stock_info=[]
    for m in range(0,len(result3)):
        sku2=str((result3[m])[0])
        warehouse_id2=str((result3[m])[2])
        stock_tuple=(sku2,warehouse_id2)
        stock_info.append(stock_tuple)
    #print(3,stock_info)
    #print('查询的库存SKUID',stock_sku_id)
    set1 = set (all_stocks_list)#将列表转换为集合
    set2 = set (stock_info)
    different_sku_id=list(set1 ^ set2)#找出不同的商品编码
    print('WMS没有库存信息的SKUid:',different_sku_id)
    Not_enough_stock_sku_id=[]
    Not_enough_stock_warehouse_id=[]
    Not_enough_stock=[]
    data=[]
    for i in range(0,len(result3)):
        stock=(result3[i])[1]
        if stock<=min_stocks:
            Not_enough_stock_sku_id.append(str((result3[i])[0]))
            Not_enough_stock_warehouse_id.append(str((result3[i])[2]))
            Not_enough_stock.append((result3[i])[1])
    for j in range(0,len(Not_enough_stock_sku_id)):
        stocks_detail1=(Not_enough_stock_sku_id[j],Not_enough_stock_warehouse_id[j],Not_enough_stock[j])
        data.append(stocks_detail1)

    if len(different_sku_id)>0:
        for m in range(0,len(different_sku_id)):
            #for warehouse_id in warehouse_list:
                #print(different_sku_id[m],type(different_sku_id[m]))
               # print(warehouse_id)
                stock_qty=('0',)
                stocks_detai2 = (different_sku_id[m]+stock_qty)
                #print(stocks_detai2)
                data.append(stocks_detai2)
    else:
        print('WMS没有库存信息的SKUid个数为0')
    #print(5,data2)
    # print(type((data2[0])[0]),type((data2[0])[1]),type((data2[0])[2]))
    # print(type((data[0])[0]),type((data[0])[1]),type((data[0])[2]))

    #data = dict (zip (Not_enough_stock_sku_id, Not_enough_stock_warehouse_id))
    poor_stocks_sku_qty=len (data)
    wms_oracle.close()
    return data,poor_stocks_sku_qty


def stock_add_frontend(qty,frontend_data) :
    '''缺货产品前台加库存'''
    gss_mysql = pymysql.connect (
        host="10.6.168.13",
        user="store",
        passwd="d41d8cd98f00b204",
        database="store",
    )
    print ('GSS-MySQL数据库:连接成功')
    mycursor = gss_mysql.cursor()
    for i in range(0,len(frontend_data)):
        item_no=(frontend_data[i])[0]
        warehouse_id=(frontend_data[i])[1]
        print('更新商品编码为：'+item_no,'仓库ID为：'+warehouse_id+'的库存')
        update = "UPDATE store_product_stock SET available_qty=%s WHERE product_no=%s AND `storage`=%s;" % (
            qty, item_no, warehouse_id)
        mycursor.execute (update)
        gss_mysql.commit ()
    gss_mysql.close ()
    print('前台库存更新完成')

def stock_add_backend(qty,backend_data):
    '''WMS加库存'''
    wms_oracle=oracle.connect('WMS_SH_YW', 'WMS_SH_YW', '10.6.84.20:1521/WMSOracle')
    #用自己的实际数据库用户名、密码、主机ip地址 替换即可
    print ('WMS-Oracle数据库:连接成功')
    cursor = wms_oracle.cursor ()                           # 使用cursor()方法获取操作游标
    for i in range(0,len(backend_data)):
        sku_id=(backend_data[i])[0]
        warehouse_id=(backend_data[i])[1]
        '''查询当前表sequence'''
        select_max_id='select SEQ_STK_BATCH_LOC_LPN_ID.Nextval from dual'
        cursor.execute (select_max_id)
        result1=cursor.fetchall()
        max_id=(result1[0])[0]
        print('插入SKU_id为：'+sku_id,'仓库ID为：'+warehouse_id+'的库存')
        '''插入库存数据'''
        if warehouse_id == 13:
            LPN_NO='PGZ206170001'
            LOT_ID='3399492'
            LOC_ID='646851'
        elif warehouse_id == 10:
            LPN_NO='PTJ107030001'
            LOT_ID='3401132'
            LOC_ID='795440'
        elif warehouse_id == 15:
            LPN_NO='PSH305130010'
            LOT_ID='3399348'
            LOC_ID='639454'
        elif warehouse_id == 20:
            LPN_NO='PMAS02080003'
            LOT_ID='3406776'
            LOC_ID='799687'
        elif warehouse_id == 30:
            LPN_NO='PSCYY12250011'
            LOT_ID='3410514'
            LOC_ID='799757'
        else :
            LPN_NO='*'
            LOT_ID='3410514'
            LOC_ID='799757'
        insert="INSERT INTO stk_batch_loc_lpn " \
               "(ID, LPN_NO, LOT_ID, LOC_ID, SKU_ID, QTY_AVAILABLE" \
               ", QTY_HOLD, CREATE_BY,CREATE_TIME, UPDATE_BY, UPDATE_TIME, IS_DELETED, VERSION, WAREHOUSE_ID) " \
               "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '0', 'chenpeng', " \
               "TO_TIMESTAMP(' 2019-03-15 17:39:19:400000', 'SYYYY-MM-DD HH24:MI:SS:FF6'), 'chenpeng'," \
               "TO_TIMESTAMP(' 2019-03-15 17:39:19:400000', 'SYYYY-MM-DD HH24:MI:SS:FF6'), '0', '0', '%s')"\
               %(max_id,LPN_NO,LOT_ID,LOC_ID,sku_id,qty,warehouse_id)
        print(insert)
        cursor.execute (insert)
        wms_oracle.commit()
    #
    # '''查询当前可用库存'''
    # select_store_now=\
    #     'SELECT sum(qty_available) from STK_BATCH_LOC_LPN where sku_id=%s and warehouse_id=%s'%(sku_id,warehouse_id)
    # cursor.execute (select_store_now)
    # result3 = cursor.fetchall ()
    # stock=(result3[0])[0]
    # print ('当前'+sku_no+'的WMS库存为：',stock)
    wms_oracle.close ()
    print('WMS库存添加完成')

def Add_Stocks_Auto(qty,min_stocks_qty):
    print('一、查询药城药网热销产品list')
    item_list=query_hotsell_product()
    print('二、查询前台商品库存，并判断是否增加库存')
    result_frontend=Not_enough_stock_frontend(item_list,warehouse_list,min_stocks_qty)
    frontend_data=result_frontend[0]
    poor_stocks_item_qty=result_frontend[1]
    if  poor_stocks_item_qty== 0 :
        print ('前端当前所有品库存充足')
    else :
        print ('前端库存不足的品对应的仓', frontend_data)
        print ('更新前台库存')
        stock_add_frontend (qty, frontend_data)
    print('三、查询WMS商品库存，并判断是否增加库存')
    result_backend=Not_enough_stock_backend(item_list,warehouse_list,min_stocks_qty)
    backend_data=result_backend[0]
    poor_stocks_sku_qty=result_backend[1]
    if poor_stocks_sku_qty==0:
        print('WMS当前所有品库存充足')
    else:
        print('WMS库存不足的品对应的仓、库存',backend_data)
        print('插入WMS库存')
        stock_add_backend(qty,backend_data)

'''
if __name__ == '__main__':
    pass
 
if __name__ == '__main__':
    Add_Stocks_Auto(1000,100) #当可用库存小于100时，自动添加1000个库存
'''
if __name__ == '__main__':
    Add_Stocks_Auto(1000,100) #当可用库存小于100时，自动添加1000个库存

#gss
# select = "SELECT *  from store_product_stock WHERE product_no='0009718289' "
# data=query_mysql('10.6.168.13','store','d41d8cd98f00b204',3306,'store',select)
#print(data)



#Not_enough_stock_backend(warehouse_id)
#Not_enough_stock_frontend(warehouse_list)
#query_ItemNo_BY_SkuNo()
#query_hotsell_product()
#Not_enough_stock_frontend()
#重庆药业 20 广州药业 13  昆山药网 15  昆山乙方 30 天津药网 10
