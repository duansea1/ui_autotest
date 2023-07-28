'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-06-28
#文件项目:   测试数据管理
#文件名称:   测试数据自动恢复
 '''
from public.files import  read_json
from public.mysql_opr import query_mysql
import os
import time
import datetime
import json

yc_user= {"host" : "mysql2.test.yiyaowang.com","user" : "yc_user","password" : "d41d8cd98f00b204","port" : 3306,"data" : "yc_user"}
yc_mall = {"host" : "10.6.168.14","user" : "b2btest","password" : "b5zUoR4JbcK3emhhUxdL","port" : 3306,"data" : "yihaoyaocheng"}
qateam = {"host" : "yyw-0345","user" : "qauser","password" : "qa_123456","port" : 3306,"data" : "qateam"}
gss = {"host" : "10.6.168.13","user" : "store","password" : "d41d8cd98f00b204","port" : 3306,"data" : "store"}
now = datetime.datetime.now ()
current_time = now.strftime ('%Y-%m-%d %H:%M:%S ')
delta = datetime.timedelta (days=366)
#n_days = now + delta  # 获取当前时间的下一年
n_days = (now + delta).strftime('%Y-%m-%d %H:%M:%S ')  # 获取当前时间的下一年


def DB_operate(DB,SQL):
    '''用作mysel 查询更新删除操作'''
    #DB = json.loads (DB)
    result=query_mysql (DB['host'], DB['user'], DB['password'],DB['port'], DB['data'], sql=SQL)
    return result 

class ActivityRecovery:
    '''活动'''
    def query_test_data_activity(self,platform):
        '''查询测试库活动数据
        @param platform: 1-药城，2-药网
        '''
        Query_SQL="SELECT activity_id,activity_type,protect_type,activity_products from auto_activity_records " \
                  "where platform="+str(platform)  #暂时只维护药城
        result1 = DB_operate(qateam,Query_SQL)
        return result1

    def activity_recovery_auto(self,platform):
        '''根据不同活动类型，自动恢复活动状态'''
        activity=self.query_test_data_activity(platform)
        print('当前共有活动：',activity['rows'])
        # promotion_activity_list=[]
        # rebate_activity_list=[]
        # butogether_activity_list=[]
        for i in range(0,activity['rows']):
            activity_type=(activity['data'][i])[1] #活动类型
            activity_id=(activity['data'][i])[0]  #活动ID
            activity_pertect_type=(activity['data'][i])[2]  #活动维护类型
            activity_product=(activity['data'][i])[3] #活动商品
            #print(activity_id,activity_type)
            #print(type(activity_id))
            if activity_type in (1,2,3):
            #if activity_type in (1, 2, 3，7) :  -- 套餐待完善
                #promotion_activity_list.append()
                self.promotion_recovery(activity_id,activity_product,activity_pertect_type)
            elif activity_type== 4:
                # rebate_activity_tuple=(activity_id,activity_pertect_type)
                # rebate_activity_list.append(rebate_activity_tuple)
                self.rebate_recovery(activity_id,activity_product,activity_pertect_type)
            elif activity_type == 5:
                self.together_buy_recovery(activity_id,activity_product,activity_pertect_type)
            elif activity_type == 6:
                self.limitbuy_recovery(activity_id,activity_product,activity_pertect_type)
            elif activity_type == 8:
                self.flashpurchase_recovery(activity_id,activity_product,activity_pertect_type)
            else:
                print('还未添加活动类型为',activity_type,'的方法')

    def promotion_recovery(self,activity_id,activity_product,activity_pertect_type):
        '''促销类型活动恢复'''
        #包含特价、满减满赠、套餐、会员   7--套餐单独写
        print('⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐')
        print ('当前监控促销类型活动ID为：',activity_id)
        if activity_pertect_type == 'b' :  # 维护类型为生效中
            YC_status_query = "SELECT a.id,a.end_time,a.promotion_state,a.audit_status,b.group_code,c.`status` from t_promotion a " \
                              "INNER JOIN t_promotion_group b on a.id=b.promotion_id " \
                              "INNER JOIN t_promotion_product c on a.id=c.promotion_id " \
                              "where a.id = %s " % (activity_id)  # 查询活动状态
            print (YC_status_query)
            YC_activity_status = DB_operate(yc_mall,YC_status_query)
            # promotion_id=(YC_activity_status['data'][i])[0]  #活动ID
            promotion_end_time = (YC_activity_status['data'][0])[1]  # 活动结束时间
            promotion_state = (YC_activity_status['data'][0])[2]  # 活动状态
            promotion_audit_status = (YC_activity_status['data'][0])[3]  # 活动审核状态
            promotion_product_staus = (YC_activity_status['data'][0])[5]  # 活动商品状态-- 后续可考虑判断商品SPU_code
            # promotion_group=(YC_activity_status['data'][i])[5] #活动客户组
            #current_time = time.strftime ('%Y-%m-%d %H:%M:%S ', time.localtime ())
            #print(promotion_end_time,current_time)
            #print(type(promotion_end_time),type(current_time))
            if str (promotion_end_time) > current_time and promotion_state == 0 and promotion_audit_status == 1 and promotion_product_staus == 0 :  # and promotion_group
                print (activity_id, '活动正常')
            else :
                print (activity_id, '活动失效！！！！！！！！！！！！！！！！！！！！！！！！')
                update_sql1 = "UPDATE t_promotion a set " \
                              "a.end_time = '%s'," \
                              "a.promotion_state= 0," \
                              "a.audit_status=1 " \
                              "WHERE a.id=%s" % (n_days, activity_id)
                update_sql2 = "update t_promotion_product c set c.`status`=0 where c.promotion_id=%s" % (activity_id)
                print(update_sql1,update_sql2)
                update1 = DB_operate(yc_mall,update_sql1) # 更新活动状态为生效
                update2 = DB_operate(yc_mall,update_sql2) # 更新活动商品为生效
                print ('---------',activity_id,'已恢复------------')

        else:
            print ('初版暂时只维护生效中活动')

    def together_buy_recovery(self,activity_id,activity_product,activity_pertect_type):
        '''一起购活动恢复'''
        #print(activity_id,activity_pertect_type)
        print ('⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐')
        print ('当前监控一起购活动ID为：', activity_id)
        yc_status_sql = "SELECT a.id,a.session_name,a.end_time,a.session_status,a.audit_status,b.end_time,b.project_status from t_buy_together_session a " \
                        "INNER JOIN t_buy_together b on a.id=b.session_id " \
                        "WHERE b.id=%s" % (activity_id)
        # print (yc_status_sql)
        buytogether_status = DB_operate (yc_mall, yc_status_sql)
        if activity_pertect_type == 'b' :  # 维护类型为生效中
            print('维护类型为生效中')
            #print ((buytogether_status['data'][0])[0], current_time)
            if str ((buytogether_status['data'][0])[2]) > current_time and (buytogether_status['data'][0])[3] == 0 and \
                    (buytogether_status['data'][0])[4] == 1 and str((buytogether_status['data'][0])[5])  > current_time and \
                    (buytogether_status['data'][0])[6] == 0:
                print (activity_id, '活动正常')
            else :
                print (activity_id, '活动失效！！！！！！！！！！！！！！！！！！！！！！！！')
                update_sql1 = "update t_buy_together_session set end_time='%s',session_status=0,audit_status=1 WHERE id = %s" % (n_days,(buytogether_status['data'][0])[0])
                update_sql2 = "UPDATE t_buy_together set end_time='%s',project_status=0 WHERE id=%s" % (n_days, activity_id)
                print (update_sql1, update_sql2)
                update1 = DB_operate (yc_mall, update_sql1)  # 更新活动状态为生效
                update2 = DB_operate (yc_mall, update_sql2)  # 更新活动商品为生效
                print ('---------',activity_id,'已维护为生效中------------')
        elif activity_pertect_type == 'c' :  # 维护类型已结束
            print('维护类型为已结束')
            if str((buytogether_status['data'][0])[2]) < current_time:
                print (activity_id, '活动正常')
            else:
                update_sql="update t_buy_together_session a," \
                       "t_buy_together b set a.end_time='%s',a.session_status=0,a.audit_status=1,b.end_time='%s',b.project_status=0 " \
                       "WHERE a.id = %s and b.id=%s"%(current_time,current_time,(buytogether_status['data'][0])[0],activity_id)
                update = DB_operate (yc_mall, update_sql)  # 更新活动状态为认购结束
                print ('---------',activity_id,'已维护为认购结束------------')
        elif activity_pertect_type == 'd':  # 维护类型为拼团成功
            print('维护类型为拼团成功')
            query_store="SELECT  a.activity_no,a.is_reserve_stock,a.activity_status,b.available_qty,b.freeze_qty from store_activity_stock a " \
                        "inner join store_activity_stock_detail b on a.activity_no=b.activity_no" \
                        " where a.activity_no = '%s'"%(activity_id)
            print(query_store)
            try:
                store_status=DB_operate(gss,query_store)
                if ((store_status['data'][0])[1])!=0 or ((store_status['data'][0])[2])!=1 or ((store_status['data'][0])[3])<=((store_status['data'][0])[4]):
                    print (activity_id, '活动正常')
                else:
                    update_sql="UPDATE store_activity_stock set activity_status = 0 where activity_no =  '%s'"%(activity_id)
                    print(update_sql)
                    update = DB_operate (gss, update_sql)  # 更新活动状态为认购结束
                    print ('---------',activity_id,'已维护为拼团成功------------')
            except:
                print(activity_id,'活动数据异常')
        else :
            print ('初版暂时只维护生效中活动')

    def rebate_recovery(self,activity_id,activity_product,activity_pertect_type):
        '''返利金活动恢复'''
        print('⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐')
        print ('当前监控返利金活动ID为：',activity_id)
        if activity_pertect_type == 'b' :  # 维护类型为生效中
            rebate_status_sql="SELECT a.id,a.`status`,a.end_time,b.is_delete from t_rebate a " \
                          "INNER JOIN t_rebate_product b on a.id=b.rebate_id " \
                          "WHERE a.id = %s"%(activity_id)
            #print (rebate_status_sql)
            rebate_status=DB_operate(yc_mall,rebate_status_sql)
            #print((rebate_status['data'][0])[2],current_time)
            if str ((rebate_status['data'][0])[2]) > current_time and (rebate_status['data'][0])[1] == 0 and (rebate_status['data'][0])[3] == 0:

                print (activity_id, '活动正常')
            else :
                print (activity_id, '活动失效！！！！！！！！！！！！！！！！！！！！！！！！')
                update_sql1 = "UPDATE t_rebate set status= 0 ,end_time = '%s' where id = %s"%(n_days,activity_id)
                update_sql2 = "update t_rebate_product SET is_delete=0 WHERE id=%s" % (activity_id)
                print(update_sql1,update_sql2)
                update1 = DB_operate(yc_mall,update_sql1) # 更新活动状态为生效
                update2 = DB_operate(yc_mall,update_sql2) # 更新活动商品为生效
                print ('---------',activity_id,'已恢复------------')

        else:
            print ('初版暂时只维护生效中活动')

    def flashpurchase_recovery(self,activity_id,activity_product,activity_pertect_type):
        '''闪购活动恢复'''
        print('⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐')
        print ('当前监控闪购活动ID为：',activity_id)
        if activity_pertect_type == 'b' :  # 维护类型为生效中
            self.promotion_recovery(activity_id,activity_product,activity_pertect_type) #闪购活动恢复先恢复其关联的特价活动
            flashpurchase_status_sql="select a.id,a.status,b.promotion_id,b.status from t_purchase a " \
                              "INNER JOIN t_purchase_promotion b on a.id=b.purchase_id " \
                              "where b.promotion_id=%s;"%(activity_id)
            #print (rebate_status_sql)
            flashpurchase_status=DB_operate(yc_mall,flashpurchase_status_sql)
            #print((rebate_status['data'][0])[2],current_time)
            if (flashpurchase_status['data'][0])[1] ==1 and (flashpurchase_status['data'][0])[3] ==1:
                print (activity_id, '活动正常')
            else :
                print (activity_id, '活动失效！！！！！！！！！！！！！！！！！！！！！！！！')
                update_sql = "update t_purchase a,t_purchase_promotion b set a.status=1,b.status=1 " \
                             "where a.id=%s and b.promotion_id=%s;"%((flashpurchase_status['data'][0])[0],activity_id)
                print(update_sql)
                update = DB_operate(yc_mall,update_sql) # 更新活动状态为生效
                print ('---------',activity_id,'已恢复------------')

        else:
            print ('初版暂时只维护生效中活动')

    def limitbuy_recovery(self,activity_id,activity_product,activity_pertect_type):
        '''商品限购活动恢复'''  #增加区域恢复
        print('⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐')
        print ('当前监控限购活动ID为：',activity_id)
        if activity_pertect_type == 'b' :  # 维护类型为生效中
            limitbuy_status_sql="SELECT id,productcode_company,begin_time,end_time,`status` from t_product_limit_buy WHERE id =%s"%(activity_id)
            #print (rebate_status_sql)
            limitbuy_status=DB_operate(yc_mall,limitbuy_status_sql)
            #print((rebate_status['data'][0])[2],current_time)
            if str ((limitbuy_status['data'][0])[2]) < current_time and str ((limitbuy_status['data'][0])[3]) > current_time and (limitbuy_status['data'][0])[4] == 0 :
                print (activity_id, '活动正常')
            else :
                print (activity_id, '活动失效！！！！！！！！！！！！！！！！！！！！！！！！')
                update_sql = "UPDATE t_product_limit_buy set begin_time='%s',end_time='%s',`status`=0 where id=%s"%(current_time,n_days,activity_id)
                print(update_sql)
                update = DB_operate(yc_mall,update_sql) # 更新活动状态为生效
                print ('---------',activity_id,'已恢复------------')
        else:
            print ('初版暂时只维护生效中活动')


if __name__ == '__main__':
    print('二、活动数据监控并恢复')
    activity=ActivityRecovery()
    activity.activity_recovery_auto(1) #活动数据，1-药城，2-药网
    print('----------所有测试数据已监控并自动恢复-----------')