# -*- coding:utf-8 -*-
import logging
from urllib.request import Request

from icecream import ic
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, filters
from .models import Projects

from myappsea.serializers import ProjectSerializer, ProjectModelSerializer
from utils.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework.decorators import action
# Create your views here.
"""
视图层，在页面展示的，可以在此进行定义方法，返回对应的html格式or其他格式的数据，如csv文件下载
"""
logger = logging.getLogger('myappsea')

class ListModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)
        page = self.paginate_queryset(queryset)
        print(page)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            # 调用get_paginated_response方法，将序列化之后的数据进行分页，并返回response
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.filters import SearchFilter

class CustomSearchFilter(SearchFilter):
    search_param = 'keyword'  # 自定义搜索参数名


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2  # 每页显示的记录数
    page_size_query_param = 'page_size'  # 允许客户端通过查询参数来覆盖每页大小
    max_page_size = 100  # 客户端请求的最大每页记录数

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
# class ProjectsView(APIView):
class ProjectsView(generics.ListCreateAPIView):
    """
    【定义视图集】
    """
    # 一旦继承GenericAPIView之后，往往需要指定queryset、serializer_class类属性
    queryset = Projects.objects.all()
    # serializer_class指定当前类视图的实例化方法需要使用序列化器类
    serializer_class = ProjectModelSerializer
    # search_fields可以在字段名称前添加相应的符号，指定查询类型
    search_fields = ['=name', '=leader', '=id']

    # filter_backends在继承了Ger类视图指定的过滤
    # filter_backends = [filters.SearchFilter]
    filter_backends = [CustomSearchFilter]
    search_param = 'keyword'

    # 可以在类视图中指定分页引擎类，优先级高于全局
    pagination_class = PageNumberPagination
    ic(pagination_class)

    def get(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ic(queryset)
        page = self.paginate_queryset(queryset)
        print(page)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            # 调用get_paginated_response方法，将序列化之后的数据进行分页，并返回response
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # 如果需要使用路由器机制，自动生成条目，那么就必须得使用action装饰器
    # 2、method指定需要使用的请求方法，如果不指定，默认GET
    # 3、detail-指定是否为详情接口，是否需要传递当前模型的pk值（如果需要传递当前模型的pk值，则detail需要设置True）
    # 4、url_path 指定url路由
    # url_name – 定义此操作的内部（“反向”）URL 名称。默认为使用下划线替换为破折号修饰的方法的名称

    @action(methods=['GET'], detail=False)
    def names(self, request, *args, **kwargs):
        # queryset = self.get_object()
        # queryset = self.filter_queryset(queryset)
        # names_list = []
        # for project in queryset:
        #     names_list.append({
        #         'id': project.id,
        #         'name': project.name
        #
        #     })
        # return Response(names_list, status=200)
        return super().list(request, *args, **kwargs)

    @action(detail=True)
    def interfaces(self, request, *args, **kwargs):
        project = self.get_object()
        logger.info(123)
        interfaces_qs = project.interfaces_set.all()
        interfaces_data = [{'id':interface.id, 'name':interface.name} for interface in interfaces_qs]

        logger.debug(interfaces_data)
        return Response(interfaces_data, status=200)

    # def retrieve(self, request, *args, **kwargs):
    #     pass

    # def get_serializer_class(self):
    #     """
    #     重写父类的get_serializer_class，用于为不同的action提供不一样的序列化器类
    #     """
    #     if self.action == 'retrieve':
    #         return ProjectModelSerializer1
    #     else:
    #         return super().get_serializer_class()
    
    # def filter_queryset(self, queryset):
    # 重写过滤
    #     if self.action == 'names':
    #         return self.queryset
    #     else:
    #         return super(ProjectsView, self).filter_queryset()
    
    # def get_queryset(self):
    #     if self.action == 'names':
    #         self.queryset.filter(name__icontains = '2')
    #     else:
    #         super(ProjectsView, self).get_queryset()

class ProjectsDetailView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         GenericAPIView):
    """
    # 1、获取一条数据（详情数据）、
    # GET /projects/<int:pk>/
    # 4、编辑、
    # # PUT /projects/<int:pk>/ 新的项目数据以JSON的形式传递
    # 5、删除项目数据
    # DELETE /projects/<int:pk>/
    --数据校验（规范传入的参数）--》反序列化输入操作（将json格式的数据转化为复杂的类型）-》数据库操作（判断数据是否存在）--》序列化操作
    """
    qs_all = Projects.objects.all()
    serializer_class = ProjectSerializer
    # lookup_url_kwar指定url路由条目中外键的路径参数
    lookup_url_kwarg = 'kk'
    search_fields = ['name', 'leader', 'id']

    def get_object(self, pk):
        try:
            project_obj = Projects.objects.get(id=pk)   # 待更新的数据
            return project_obj
        except Exception as e:
            return Response({'msg': 'pk不存在'}, status=400)

    def get(self, request, pk, *args, **kwargs):

        #  filter_queryset 对查询对象进行过滤
        # qs_all = self.filter_queryset(self.get_queryset(pk))
        # project_obj = self.get_object(pk)  # self.get_object()  --可以不传递pk参数
        #
        # serializer = self.serializer_class(instance=project_obj)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, pk):
        """更新数据"""
        # 获取指定数据
        project_obj = self.get_object(pk)

        serializer = self.serializer_class(instance=project_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        # if not serializer.is_valid():
        #     return JsonResponse(serializer.errors, status=402)
        # 需要进行大量的数据校验
        print('project_obj返回参数：:', project_obj)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """
        删除项目数据
        """
        # try:
        #     project_obj = Projects.objects.get(id=pk)
        # except Exception as e:
        #     return JsonResponse({'msg': 'pk不存在'}, status=1002)
        project_obj = self.get_object(pk)
        # 3、执行删除
        project_obj: Projects
        project_obj.delete()
        project_dic = {
            # 'id': project_obj.id,
            'name': project_obj.name,
            'msg': '数据删除成功'
        }
        return Response(project_dic, status=status.HTTP_200_OK)

