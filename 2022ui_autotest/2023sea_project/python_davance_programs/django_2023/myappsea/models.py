# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Animal(models.Model):
    """
    1)一般在子应用models.py中定义模型类（相当于数据库中的一张表）
    2）必须继承model或者model子类
    3）在模型类中定义类属性（必须是Filed子类）-相当于数据表中的字段
    4）CharField-对应varchar
        IntegerField-->int
        BooleanField-->bool
    5) 生成迁移脚本，在migrations里，存放迁移脚本 python manage.py makemigrations 子应用名(如果不指定子应用，会把所有子应用生成迁移脚本)
    6）查看迁移脚本生成的sql语句：python manage.py sqlmigrate
    7) 生成的数据表名称默认为：子应用名_模型类名（myappsea_animal）
    8）默认会自动创建一个名为id的自增字段
    """
    # varchar 变字符串
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'mydjango'

class Projects(models.Model):
    ids = models.IntegerField(primary_key=True, verbose_name='主键', help_text='主键')
    # a、CharField必须指定max_length参数（该字段的最大字节数）
    # b、如果需要给一个添加唯一约束，unique = True（默认为false）
    name = models.CharField(max_length=20, verbose_name='项目名称', help_text='项目名称',
                            unique=True)
    leader = models.CharField(max_length=20, verbose_name='项目负责人', help_text='项目负责人',
                            unique=False)
    # 使用default-指定默认值，在创建记录时，该字段传递，会使用默认值
    is_excue = models.BooleanField(verbose_name='是否启动项目', help_text='是否启动项目',
                            unique=True, default=True)
    # null=True指定，前端创建数据时，可以指定该字段未null，默认为null=False，DRF进行反序列化
    # blank=True指定前端创建数据时，可以指定该字段为空字符串，默认为false
    desc = models.TextField(verbose_name='项目描述信息', help_text='是否启动项目', null=True, blank=True, default='')
    # auto_now_add=True，在创建一条数据时，会自动将创建时间作为该字段的时间
    # auto_now=True--在更新数据时，会自动更新该字段的值
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    # 可以在任意一个模型类中创建meta内部类，用于修改数据库的元数据信息
    class Meta:
        managed = True
        # 指定数据库的名称
        db_table = 'tb_projects'

