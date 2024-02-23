# -*- coding: utf-8 -*-
from django.db import models
from myappsea.models import Projects
from utils.base_model import BaseModel
# 表与表之间有哪些关系？
# myappsea与interfaces表，一对多的关系

# 学生表与学生详细信息表，一对一关系

# 学生表与课程表，是多对多的关系

# 继承BaseModel
class Interfaces(BaseModel):
    # id = models.AutoField(primary_key=True, verbose_name='主键', help_text='主键')
    name = models.CharField(max_length=200,verbose_name='接口名称',help_text='接口名称', unique=True)
    tester = models.CharField(max_length=200, verbose_name='测试人员',help_text='测试人员')

    # interface与project表建立联系on_delete=models.CASCADE、
    # a、如果需要创建一对一的外键，那么会在“多”的那个一个模型类中定义外键字段OneToOneFiled
    # b、如果是一对多，使用ForeignKe；
    #   方式1、直接使用父表模型类的引用
    #   方式2、可以使用 子应用名称.父类模型类名
    # 使用ForeignKe，需要使用on_delete指定级联删除策略
    # -CASCADE：当父表数据删除时，相对应的从表数据会自动删除
    # -PROTECT 当父表数据删除时，相对应的从表会抛出异常
    # -SET-NULL 当父表数据删除时，相对应的从表数据会自动置为null
    # -SET_DEFAULT 当父表数据删除时，相对应的从表数据会自动置为默认值，还需要额外指定default=true

    # c、如果是多对多，使用ManyToManyField
    # d
    # -- 从表与主表进行关联：to=Projects--指向model模块中的关联【模型类】；；on_delete当主表数据被删除时，从表数据也会删除
    projects = models.ForeignKey(to=Projects, on_delete=models.CASCADE, verbose_name='所属项目', help_text='所属项目',
                                 related_name='interToP')
    # projects = models.ForeignKey(to='projects.Projects' )  # 两种建立关联方式
    # create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间', help_text='创建时间')
    # update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        managed = True
        # 指定数据库的名称
        db_table = 'tb_interfaces'
        # 未当前数据表设置中文描述信息
        verbose_name = '接口表'
        verbose_name_plural = '接口表'
        ordering = ['id']

    def __str__(self):
        return f"Interfaces({self.name})"


