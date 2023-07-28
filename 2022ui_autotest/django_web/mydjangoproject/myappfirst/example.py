# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm 新增一个example文件创建一个简单的试图显示
# @Author: duansea
# @Time: 2022年12月月14日 12:42
# ---
from django.http import HttpResponse
from django.shortcuts import render

<<<<<<< HEAD
<<<<<<< HEAD
from django.db import models
from django.core.mail import send_mail
from django.http import HttpResponse


def sendSimpleEmail(request,emailto):
    res = send_mail("hello paul", "comment tu vas?", "xxx@(cainiaojc.com)", [emailto])
    return HttpResponse('%s'%res)

class Dreamreal(models.Model):
    website = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phonenumber = models.IntegerField()
    class Meta:
        db_table = "dreamreal"



=======
>>>>>>> 5210fa1b7715b51962a03b38b5322cac1dc97b6c
=======
>>>>>>> 5210fa1b7715b51962a03b38b5322cac1dc97b6c

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


