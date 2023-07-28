'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-06-28
#文件项目:   测试数据管理
#文件名称:   测试数据自动恢复
 '''

from conftest import  read_json
from public.mysql_opr import query_mysql
import os
import openpyxl
import time
import datetime

yc_user_dbinfo = {"host" : "mysql2.test.yiyaowang.com","user" : "yc_user","password" : "d41d8cd98f00b204","port" : 3306,"data" : "yc_user"}
yc_mall_dbinfo = {"host" : "10.6.168.14","user" : "b2btest","password" : "b5zUoR4JbcK3emhhUxdL","port" : 3306,"data" : "yihaoyaocheng"}
qateam_dbinfo = {"host" : "yyw-0345","user" : "qauser","password" : "qa_123456","port" : 3306,"data" : "qateam"}
now = datetime.datetime.now ()
current_time = now.strftime ('%Y-%m-%d %H:%M:%S ')
delta = datetime.timedelta (days=366)
#n_days = now + delta  # 获取当前时间的下一年
n_days = (now + delta).strftime('%Y-%m-%d %H:%M:%S ')  # 获取当前时间的下一年
def DB_operate(DB,SQL):
    '''用作mysel 查询更新删除操作'''
    if DB== 'yc_user':
        result = query_mysql (yc_user_dbinfo['host'], yc_user_dbinfo['user'], yc_user_dbinfo['password'],
                               yc_user_dbinfo['port'], yc_user_dbinfo['data'], sql=SQL)
    elif DB== 'yc_mall':
        result = query_mysql (yc_mall_dbinfo['host'], yc_mall_dbinfo['user'], yc_mall_dbinfo['password'],
                               yc_mall_dbinfo['port'], yc_mall_dbinfo['data'], sql=SQL)
    elif DB== 'qateam':
        result = query_mysql (qateam_dbinfo['host'], qateam_dbinfo['user'], qateam_dbinfo['password'],
                               qateam_dbinfo['port'], qateam_dbinfo['data'], sql=SQL)
    else:
        result=print('请输入正确的数据库名称')

    return result

class Test_Data_Recovery:
    class account:
        '''账号类'''
        def account_recovery_auto(self):
            '''查看数据库保存的密码是否与JOSN文件密码一致，如不一致，则自动更新'''
            username_list=[]
            pwd_list=[]
            login_pwd_list=[]
            use_info=read_json('account_in_db','b2b')
            #use_info=read_json('user_pwdrecovery_test','b2b')
            # pwd=read_json('user_pwdrecovery_test','b2b')
            for a in use_info :
                username_list.append(a['name'] )
            for b in use_info:
                pwd_list.append(b['password'])
            for c in use_info:
                login_pwd_list.append(c['login_pwd'])

            #print('username_list',username_list)
            #print('pwd_list',pwd_list)
            #print(type(username_list))
            username=tuple(username_list)
            print('hh',username)
            #print('username',username)
            #print(type(username))
            args=','.join(username)
            SELECT_SQL = "SELECT id,username,password from t_passport_user where username in %s order by instr(',%s,',CONCAT(',',username,','))" % (username,args,)#查询结果按查询条件顺序排序
            #print(SELECT_SQL)
            result1 = query_mysql (yc_user_dbinfo['host'], yc_user_dbinfo['user'], yc_user_dbinfo['password'], yc_user_dbinfo['port'], yc_user_dbinfo['data'],sql=SELECT_SQL)
            for i in range(0,len(result1['data'])):
                username_db=(result1['data'][i])[1]
                pwd_db=(result1['data'][i])[2]
                username_json=username[i]
                pwd_json=pwd_list[i]
                pwd_login_json=login_pwd_list[i]
                #print('JOSN_DATA:',username_json,pwd_json)
                #print('DB_DATA:',username_db,pwd_db)
                if username_db ==username_json:
                    if pwd_db != pwd_json:
                        print('密码异常的账号：'+username_db)
                        UPDATA_SQL = "update t_passport_user set `password`='%s' WHERE username='%s'" %(pwd_json,username_db)
                        #print(UPDATA_SQL)
                        UPDATE = query_mysql (yc_user_dbinfo['host'], yc_user_dbinfo['user'], yc_user_dbinfo['password'],
                                               yc_user_dbinfo['port'], yc_user_dbinfo['data'], sql=UPDATA_SQL)
                        print(username_db+'的密码已更新为：'+pwd_login_json)
                    else:
                        print(username_db+'---账号密码正常')
                else:
                    print('当前账号异常，请检查JOSN文件')

    class activity:
        '''活动'''
        def query_test_data_activity(self):
            '''查询测试库活动数据'''
            Query_SQL="SELECT * from auto_activity_records where platform=1"  #暂时只维护药城
            result1 = DB_operate('qateam',Query_SQL)
            return result1
        # def Query_Yc_Activity_atatus(self,activity_id,activity_type):
        #     '''根据不同活动类型查询YC当前活动状态'''
        #     if activity_type in (1,2,3):
        #         sql="SELECT a.id,a.end_time,a.promotion_state,a.audit_status,b.group_code,c.`status` from t_promotion a " \
        #                       "INNER JOIN t_promotion_group b on a.id=b.promotion_id " \
        #                       "INNER JOIN t_promotion_product c on a.id=c.promotion_id " \
        #                       "where a.id = %s " % (activity_id)  # 查询活动状态
        #         YC_activity_status = query_mysql (yc_mall_dbinfo['host'], yc_mall_dbinfo['user'],
        #                                           yc_mall_dbinfo['password'],
        #                                           yc_mall_dbinfo['port'], yc_mall_dbinfo['data'], sql=sql)
        #     elif activity_type == 4:
        #         sql="SELECT a.id,a.`status`,a.end_time,b.is_delete from t_rebate a " \
        #                   "INNER JOIN t_rebate_product b on a.id=b.rebate_id " \
        #                   "WHERE a.id = %s"%(activity_id)
        #         YC_activity_status = query_mysql (yc_mall_dbinfo['host'], yc_mall_dbinfo['user'],
        #                                           yc_mall_dbinfo['password'],
        #                                           yc_mall_dbinfo['port'], yc_mall_dbinfo['data'], sql=sql)

        def promotion_recovery(self,activity_id,activity_product,activity_pertect_type):
            '''特价类型活动恢复'''#包含特价、满减满赠、套餐、会员
            print('⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐')
            print ('当前监控特价类型活动ID为：',activity_id)
            if activity_pertect_type == 'b' :  # 维护类型为生效中
                YC_status_query = "SELECT a.id,a.end_time,a.promotion_state,a.audit_status,b.group_code,c.`status` from t_promotion a " \
                                  "INNER JOIN t_promotion_group b on a.id=b.promotion_id " \
                                  "INNER JOIN t_promotion_product c on a.id=c.promotion_id " \
                                  "where a.id = %s " % (activity_id)  # 查询活动状态
                #print (YC_status_query)
                YC_activity_status = DB_operate('yc_mall',YC_status_query)
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
                    update1 = DB_operate('yc_mall',update_sql1) # 更新活动状态为生效
                    update2 = DB_operate('yc_mall',update_sql2) # 更新活动商品为生效
                    print ('---------',activity_id,'已恢复------------')

            else:
                print ('初版暂时只维护生效中活动')

        def together_buy_recovery(self,activity_id,activity_product,activity_pertect_type):
            '''一起购活动恢复'''
            #print(activity_id,activity_pertect_type)
            print ('⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐')
            print ('当前监控一起购活动ID为：', activity_id)
            if activity_pertect_type == 'b' :  # 维护类型为生效中
                yc_status_sql = "SELECT a.id,a.session_name,a.end_time,a.session_status,a.audit_status,b.end_time,b.project_status from t_buy_together_session a " \
                                "INNER JOIN t_buy_together b on a.id=b.session_id " \
                                "WHERE b.id=%s" % (activity_id)
                #print (yc_status_sql)
                buytogether_status = DB_operate ('yc_mall', yc_status_sql)
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
                    update1 = DB_operate ('yc_mall', update_sql1)  # 更新活动状态为生效
                    update2 = DB_operate ('yc_mall', update_sql2)  # 更新活动商品为生效
                    print ('---------',activity_id,'已恢复------------')
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
                rebate_status=DB_operate('yc_mall',rebate_status_sql)
                #print((rebate_status['data'][0])[2],current_time)
                if str ((rebate_status['data'][0])[2]) > current_time and (rebate_status['data'][0])[1] == 0 and (rebate_status['data'][0])[3] == 0:

                    print (activity_id, '活动正常')
                else :
                    print (activity_id, '活动失效！！！！！！！！！！！！！！！！！！！！！！！！')
                    update_sql1 = "UPDATE t_rebate set status= 0 ,end_time = '%s' where id = %s"%(n_days,activity_id)
                    update_sql2 = "update t_rebate_product SET is_delete=0 WHERE id=%s" % (activity_id)
                    print(update_sql1,update_sql2)
                    update1 = DB_operate('yc_mall',update_sql1) # 更新活动状态为生效
                    update2 = DB_operate('yc_mall',update_sql2) # 更新活动商品为生效
                    print ('---------',activity_id,'已恢复------------')

            else:
                print ('初版暂时只维护生效中活动')


        def activity_recovery_auto(self):
            '''根据不同活动类型，自动恢复活动状态'''
            activity=self.query_test_data_activity()
            print('当前共有活动：',activity['rows'])
            # promotion_activity_list=[]
            # rebate_activity_list=[]
            # butogether_activity_list=[]
            for i in range(0,activity['rows']):
                activity_type=(activity['data'][i])[2] #活动类型
                activity_id=(activity['data'][i])[1]  #活动ID
                activity_pertect_type=(activity['data'][i])[6]  #活动维护类型
                activity_product=(activity['data'][i])[7] #活动商品
                #print(activity_id,activity_type)
                #print(type(activity_id))
                if activity_type in (1,2,3):
                    #promotion_activity_list.append()
                    self.promotion_recovery(activity_id,activity_product,activity_pertect_type)
                elif activity_type== 4:
                    # rebate_activity_tuple=(activity_id,activity_pertect_type)
                    # rebate_activity_list.append(rebate_activity_tuple)
                    self.rebate_recovery(activity_id,activity_product,activity_pertect_type)
                elif activity_type == 5:
                    self.together_buy_recovery(activity_id,activity_product,activity_pertect_type)
                else:
                    print('还未添加活动类型为',activity_type,'的方法')

if __name__ == '__main__':
    print('----------测试数据监控并自动恢复-----------')
    R=Test_Data_Recovery()
    user=R.account()
    print('一、账号数据监控并恢复')
    #user.account_recovery_auto()  #账号数据
    print('二、活动数据监控并恢复')
    activity=R.activity()
    activity.activity_recovery_auto() #活动数据
    print('----------所有测试数据已监控并自动恢复-----------')
