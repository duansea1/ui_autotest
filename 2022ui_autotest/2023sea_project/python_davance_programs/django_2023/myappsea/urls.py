# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-01-01 13:18
# ---
from django.urls import path
from rest_framework.documentation import include_docs_urls

from . import views
from rest_framework import routers
# 子项目中的路径urlpatterns=[]


# 1、可以使用路由器对象，为视图及自动生成条目
# 2、路由器对象默认只为通用actions （create,list,retrice,update)生成路由条目，自定义
# 3、SimpleRouter创建对象
router = routers.SimpleRouter()
# router = routers.DefaultRouter() # 会自动指定根路径
# 4、使用路由器对象调用register方法进行注册
# 5、prefix指定路由前缀
# 6、viewset指定视图集
router.register(r'projects', views.ProjectsView)

urlpatterns = [
    # path('projects/', views.projects),

    # path('create/', views.get_project),
    # path('put/', views.put_project),
    # path('delete/', views.delete_project),

    # 使用类属性定义视图路由；；类视图.as_view
    # path('projects/<int:pk>/', views.ProjectsView.as_view()),
    # path('projects/csv/', views.ProjectsView.as_view()),
    path('projects/', views.ProjectsView.as_view()),  # 查询数据
    path('projects/<int:pk>/', views.ProjectsDetailView.as_view()),  # 查询、更新、删除
    path('projects/names/', views.ProjectsView.as_view(
    )),
    path('projects/interfaces/', views.ProjectsView.as_view()),
    path('docs/', include_docs_urls(title='测试平台接口文档', description='API文档')),

    # 7、加载路由条目
    # 方式一：加载路由条目
    # path(' ', include(router.urls)),
]

# 方式二
# router.url为列表
# urlpatterns += router.urls
