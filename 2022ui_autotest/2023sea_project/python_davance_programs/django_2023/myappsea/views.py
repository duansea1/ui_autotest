# -*- coding:utf-8 -*-

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
import json

import csv

# Create your views here.
"""
视图层，在页面展示的，可以在此进行定义方法，返回对应的html格式or其他格式的数据，如csv文件下载
"""

# def index(request):
#
#     return HttpResponse("11k看sea", content_type='text/plain; charset=utf-8')
#
# def get_project(request):
#     return HttpResponse("<h1>这个是一个项目信息</h1>")
#
# def get_project1(request):
#     return HttpResponse("<h1>这个是一个项目信息1</h1>")
#
# def get_project2(request):
#     return HttpResponse("<h1>这个是一个项目信息2222</h1>")
#
#
# def create_project(request):
#     return HttpResponse("<h1>这个是一个项目信息create</h1>")
#
# def put_project(request):
#     return HttpResponse("<h1>这个是一个项目信息put</h1>")
#
# def delete_project(request):
#     return HttpResponse("<h1>这个是一个项目信delete</h1>")
#
# def get_projects(request, pk):
#     return HttpResponse(f"<h1>这个是一个项目信{pk}</h1>")


def projects(request):
    """
    视图函数
    a、视图函数的第一个参数是httpResponse
    b、HttpResponse 对象包含了请求的所有数据（请求头、请求体）
    c、视图函数必须返回一个HttpResponse对象或其子对象
    """
    print(request)
    print(type(request))
    print(type(request).__mro__)
    if request.method == 'GET':
        return HttpResponse(f"<h1>获取项目信息{request}哦</h1>")
    elif request.method == 'POST':
        return HttpResponse(f"<h1>创建项目信息{request}哦</h1>")
    elif request.method == 'PUT':
        return HttpResponse(f"<h1>更新项目信息{request}哦</h1>")
    elif request.method == 'DELETE':
        return HttpResponse(f"<h1>删除项目信息{request}哦</h1>")
    else:
        return HttpResponse(f"<h1>不合法的请求方式</h1>")


class ProjectsView(View):
    """
    一、定义类视图
    1、继承view或者view的子类
    2、不同的请求方法有相应的方法进行对应
            GET-》get
            POST--》post
            PUT--》put
            DELETE----》delete
            PATCH -->patch
    3、每一个处理请求的方法，必须返回HttpResponse对象或HttpResponse的子对象
    4、每一个处理请求的方法，第二个参数必须是httpRequest的对象


    """

    def get(self, request, pk):
        project_data = {
            'id': 1,
            'name': 'XXX项目',
            'leader': 'sea_name'
        }
        project_data_list = [
            {
                'id': 1,
                'name': 'XXX项目',
                'leader': 'sea_name'
            },
            {
                'id': 2,
                'name': 'XXX项目2',
                'leader': 'sea_name2'
            },
        ]
        # 5、HttpResponse
        # a、HttpResponse第一个参数为字符串类型（需要返回给前端的字符串数据）
        # b、content_type可以指定响应头中的content_type类型
        # c、status可以指定状态码

        json_str = json.dumps(project_data, ensure_ascii=False)
        # return HttpResponse(json_str, content_type='application/json', status=201)

        # json_dumps_params={'ensure_ascii': False}--保证中文不会转义
        # 6、JsonResponse
        # a、为HttpResponse的子类
        # b、用于返回json数据
        # c、第一个参数可以直接传字典或者嵌套字典的列表
        # d、默认添加：setdefault("content_type", "application/json")--
        # e、默认第一个参数只能为字典。如果为其他数据类型（嵌套数据列表），则需要safe=False

        # 7、两种开发模式
        # 1、前后端不分离的开发模式
        # a、后端如果返回的是一个完整的html页面，

        # 2、前后端分离的开发模式
        # a、后端如果返回的是数据（json、xml）
        return JsonResponse(project_data_list, json_dumps_params={'ensure_ascii': False}, safe=False)

    def put(self, request):
        return HttpResponse(f"<h1>更新项目信息{request}哦</h1>")

    def post(self, request, pk):
        # 前端参数的解析
        # 一、前端传参方式
        # 1、路径参数
        # a、在url路径中传递的参数
        # b、在请求实例发放中，使用关键字参数来接收
        #

        # 2、查询字符串参数
        # a、url？后边的key value键值对，如http://XXX:8000/projects/6/?key1=value1&key2=value2
        # b、request.GET获取
        # c、request.GET返回的QueryDict，类似于python中的dict类型
        # d、可以使用['key']、get['key1'],会返回具体的值，如果有多个相同的值，则返回最后一个
        # e、getList（‘key1’），获取相同的key的多个值，返回list类型

        # 请求体参数：
        # 1、json
        # a、JSON格式的参数存放在body中，一般为字节类型
        # b、json.load()返回python中的数据类型（字典、嵌套字典的列表）

        # 2、www-form-urlencoded
        # a、一般在前端页面中使用表单录入的参数
        # b、request.post返回的QueryDict，类似于python中的dict类型

        # 3、请求头参数
        # a、第一种方式：如何传递纯粹的问，request.header['key']
        # b、第2中：request.META['HTTP_AUTHORIZATION']
        #   请求头参数可以转化为HTTP_参数名大写
        #   如果参数中含有-，会自动转化为_

        return HttpResponse(f"<h1>创建项目信息{request}哦</h1>")

    def delete(self, request):
        return HttpResponse(f"<h1>删除项目信息{request}哦</h1>")

    def some_view(self):
        response = HttpResponse(content_type='text/csv',
                                headers={'Content-Disposition': 'attachment; filename = "somefilename.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', 'A', 'B', 'C','Testing', "Here's a quote"])
        return response


