# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-01-22 19:06
# ---
"""
一、序列化器
a、如果使用DRF来实现序列化、反序列化、数据操作，在serializers.py文件中
b、文件名称推荐serializers

"""
from rest_framework import serializers
from interfaces.models import Interfaces
from .models import Projects

# -- 从表获取数据，校验操作主表的数据
class InterfacesSerializer(serializers.Serializer):
    """
    1、自定义序列化类实际上也是Field的子类
    2、所以自定义的序列化器类可以作为另一个序列化器中的字段
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    leader = serializers.CharField()

    projects = serializers.PrimaryKeyRelatedField(label='项目id', help_text='项目id')
