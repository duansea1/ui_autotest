from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def hello_web(request):
    """¥¥Ω® ”Õº"""
    text = """<h1>welcom to my first djangoweb!<h1>"""
    return HttpResponse(text)