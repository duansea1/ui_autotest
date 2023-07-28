'''
Created on 2019年7月5日

@author: zhangtingting01
'''
import pymysql
import hashlib


def select_from_db(address, username, password, db_name,sql):
    '''获取数据库内容'''
    try:
        db = pymysql.connect(address, username, password, db_name)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except Exception:
        return 0
    finally:
        db.close()


def update_db(address, username, password, db_name,sql,val):
    '''修改,插入,删除数据库内容'''
    try:
        db = pymysql.connect(address, username, password, db_name)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行SQL语句
        cursor.execute(sql,val)
        # 提交到数据库执行
        db.commit()
        return True
    except Exception:
        # 发生错误时回滚
        db.rollback()
        return False
    finally:
        db.close()
        
def yc_account_check_and_reset():   
    '''药城账号数据监测恢复'''
    sql = 'select userid,username,entername,password,receive_province,is_vip,pf_sale_province,enter_status,protect_type,register_province,AES_ENCRYPT(phone,md5("111JT")) as phone from auto_account_records where platform = 1'
    result = select_from_db('yyw-0345', 'qauser', 'qa_123456', 'qateam',sql)  #UI脚本测试数据
    
    type_fun = {"a":account_password_reset,
                "b":enterprise_name_reset,
                "c":account_phone_reset,
                "d":logister_address_reset,
                "e":receive_address_reset,
                "i":user_sell_area_reset,
                "k":zhangqi_money_reset,
                "u":vip_status_reset,
                "n":user_profile_status_reset
                
                }
    for dict in result:
#         print('userid:{}需监控的类型有{}'.format(dict['userid'],dict['protect_type']))
        protect_type = dict['protect_type'].split(',')
        for type in protect_type:
#             print(type)
            if type in ["a","b","c","d","e","i","k","u","n"]:
                fun = type_fun[type]
                try:
                    fun(dict)
                except Exception as e:
                    print('函数：{}调用异常，异常信息：{}'.format(fun,e))
            
    
def yw_account_check_and_reset():   
    '''药网账号数据监测恢复'''
    sql = 'select userid,username,password,receive_province,is_vip,protect_type,AES_ENCRYPT(phone,md5("wwSzpWz2OwA5MYUePExCPBxicArCpdrTOmpcqzMhUrYanWDID0cUpZIAY815qYPWm5nvFjfpahUXSKGQc4RdBo5hFVX9Ht5y8hVxpM933czKewhxsW4cA6qLO2WbHFKB")) as phone from auto_account_records where platform = 2'
    result = select_from_db('yyw-0345', 'qauser', 'qa_123456', 'qateam',sql)  #UI脚本测试数据
    
    type_fun = {"a":yw_account_password_reset,
                "c":yw_account_phone_reset,
                "f":yw_receive_address_reset,
                "g":yw_receive_address_delete,
                "j":yw_account_money_reset,
                "m":cyclebuy_user_reset,
                "u":yw_vip_user_reset 
                }
    for dict in result:
#         print('userid:{}需监控的类型有{}'.format(dict['userid'],dict['protect_type']))
        protect_type = dict['protect_type'].split(',')
        for type in protect_type:
#             print(type)
            if type in ["a","c","f","g","j","m","u"]:
                fun = type_fun[type]
                try:
                    fun(dict)
                except Exception as e:
                    print('函数：{}调用异常，异常信息：{}'.format(fun,e))
            
           

def account_password_reset(dict):
    '''账号密码恢复'''

    sql1 = 'select id,username,password,amobile from t_passport_user'
    result1 = select_from_db('mysql2.test.yiyaowang.com', 'yc_user', 'd41d8cd98f00b204', 'yc_user',sql1)  #药城账号数据库

    for dict1 in result1:
        if dict['userid'] == dict1['id']:
            if dict['password'] == 'null':
                print('测试数据账号：{} 密码为空，请检查！'.format(dict['password']))
            else:
                data = dict['password']
                test_password = hashlib.md5((data).encode('utf-8')).hexdigest()   #测试数据中账号密码加密
                if test_password != dict1['password']:
                    print('测试数据中账号密码与用户数据库中密码不同')
                    print('测试数据中账号信息：账号{}，密码：{}，MD5加密后密码{}'.format(dict['username'],dict['password'],test_password))
                    print('用户数据库中账号信息：账号{}，密码{}'.format(dict1['username'],dict1['password']))
                    update_sql = 'update t_passport_user set password = %s where id = %s'
                    val = (test_password,dict1['id'])
                    update_db('mysql2.test.yiyaowang.com', 'yc_user', 'd41d8cd98f00b204', 'yc_user',update_sql,val)
                        


def account_phone_reset(dict):
    '''手机号恢复'''

    sql1 = 'select id,username,amobile from t_passport_user'
    result1 = select_from_db('mysql2.test.yiyaowang.com', 'yc_user', 'd41d8cd98f00b204', 'yc_user',sql1)

    for dict1 in result1:
        if dict['userid'] == dict1['id']:
            if dict['phone'] != dict1['amobile']:
                print('测试数据中账号:{}手机号与用户数据库中手机号不同'.format(dict['userid']))
                update_sql = 'update t_passport_user set amobile = %s where id = %s'
                val = (dict["phone"],dict1['id'])
                update_db('mysql2.test.yiyaowang.com', 'yc_user', 'd41d8cd98f00b204', 'yc_user',update_sql,val)
               
                
def enterprise_name_reset(dict):
    '''企业名称恢复
    t_usermanage_enterprise正式表，t_usermanage_enterprise_dft草稿表'''
    
    sql = 'select enterprise_id,enterprise_name from t_usermanage_enterprise_dft'
    result1 = select_from_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',sql)

    sql1 = 'select enterprise_id,enterprise_name from t_usermanage_enterprise'
    result2 = select_from_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',sql1)
 
    for dict1 in result1:
        if dict['userid'] == dict1['enterprise_id']:
            if dict['entername'] != dict1['enterprise_name']:
                print('测试数据账号：{}的企业名称被修改'.format(dict['userid']))
                print('修改前的：{}，修改后的：{}'.format(dict['entername'],dict1['enterprise_name']))
                update_sql = 'update t_usermanage_enterprise_dft set enterprise_name = %s where enterprise_id = %s'
                val = (dict["entername"],dict1['enterprise_id'])
                update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',update_sql,val)
                
    for dict2 in result2:
        if dict['userid'] == dict2['enterprise_id']:
            if dict['entername'] != dict2['enterprise_name']:
                print('测试数据账号：{}的企业名称被修改'.format(dict['userid']))
                print('修改前的：{}，修改后的：{}'.format(dict['entername'],dict2['enterprise_name']))
                update_sql = 'update t_usermanage_enterprise set enterprise_name = %s where enterprise_id = %s'
                val = (dict["entername"],dict2['enterprise_id'])
                update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',update_sql,val)               


def logister_address_reset(dict):
    '''注册地址恢复
    t_usermanage_enterprise正式表，t_usermanage_enterprise_dft草稿表'''
    
    sql = 'select enterprise_id,province_name from t_usermanage_enterprise_dft'
    result1 = select_from_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',sql)

    sql1 = 'select enterprise_id,province_name from t_usermanage_enterprise'
    result2 = select_from_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',sql1)

    for dict1 in result1:
        if dict['userid'] == dict1['enterprise_id']:
            if dict['register_province'] != dict1['province_name']:
                print('测试数据userid：{}的注册地址被修改'.format(dict['userid']))
                print('修改前的：{}，修改后的：{}'.format(dict['register_province'],dict1['province_name']))
                update_sql = 'update t_usermanage_enterprise_dft set province_name = %s where enterprise_id = %s'
                val = (dict["register_province"],dict1['enterprise_id'])
                update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',update_sql,val)
                
    for dict2 in result2:
        if dict['userid'] == dict2['enterprise_id']:
            if dict['register_province'] != dict2['province_name']:
                print('测试数据userid：{}的注册地址被修改'.format(dict['userid']))
                print('修改前的：{}，修改后的：{}'.format(dict['register_province'],dict2['province_name']))
                update_sql = 'update t_usermanage_enterprise set province_name = %s where enterprise_id = %s'
                val = (dict["register_province"],dict2['enterprise_id'])
                update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',update_sql,val)


def receive_address_reset(dict):
    '''收货地址恢复
    t_usermanage_receiver_address正式表，t_usermanage_receiver_address_dft草稿表'''

    sql = 'select enterprise_id,province_name from t_usermanage_receiver_address_dft'
    result1 = select_from_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',sql)

    sql1 = 'select enterprise_id,province_name from t_usermanage_receiver_address'
    result2 = select_from_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',sql1)

    for dict1 in result1:
        if dict['userid'] == dict1['enterprise_id']:
            if dict['receive_province'] != dict1['province_name']:
                print('测试数据userid：{}的收货地址被修改'.format(dict['userid']))
                print('修改前的：{}，修改后的：{}'.format(dict['receive_province'],dict1['province_name']))
                update_sql = 'update t_usermanage_receiver_address_dft set province_name = %s where enterprise_id = %s'
                val = (dict["receive_province"],dict1['enterprise_id'])
                update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',update_sql,val)

    for dict2 in result2:
        if dict['userid'] == dict2['enterprise_id']:
            if dict['receive_province'] != dict2['province_name']:
                print('测试数据userid：{}的收货地址被修改'.format(dict['userid']))
                print('修改前的：{}，修改后的：{}'.format(dict['receive_province'],dict2['province_name']))
                update_sql = 'update t_usermanage_receiver_address set province_name = %s where enterprise_id = %s'
                val = (dict["receive_province"],dict2['enterprise_id'])
                update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',update_sql,val)



def user_profile_status_reset(dict):
    '''用户资质状态恢复，包括变更，待电子审核，审核通过，审核不通过等'''
    
    sql1 = 'select enterprise_id,is_check from t_usermanage_enterprise_dft'
    result1 = select_from_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',sql1)

    for dict1 in result1:
        if dict['userid'] == dict1['enterprise_id']:
            if dict['enter_status'] != dict1['is_check']:
                print('0:待电子审核,1:审核通过,2:审核不通过,3:变更,5:变更待电子审核,7:变更审核不通过')
                print('用户:{}资质状态被修改！原先状态{}，当前状态{}'.format(dict['userid'],dict['enter_status'],dict1['is_check']))
                update_sql = 'update t_usermanage_enterprise_dft set is_check = %s where enterprise_id = %s'
                val = (dict["enter_status"],dict1['enterprise_id'])
                update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',str(update_sql),val)


def user_sell_area_reset(dict):
    '''用户销售区域恢复
    t_usermanage_delivery_area正式表，t_usermanage_delivery_area_dft草稿表'''
    
    sql = 'select enterprise_id,province,province_name from t_usermanage_delivery_area_dft'
    result1 = select_from_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',sql)
    
    sql1 = 'select enterprise_id,province,province_name from t_usermanage_delivery_area'
    result2 = select_from_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',sql1)

    list_sell_area1 = []  
    list_sell_area2 = [] 

    for dict1 in result1:
        if dict['userid'] == dict1['enterprise_id']:
            list_sell_area1.append(dict1['province_name'])
#     print('当前销售区域：',list_sell_area1)            
    if dict1['province'] != '000000':
        print('销售区域非全国')
        if dict['pf_sale_province'] not in list_sell_area1:
            print('用户userid为{}的账号，{}不在销售区域内'.format(dict['userid'],dict['pf_sale_province']))
            update_sql = 'INSERT INTO t_usermanage_delivery_area_dft (enterprise_id,province,city, province_name,city_name,district_name) VALUES (%s,%s,%s,%s,%s,%s)'
            if dict['pf_sale_province'] in ['北京','上海','重庆','天津']:
                val = (dict['userid'],dict['province'],'',dict['pf_sale_province'],'全市','')
            else:
                val = (dict['userid'],dict['province'],'',dict['pf_sale_province'],'全省','')
                update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',str(update_sql),val)                   
        else:
            print('{}在销售区域内'.format(dict['pf_sale_province']))
    
    for dict2 in result2:
        if dict['userid'] == dict2['enterprise_id']:
            list_sell_area2.append(dict2['province_name'])
#     print('当前销售区域：',list_sell_area2)            
    if dict2['province'] != '000000':
        print('销售区域非全国')
        if dict['pf_sale_province'] not in list_sell_area2:
            print('用户userid为{}的账号，{}不在销售区域内'.format(dict['userid'],dict['pf_sale_province']))
            update_sql = 'INSERT INTO t_usermanage_delivery_area_dft (enterprise_id,province,city, province_name,city_name,district_name) VALUES (%s,%s,%s,%s,%s,%s)'
            if dict['pf_sale_province'] in ['北京','上海','重庆','天津']:
                val = (dict['userid'],dict['province'],'',dict['pf_sale_province'],'全市','')
            else:
                val = (dict['userid'],dict['province'],'',dict['pf_sale_province'],'全省','')
                update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',str(update_sql),val)                   
        else:
            print('{}在销售区域内'.format(dict['pf_sale_province']))


def zhangqi_money_reset(dict):
    '''账期额度恢复'''
    
    sql1 = 'select buyer_code,credit_limit,avl_limit,freeze_limit,status from t_credit'
    result1 = select_from_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',sql1)
  
    for dict1 in result1:
        if dict['userid'] == dict1['buyer_code']:
            if dict1['status'] == 2:
                if int(dict1['avl_limit']) <100:
                    print('账号：{}当前可用账期额度小于100'.format(dict['userid']))
                    if int(dict1['freeze_limit'])>100:
                        print('有大于100的额度被冻结，解冻额度')
                        update_sql1 = 'update t_credit set avl_limit = %s where buyer_code = %s'
                        val1 = (dict1['freeze_limit']+dict1['avl_limit'],dict1['buyer_code'])
                        update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',str(update_sql1),val1)
                        update_sql2 = 'update t_credit set freeze_limit = 0.00 where buyer_code = %s'
                        val2 = (dict1['buyer_code'])
                        update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',str(update_sql2),val2)
                        
                    else:
                        print('剩余可用额度小于100，额度增加100')
                        print('用户资信额度：{}，可用额度：{}'.format(dict1['credit_limit'],dict1['avl_limit']))
                        update_sql1 = 'update t_credit set credit_limit = %s where buyer_code = %s'
                        val1 = (int(dict1['credit_limit'])+100,dict1['buyer_code'])
                        update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',str(update_sql1),val1)
                        update_sql2 = 'update t_credit set avl_limit =%s where buyer_code = %s'
                        val2 = (int(dict1['avl_limit'])+100,dict1['buyer_code'])
                        update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',str(update_sql2),val2)

            else:
                print('账期不是生效状态，请检查')
                        
                        
def vip_status_reset(dict):
    '''会员状态恢复'''
    
    sql1 = 'select enterprise_id,vip_id,status from t_vip_member'
    result1 = select_from_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',sql1)
    vip_user = []

    for dict1 in result1:
        vip_user.append(dict1['enterprise_id'])
#             print('当前会员的企业id列表：',vip_user)   
    if dict['is_vip'] == 1:
        print('该用户是会员')
        if dict['userid'] not in vip_user:
            print('用户:{}不在会员列表中，恢复用户会员状态'.format(dict['userid']))
            update_sql = 'INSERT INTO t_vip_member (vip_id,enterprise_id,status) VALUES  (%s,%s,%s)'
            val = ('1',dict['userid'],'0')
            update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',str(update_sql),val)
        else:
            print('该用户在会员信息数据库中')
            
    elif dict['is_vip'] == 0:
        print('该用户不是会员')
        if dict['userid'] in vip_user:
            print('用户:{}在会员列表中，取消会员状态'.format(dict['userid']))
            update_sql = 'DELETE FROM t_vip_member WHERE enterprise_id = %s'
            val = (dict['userid'])
            update_db('10.6.168.14', 'b2btest', 'b5zUoR4JbcK3emhhUxdL', 'yihaoyaocheng',str(update_sql),val)
        else:
            print('该用户不在会员信息数据库中')
                    


#药网账号恢复代码      
def yw_account_password_reset(dict):
    '''账号密码恢复'''

    sql1 = 'select EcUserId,Id,Password,Salt from ecuser_customer'
    result1 = select_from_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',sql1)  #药网账号数据库

    for dict1 in result1:
        if dict['userid'] == dict1['EcUserId']:
            if dict['password'] == 'null':
                print('测试数据中账号：{} 的密码为空，请检查!'.format(dict['userid']))
            else:
                data = dict['password']+dict1['Salt']
                test_password = hashlib.md5((data).encode('utf-8')).hexdigest()   #测试数据中账号密码加密
                if test_password != dict1['Password']:
                    print('测试数据中账号密码与用户数据库中密码不同')
                    print('测试数据中账号信息：账号{}，密码：{}，MD5加密后密码{}'.format(dict['username'],dict['password'],test_password))
                    print('用户数据库中账号信息：账号{}，密码{}'.format(dict1['Id'],dict1['Password']))
                    update_sql = 'update ecuser_customer set Password = %s where id = %s'
                    val = (test_password,dict1['EcUserId'])
                    update_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',update_sql,val)

def yw_account_phone_reset(dict):
    '''手机号恢复'''

    sql1 = 'select EcUserId,Id,login_mobile_aes from ecuser_customer'
    result1 = select_from_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',sql1)
   
    for dict1 in result1:
        if dict['userid'] == dict1['EcUserId']:
            if dict['phone'] != dict1['login_mobile_aes']:
                print('测试数据中账号:{}手机号与用户数据库中手机号不同'.format(dict['userid']))
                update_sql = 'update ecuser_customer set login_mobile_aes = %s where EcUserId = %s'
                val = (dict["phone"],dict1['EcUserId'])
                update_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',update_sql,val)
                                                          
 
def yw_vip_user_reset(dict):
    '''vip账号恢复'''
    
    sql1 = 'select ecuser_id,equity_ids,member_status from ecuser_member'
    result1 = select_from_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',sql1)
    vip_user = []
   
    for dict1 in result1:
        vip_user.append(dict1['ecuser_id'])
#             print('当前会员的企业id列表：',vip_user)   
    if dict['is_vip'] == 1:
        print('该用户是会员')
        if dict['userid'] not in vip_user:
            print('用户:{}不在会员列表中，恢复用户会员状态'.format(dict['userid']))
            sql = 'select Id,login_mobile_aes,Name from ecuser_customer where EcUserId='+str(dict['userid'])
            info = select_from_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',sql)
            update_sql1 = 'INSERT INTO ecuser_member (ecuser_id,equity_ids,true_name,user_name,user_phone_aes,member_status) VALUES (%s,%s,%s,%s,%s,%s)'
            val1 = (dict['userid'],'1,2,3,4',info[0]['Name'],info[0]['Id'],info[0]['login_mobile_aes'],'1')
            update_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',update_sql1,val1)
            #会员购买表添加记录
            update_sql2 = 'INSERT INTO ecuser_member_order (ecuser_id,order_id,combo_id,start_date,end_date) VALUES (%s,%s,%s,Now(),Now())'
            val2 = (dict['userid'],'123456','12345')
            update_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',update_sql2,val2)
            #会员免邮表添加记录
            update_sql3 = 'INSERT INTO ecuser_member_post (ecuser_id,status,update_date,create_date) VALUES (%s,%s,Now(),Now())'
            val3 = (dict['userid'],'1')
            update_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',update_sql3,val3)
        else:
            print('该用户在会员信息数据库中')
            
    elif dict['is_vip'] == 0:
        print('该用户不是会员')
        if dict['userid'] in vip_user:
            print('用户{} 在会员列表中，取消会员状态'.format(dict['userid']))
            update_sql = 'DELETE FROM ecuser_member WHERE ecuser_id = %s'
            val = (dict['userid'])
            update_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',update_sql,val)
        else:
            print('该用户不在会员信息数据库中')
    
 
 
def yw_account_money_reset(dict):
    '''账户余额恢复'''
    
    sql1 = 'select ecuserId,account,freezeAccount from ecuser_account'
    result1 = select_from_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',sql1)
  
    for dict1 in result1:
        if dict['userid'] == dict1['ecuserId']:
            if int(dict1['account']) <100:
                print('用户：{}当前账户余额小于100'.format(dict['userid']))
                if int(dict1['freezeAccount'])>100:
                    print('有大于100的额度被冻结，解冻额度')
                    print('账户余额：{}，冻结额度：{}'.format(dict1['account'],dict1['freezeAccount']))
                    update_sql1 = 'update ecuser_account set account = %s where ecuserId = %s'
                    val1 = (dict1['freezeAccount']+dict1['account'],dict1['ecuserId'])
                    update_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',str(update_sql1),val1)
                    update_sql2 = 'update ecuser_account set freezeAccount = 0 where ecuserId = %s'
                    val2 = (dict1['ecuserId'])
                    update_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',str(update_sql2),val2)
                    
                else:
                    print('剩余可用额度小于100，额度增加100')
                    print('账户余额：{}'.format(dict1['account']))
                    update_sql1 = 'update ecuser_account set account = %s where ecuserId = %s'
                    val1 = (int(dict1['account'])+100,dict1['ecuserId'])
                    update_db('10.6.168.13', 'user8', 'd41d8cd98f00b204', 'kubauser',str(update_sql1),val1)
                            
                
def yw_receive_address_reset(dict):  
    '''收货地址恢复'''
    
    sql1 = 'select Id,UserId,ProvinceName from ecextend_acceptaddress'
    result1 = select_from_db('10.6.168.13', 'order5', 'd41d8cd98f00b204', 'kubaorder',sql1)
    adress_id = []
    
    for dict1 in result1:
        if dict['userid'] == dict1['UserId']:
            adress_id.append(dict1['Id'])
    if len(adress_id)<1:
        print('测试数据userid：{}新增一条收货地址'.format(dict['userid']))
        update_sql = 'insert into ecextend_acceptaddress (UserId,RealName,Address,Mobile,ProvinceName,CityName,CountyName,Email) values(%s,%s,%s,%s,%s,%s,%s,%s)'
        val = (dict["userid"],'测试','测试地址','1876767534','上海','上海市','黄浦区','123.com')
        update_db('10.6.168.13', 'order5', 'd41d8cd98f00b204', 'kubaorder',update_sql,val)

def yw_receive_address_delete(dict):  
    '''收货地址删除'''
    
    sql1 = 'select Id,UserId,ProvinceName from ecextend_acceptaddress'
    result1 = select_from_db('10.6.168.13', 'order5', 'd41d8cd98f00b204', 'kubaorder',sql1)
    adress_id = []
    
    for dict1 in result1:
        if dict['userid'] == dict1['UserId']:
            adress_id.append(dict1['Id'])
    if len(adress_id)>20:
        print('测试数据userid的收货地址大于20：{}删除至一条收货地址'.format(dict['userid']))
        update_sql = 'DELETE FROM ecextend_acceptaddress WHERE Id = %s'
        for index in range(1,len(adress_id)):
            val = (adress_id[index])
            update_db('10.6.168.13', 'order5', 'd41d8cd98f00b204', 'kubaorder',update_sql,val)

 
def cyclebuy_user_reset(dict):
    '''疗程购账号恢复'''
    
    sql1 = 'select user_id from crm_cyclebuy_user'
    result1 = select_from_db('10.25.32.10', 'bitest1', 'bitest1', 'crm',sql1)
    cyclebuy_user = []
        
    for dict1 in result1: 
        cyclebuy_user.append(dict1['user_id'])     #疗程购账号列表
#             print('疗程购账号：',cyclebuy_user)
    if str(dict['userid']) not in cyclebuy_user:
        print('账号{} 不在疗程购数据表中，恢复疗程购账号'.format(dict['userid']))
        update_sql2 = 'INSERT INTO crm_cyclebuy_user (user_id,pm_id) VALUES (%s,%s)'
        val2 = (str(dict['userid']),'123456')
        update_db('10.25.32.10', 'bitest1', 'bitest1', 'crm',update_sql2,val2)
        
        
                     
if __name__ == '__main__':
    
    yc_account_check_and_reset()
    yw_account_check_and_reset()
