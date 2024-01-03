# -*- coding:utf-8 -*-
"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin

from django.urls import path, include, re_path
from myappsea import views
from myappsea import views

"""
# 一、什么是路由？
# 1、定义
#  url与后端视图之间的一一映射关系

# 2、添加路由
# 在路由文件urls.py中的urlpatterns列表中添加路由；
# 从上到下进行匹配路径
3) urlpaterns 列表从上到下进行匹配
4）一旦匹配成功，就会终止往下匹配
5）如果匹配不成功，就会一直往下匹配
6）如果全部匹配不成功，那么会抛出404页面

、path函数
1）用于定义路由条目
2）第一个参数为url路径参数，路径最前面不能添加/,路径最后边添加/
3)第二个参数为视图函数或者类视图，如果添加的视图函数，，无需使用（）
4）如果第二个参数为include,那么会继续进入子路由匹配，子路由匹配规则和全局路由规则一致
5) 第一个参数可以使用类型转换器
    <类型转换器：参数名称>
    默认的类型转换器：int、str、slug、uuid
    参数名称，在调用视图时，会自动传递给视图函数，需要使用同名的参数接收
"""

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('project/index/', views.index),
    # path('get_project/', views.get_project),
    # path('get_project1/', views.get_project1),

    # 参数值匹配路径路由
    path('projects/<int:pk>/', views.get_projects),
    path('project/', include('myappsea.urls')),
    path('cases/', include('myappsea.urls')),
    re_path(r'projects/(?P<pk>\w{3})/$',views.get_projects),

]

