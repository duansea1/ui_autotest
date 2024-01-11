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




class Shop(object):

    def __init__(self):
        pass
