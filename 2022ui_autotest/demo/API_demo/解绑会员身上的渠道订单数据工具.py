# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-20 10:57
# ---
"""
工具说明：解绑会员身上的渠道订单
"""
from baofoo_tools import ConvenientScript

if __name__ == '__main__':
    unbind_order = ConvenientScript.del_bind_member_data(external_user_id='AAHZ9TdrAOHupynQxEEPzRzA',
                                                         member_no="540133129594068993", is_del_redis=True)
