<<<<<<< HEAD
import datetime

from django.shortcuts import render

# Create your views here.
# -*-coding:utf-8-*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse


def hello_web(request, num=9):
    """ChuangJianShiTu"""
    text = """<h1>welcom to my first djangoweb!<h1>
            <div>ya haha!:%s <div>
            """ % num
    # return HttpResponse(text)
    # return redirect('https://www.baidu.com')
    return redirect(viewArticles, year="2045", month="02")


def hell(request):
    """ChuangJianShiTu"""
    text = """<h1>djangoweb!<h1>
            <div>ya haha!---hell <div>
            """
    res = '<h1>hellyuming:   ' + reverse('hell') + '<h1>'
    return HttpResponse(res)


def viewArticles(request, month, year):
    text = "Displaying articles of : %s/%s"%(year, month)
    return HttpResponse(text)
    # return redirect(viewArticles, year = "2045", month = "02")


def showdatetime(request):
    today = datetime.datetime.now().date()
    daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    # return render(request, 'hello_2.html', {'today': today, 'days_of_week': daysOfWeek})
    return redirect("https://www.baidu.com")    # 重定向链接














=======
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def hello_web(request):
    """创建视图"""
    text = """<h1>welcom to my first djangoweb!<h1>"""
    return HttpResponse(text)
>>>>>>> 5210fa1b7715b51962a03b38b5322cac1dc97b6c
