from django.db import models

# Create your models here.
class Stu(models.Model):#�̳�ģ����
    sname=models.CharField(max_length=10)#��������
    spwd=models.CharField(max_length=10)
    class Meta:#����Ҫ�洢�����ݿ�����,Ĭ�ϰ��ո�������ƴ���
        db_table='mydjango'
