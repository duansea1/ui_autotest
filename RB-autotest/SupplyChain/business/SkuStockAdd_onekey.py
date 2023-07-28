'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-05-07
#文件项目:   自动化测试
#文件名称:   一键加库存
 '''

#import mysql.connector
import pymysql
import cx_Oracle as oracle
class stock_add:
    '''产品加库存'''

    def stock_add_frontend(self,qty,sku_no,warehouse_id):

        item_no = stock_add ().query_ItemNo_BY_SkuNo (sku_no)
        '''前台加库存'''
        gss_mysql = pymysql.connect(
                host="10.6.168.13",
                user="store",
                passwd="d41d8cd98f00b204",
                database="store",
        )
        print ('GSS-MySQL数据库:连接成功')
        mycursor = gss_mysql.cursor()
        select="select available_qty,freeze_qty from store_product_stock where product_no=%s and `storage` = %s"%(item_no,warehouse_id)


        mycursor.execute(select)
        result = mycursor.fetchall()
        available_qty=(result[0])[0]
        freeze_qty=(result[0])[1]
        sellable_qty=available_qty-freeze_qty
        print('GSS更新前'+item_no,'的当前库存为：',available_qty,'\n',
              'GSS更新前'+item_no,'的冻结数量为：',freeze_qty,'\n',
              'GSS更新前'+item_no,'的可售数量为：',sellable_qty,sep='')
        if sellable_qty >= 0:
            QTY=qty+available_qty
            update = "UPDATE store_product_stock SET available_qty=%s WHERE product_no=%s AND `storage`=%s;" % (
                QTY, item_no, warehouse_id)
        else:
            QTY=qty+abs(sellable_qty)+available_qty
            update = "UPDATE store_product_stock SET available_qty=%s WHERE product_no=%s AND `storage`=%s;" % (
                QTY, item_no, warehouse_id)
        mycursor.execute(update)
        gss_mysql.commit()
        print('--------------',item_no,'-GSS库存已更新为：',QTY,'--------------')
        mycursor.execute(select)
        result1 = mycursor.fetchall()
        available_qty=(result1[0])[0]
        freeze_qty=(result1[0])[1]
        sellable_qty=available_qty-freeze_qty
        print ('GSS更新后' + item_no, '的当前库存为：', available_qty, '\n',
               'GSS更新后' + item_no, '的冻结数量为：', freeze_qty, '\n',
               'GSS更新后' + item_no, '的可售数量为：', sellable_qty,sep='')
        gss_mysql.close()

    def stock_add_backend(self,qty,sku_no,warehouse_id):
        '''WMS加库存'''
        wms_oracle=oracle.connect('WMS_SH_YW', 'WMS_SH_YW', '10.6.84.20:1521/WMSOracle')
        #用自己的实际数据库用户名、密码、主机ip地址 替换即可
        print ('WMS-Oracle数据库:连接成功')
        #print(warehouse_id,type(warehouse_id))
        cursor = wms_oracle.cursor ()                           # 使用cursor()方法获取操作游标
        '''查询当前表sequence'''
        select_max_id='select SEQ_STK_BATCH_LOC_LPN_ID.Nextval from dual'
        cursor.execute (select_max_id)
        result1=cursor.fetchall()
        max_id=(result1[0])[0]

        '''查询SKU_ID'''
        select_sku_id='SELECT id from MD_SKU where product_code=%s'%(sku_no)
        cursor.execute(select_sku_id)
        result2=cursor.fetchall()
        sku_id=(result2[0])[0]
        #print(sku_no,'的SKU_ID为：',sku_id)
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
        else:
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
        #print(insert)
        cursor.execute (insert)
        wms_oracle.commit()
        print('--------------',sku_no,'-WMS库存已增加：',qty,'--------------')

        '''查询当前可用库存'''
        select_store_now=\
            'SELECT sum(qty_available) from STK_BATCH_LOC_LPN where sku_id=%s and warehouse_id=%s'%(sku_id,warehouse_id)
        cursor.execute (select_store_now)
        result3 = cursor.fetchall ()
        stock=(result3[0])[0]
        print ('当前'+sku_no+'的WMS库存为：',stock)
        wms_oracle.close ()

    def query_ItemNo_BY_SkuNo(self,sku_no):
        '''根据产品编码查询商品编码'''
        pms_mysql=pymysql.connect(
            host="mysql.test.yiyaowang.com",
            user="yao",
            passwd="d41d8cd98f00b204",
            database="yao",
        )
        print ('PMS-MySQL数据库:连接成功')
        mycursor = pms_mysql.cursor()
        #select_sku_no="SELECT product_code from pms_merchant_product where item_no= %s"%(item_no)
        select_item_no="SELECT item_no from pms_merchant_product where product_code= %s"%(sku_no)
        mycursor.execute(select_item_no)
        result4 = mycursor.fetchall()
        item_no=(result4[0])[0]
        print('商品编码为:'+item_no,'产品编码为：'+sku_no)
        pms_mysql.close()
        return item_no

    def query_SkuNo_BY_ItemNo(self,item_no):
        '''根据商品编码查询产品编码'''
        pms_mysql=pymysql.connect(
            host="mysql.test.yiyaowang.com",
            user="yao",
            passwd="d41d8cd98f00b204",
            database="yao",
        )
        print ('PMS-MySQL数据库:连接成功')
        mycursor = pms_mysql.cursor()
        select_sku_no="SELECT product_code from pms_merchant_product where item_no= %s"%(item_no)
        #print(select_sku_no)
        #select_item_no="SELECT item_no from pms_merchant_product where product_code= %s"%(sku_no)
        mycursor.execute(select_sku_no)
        result4 = mycursor.fetchall()
        sku_no=(result4[0])[0]
        print('商品编码为:'+item_no,'产品编码为：'+sku_no)
        pms_mysql.close()
        return sku_no

    def add_stocks_by_skuno(self,qty,sku_no,warehouse_id):
        stock_add().stock_add_frontend(qty,sku_no,warehouse_id)
        stock_add().stock_add_backend(qty,sku_no,warehouse_id)

    def add_stocks_by_itemno(self,qty,item_no,warehouse_id):
        sku_no=self.query_SkuNo_BY_ItemNo(item_no)
        stock_add().stock_add_frontend(qty,sku_no,warehouse_id)
        stock_add().stock_add_backend(qty,sku_no,warehouse_id)


'''前台GSS加库存,后台WMS同步加库存'''
#已知产品编码添加
if __name__ == '__main__':
    #stock_add().add_stocks_by_skuno(10000,'1600870861',20)  #产品编码(数量，产品编码，仓库ID)
    #已知商品编码添加
    stock_add().add_stocks_by_itemno(10000,'1601948055',10)  #商品编码(数量，商品编码，仓库ID)


# 重庆药业 20
# 广州药业 13
# 昆山药网 15
# 昆山乙方 30
# 天津药网 10

#ps:商品编码和产品编码可能一样,也可能不一样，所以需要先查询对应的商品编码












