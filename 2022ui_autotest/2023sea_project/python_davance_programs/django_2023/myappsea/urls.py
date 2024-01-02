# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-01-01 13:18
# ---
from django.urls import path

from . import views
urlpatterns = [
    path('get/', views.get_project2),
    path('create/', views.get_project),
    path('put/', views.put_project),
    path('delete/', views.delete_project),
]