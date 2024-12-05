# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-12-29 16:29
# ---


def delete_shop_user_sqls(open_kid):
    """
    删除商城用户的sql
    :param open_kid: 用户的openid
    :return:
    """
    # zw_user
    sql1 = ("DELETE from zw_user where open_kid='" + str(open_kid)+"'")
    yield sql1
    # zw_wx_user
    sql2 = ("DELETE from zw_wx_user where open_kid='" + str(open_kid)+"'")
    yield sql2
    # zw_member
    wx_openid = open_kid
    sql3 = ("DELETE from zw_member where open_kid='" + str(open_kid)+"'")
    yield sql3
    # zw_member
    sql4 = ("DELETE from zw_member_points where open_kid='" + str(open_kid)+"'")
    yield sql4
    # zw_coupon_customer --优惠券记录
    sql5 = ("DELETE from zw_coupon_customer where  open_kid='" + str(open_kid)+"'")
    yield sql5


def delete_shop_to_scrm_user_sqls(mobile):
    """
    删除ucenter库中 商城会员与scrm会员的关系数据
    :param mobile: 用户的手机号
    :return:
    """
    # zw_kyd_member_v2-会员基础数据表，会员与手机号的绑定关系
    # sql1 = ("DELETE from zw_kyd_member_v2 where mobile='" + str(mobile)+"'")
    # yield sql1

    # zw_kyd_member_shop_v2-零售店铺会员数据
    sql2 = ("DELETE from zw_kyd_member_shop_v2 where channel_id = 1 and mobile='" + str(mobile)+"'")
    yield sql2
    # zw_kyd_member_shop_info_v2-店铺会员信息表
    sql3 = ("DELETE from zw_kyd_member_shop_info_v2 where channel_id = 1 and mobile='" + str(mobile)+"'")
    yield sql3

    # zw_kyd_member_cust-会员客户关联表 todo:客户详情页面展示关联的会员信息，与该表有关，可手动删除或者根据查询结果删除
    # sql4 = ("DELETE from zw_kyd_member_cust where  external_user_id='" + external_user_id + "'")
    # yield sql5

    # # zw_kyd_member_store_index-店铺会员信息表
    # sql3 = ("DELETE from zw_kyd_member_store_index where channel_id = 1 and mobile='" + str(mobile) + "'")
    # yield sql3







class Shop(object):

    def __init__(self):
        pass
