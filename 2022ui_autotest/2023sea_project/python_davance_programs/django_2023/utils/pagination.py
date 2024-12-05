# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-03-06 19:49
# ---

from rest_framework.pagination import PageNumberPagination as _PageNumberPagination
class PageNumberPagination(_PageNumberPagination):
    """
    A simple page number based style that supports page numbers as
    query parameters. For example:

    http://api.example.org/accounts/?page=4
    http://api.example.org/accounts/?page=4&page_size=100
    """
    # The default page size.
    # Defaults to `None`, meaning pagination is disabled.
    page_size = 3
    # 指定前端的参数-页面参数
    page_query_param = 'page'
    page_query_description = '获取的页码'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    # 前端用于指定每一页显示的数据
    page_size_query_param = 'ss'
    page_size_query_description = '每一页数据条数'

    max_page_size = 2

    invalid_page_message = '无效页码'

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_num'] = self.page.number
        response.data['max_num'] = self.page.count(data)
        return response
