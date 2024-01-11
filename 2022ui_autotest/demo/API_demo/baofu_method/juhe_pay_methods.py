# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-10-24 17:56
# ---

class Aggregatd_Payment():

    def delete_payhub_data(self, corp_unified_social_credit_code):
        """
        @corp_unified_social_credit_code-统一社会代码
        """
        # 1、删除快照表的数据-zw_merchant_info_snapshot
        sql_sapshot = ("delete from zw_merchant_info_snapshot where open_no in ("
                       + "select open_no from zw_merchant_info where corp_unified_social_credit_code='"
                       + corp_unified_social_credit_code + "')")
        yield sql_sapshot

        # 2、删除zw_merchant_isp
        sql_isp = ("delete from zw_merchant_isp where open_no in ("
                   + "select open_no from zw_merchant_info where corp_unified_social_credit_code='"
                   + corp_unified_social_credit_code + "')")
        yield sql_isp
        # 4、 删除 zw_merchant_info_draft
        sql_draft = ("delete from zw_merchant_info_draft where corp_unified_social_credit_code='"
                     + corp_unified_social_credit_code + "'")
        yield sql_draft

        # 5、删除企业开户信息表的数据-zw_merchant_info
        sql_info = ("delete from zw_merchant_info where corp_unified_social_credit_code='"
                    + corp_unified_social_credit_code + "'")
        yield sql_info

    def query_openNO_sql(self, corp_unified_social_credit_code):
        """
        查询商户的openNo
        :param corp_unified_social_credit_code:
        :return:
        """
        sql_info = ("select open_no from zw_merchant_info where corp_unified_social_credit_code='"
                    + corp_unified_social_credit_code + "'")
        return sql_info
