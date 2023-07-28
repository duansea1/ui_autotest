from django.db import models

# Create your models here.
class Stu(models.Model):#继承模型类
    sname=models.CharField(max_length=10)#设置列名
    spwd=models.CharField(max_length=10)
    class Meta:#设置要存储的数据库名称,默认按照父类的名称创建
        db_table='mydjango'
