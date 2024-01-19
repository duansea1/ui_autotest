# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-01-13 16:16
# ---

from django.db import models

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键', help_text='主键')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        # 在内部类meta中，一旦指定了abstract = True,那么当前的类字段不会自动创建表。在迁移时不会创建表，仅仅是为了供其他类继承
        abstract = True
