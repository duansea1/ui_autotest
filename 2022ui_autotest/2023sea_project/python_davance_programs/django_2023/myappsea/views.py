# -*- coding:utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
import json

import csv
from .models import Projects
from django.db import connection
from interfaces.models import Interfaces

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

    def get1(self, request, pk):
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

    def get(self, request, pk):
        # 一、创建
        # 方式一
        # 直接使用模型类（字段名=值1，字段2=值2），来创建模型实例
        # b、必须使用模型实例，调用save（）方法才会执行sql语句
        # obj = Projects(name='在线哈哈', leader='B负责人')
        # obj.save()  # 执行sql语句
        # pass
        # 方式二
        # a、使用模型类.objects.create
        # b\使用manage对象的.create(字段名=值1，字段2=值2)来创建模型类实例
        # c、无需使用save方法，直接调用皆可
        # Projects.objects.create(name='在线玲子', leader='玲子夜东京')

        # 二、读取
        # 1、读取多条数据
        # qs = Projects.objects.all()
        # 2、读取单条数据
        # 方式1：
        # Projects.objects.get(id=1)
        # 方式二
        # a、可以使用模型类.filter()返回querySet对象
        # b、如果使用指定条件查询的记录数量为0，会返回空的QuerySet对象
        # c、如果使用指定条件查询的记录数量超过1，将符合条件的模型对象包裹在QuerySet对象中返回
        # 支持数值索引取值、支持切片操作、first()\last()\获取长度：len（Query对象）、count()
        # 判断对象是否为空exists（）
        # obj2 = Projects.objects.filter(id=1)
        # ORM框架中，会给每一个模型类中的主键设置一个别名<pk>
        # obj2 = Projects.objects.filter(pk=1)
        # id__gte:greate_than
        # Projects.objects.filter(id__in=[1,4]) in(1,2,3)
        # Projects.objects.filter(id__contains='XXX')--LIKE BINARY '%hhh%'
        # Projects.objects.filter(id__gte=1)

        """
         filter方法支持多种查询类型:
         1、字段名_查询类型=具体值
         2、字段名_exac = 具体值。==》字段名=具体值
         3、字段名_gte:大于等于 _gt:大于
         4、字段名_lt:小于   字段名_lte 小于等于
         5、contains 包含
         6、startwith:以XXX开头
         7、endwith：以XXX结尾
         8、isnull:是否为null
         9、一般前面加上i，表示忽略
         10、exclude为反向查询，filter支持所有类型的查询


        """
        # 创建从表数据
        # 外键对应的父表如何传递？
        # -方式一：1、先获取父表的模型对象；2、将获取的父表对象以外件名作为参数传递
        # project_obj = Projects.objects.get(name='詹姆斯')
        # interface_obj = Interfaces.objects.create(name='在线图书项目-执行', tester='布克',
        #                           projects=project_obj)

        # a、通过从表模型对象（已经获取到了），如何获取父表数据
        # 可以通过外键字段先获取父类模型对象
        # projects_obj = Projects.objects.get(id=1)
        # projects_obj.interfaces_set.all()

        # b、通过父表模型对象（已经获取到了）
        # 默认可以通过从表模型类名小写_set,返回manager对象，可以进一步使用filter进行过滤
        # projects_obj.interfaces_set.all()-返回的是manager对象
        # 如果在从表模型类的外键字段，指定了related_name参数，那么可以使用related_name参数projects_obj.inter
        # interface_obj.projects.name

        # c、如果想要通过父表参数来获取从表数据，想要通过从表参数获取父表数据---关联查询
        # 可以使用关联查询格式：
        # 关联字段名称_关联模型类中的字段名_查询类型
        # projects_obj.inter.filter(interfaces_name='XXX')
        # interfaces_obj.inter.filter(projects_name='XXX')

        # d\逻辑关系
        # 与关系
        # 方式一：在同一个方法内部使用，使用添加多个关键字参数，那么每个条件为“与”的关系
        # 方式二：可以多次调用filter方法，那么filter方法为“与”的关系---QuerySet链式调用
        # Projects.objects.filter(name_contains='2', leader='湖人')
        # 或关系：
        # 可以使用Q查询，实现逻辑关系，多个Q对象之间，如果使用“|”，那么是或的关系
        # qs = Projects.objects.filter(Q(name__contains='2') | Q(leader='湖人'))

        # e\ 排序：
        # 可以使用QuerySet对象.order_by(字段名1，-字段名2)
        # 默认asc升序，可以在字段前面加-，那么就是降序排列
        # Projects.objects.filter(Q(name__contains='2') | Q(leader='湖人'))order_by('-name')

        # 三、更新：
        # 方式一：1、先获取数据
        pj = Projects.objects.get(id=1)
        pj.name = 'update-在线用户'
        pj.leader = '保罗'
        pj.save()
        pass

        # return JsonResponse(project_data_list, json_dumps_params={'ensure_ascii': False}, safe=False)

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


