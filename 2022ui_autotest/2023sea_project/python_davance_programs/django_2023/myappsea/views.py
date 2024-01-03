# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):

    return HttpResponse("11k看sea", content_type='text/plain; charset=utf-8')

def get_project(request):
    return HttpResponse("<h1>这个是一个项目信息</h1>")

def get_project1(request):
    return HttpResponse("<h1>这个是一个项目信息1</h1>")

def get_project2(request):
    return HttpResponse("<h1>这个是一个项目信息2222</h1>")


def create_project(request):
    return HttpResponse("<h1>这个是一个项目信息create</h1>")

def put_project(request):
    return HttpResponse("<h1>这个是一个项目信息put</h1>")

def delete_project(request):
    return HttpResponse("<h1>这个是一个项目信delete</h1>")

def get_projects(request, pk):
    return HttpResponse(f"<h1>这个是一个项目信{pk}</h1>")