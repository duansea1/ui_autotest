# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm 新增一个example文件创建一个简单的试图显示
# @Author: duansea
# @Time: 2022年12月月14日 12:42
# ---
from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    text = """<h1>welcom to my first djangoweb!<h1>"""
    return HttpResponse(text)

def helloo(request):
    """视图无参数情况"""
    return render(request, "/myappfirst/templates/hello.html", {})

def some_args(request, number):
    """视图还可以接受参数"""
    text = "<h1>welcome to my app number %s !<h1>" % number
    return HttpResponse(text)


