# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-01-01 13:18
# ---
from django.urls import path

from . import views
# 子项目中的路径urlpatterns=[]

urlpatterns = [
    # path('projects/', views.projects),

    # path('create/', views.get_project),
    # path('put/', views.put_project),
    # path('delete/', views.delete_project),

    # 使用类属性定义视图路由；；类视图.as_view
    path('projects/<int:pk>/', views.ProjectsView.as_view()),
    path('projects/csv/', views.ProjectsView.as_view())
]