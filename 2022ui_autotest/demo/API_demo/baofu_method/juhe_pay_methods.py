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

    def delete_zw_payhub_data(self, open_no):
        """
        宝财通2.0-删除开户资料
        @corp_unified_social_credit_code-统一社会代码
        """

        # 1、zw_merchant_info 删除商户信息
        sql_info = f"delete from zw_merchant_info where open_no ='{open_no}'"
        yield sql_info
        # 2、 删除 zw_merchant_product--删除产品信息
        sql_product = f"delete from zw_merchant_product where open_no ='{open_no}'"
        yield sql_product

        # 3、zw_merchant_apply--删除申请信息
        sql_apply = f"delete from zw_merchant_apply where open_no ='{open_no}'"
        yield sql_apply

        # 4、zw_merchant_apply_record--删除申请记录
        sql_apply_record = f"delete from zw_merchant_apply_record where open_no ='{open_no}'"
        yield sql_apply_record

        # 5、zw_merchant_info_snapshot--删除快照信息
        sql_snapshot = f"delete from zw_merchant_info_snapshot where open_no ='{open_no}'"
        yield sql_snapshot

    def query_bct_openNo_sql(self, corp_unified_social_credit_code):
        """
        查询BCT2.0商户的统一社会信用代码对应的open_no
        :param corp_unified_social_credit_code: 统一社会信用代码
        :return:
        """
        sql_info = f"select open_no,corp_name from zw_merchant_info where corp_unified_social_credit_code ='{corp_unified_social_credit_code}'"
        return sql_info


